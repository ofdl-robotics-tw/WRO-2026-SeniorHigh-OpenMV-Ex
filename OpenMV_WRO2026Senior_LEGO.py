# OFDL Robotics Lab Taiwan = Anthony 2026
# WRO 2026 SeniorHigh OpenMV Example

import sensor
import time
import math
import gc,utime
import micropython
import LPF2
from machine import Pin
from pyb import LED
micropython.alloc_emergency_exception_buf(200)

sensor.reset()
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # must be turned off for color tracking
sensor.set_auto_whitebal(False)  # must be turned off for color tracking
clock = time.clock()

##LUMP Define
modes = [LPF2.mode('OpenMV-ALL',size = 8, type = LPF2.DATA16, format = '3.0'),]
DataToSend = [0, 0, 0, 0, 0, 0, 0, 0] #X, Y, W, H, ID, state, 0, 0
lpf2 = LPF2.Prime_LPF2(3, 'P4', 'P5', modes, 62, timer = 4, freq =10)
lpf2.initialize()

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track in general red/green/blue things. You may wish to tune them...
thresholds = [
   (24, 42, -55, -22, -8, 19),  # generic_green_thresholds
   (86, 100, 3, 127, -128, 27),  # generic_white_thresholds
   (100, 30, -128, 127, -128, -28), # generic_blue_thresholds
   (100, 0, -50, 5, 29, 67), # generic_yellow_thresholds
 ]

color_names = ["green", "white", "blue", "yellow"]
color_code_map = [1, 2, 3, 4]
ROI = (0, 0, 320, 220)

while True:
    #If LEGO Brick not connect
    if not lpf2.connected:
        LED(1).on() # Turn on Red LED
        LED(2).off() # Turn off Green LED
        LED(3).off() # Turn off Blue LED
        lpf2.sendTimer.deinit()
        utime.sleep_ms(50)
        lpf2.initialize()
    else:
        LED(1).off() # Turn off Red LED
        clock.tick()
        img = sensor.snapshot()

        blobs_data = []

        for blob in img.find_blobs(
            thresholds,
            pixels_threshold=200,
            area_threshold=200,
            merge=True,
            roi=ROI
        ):
            code = blob.code()
            color_index = int(math.log(code, 2))
            color_number = color_code_map[color_index]

            blobs_data.append((blob.cx(), blob.cy(), color_number))

            img.draw_rectangle(blob.rect())
            img.draw_string(blob.x(), blob.y(), str(color_number), color=(255,0,0))
            img.draw_rectangle(ROI)

        # 確保一定12個
        if len(blobs_data) == 12:

            # 1️⃣ 依 y 排序
            blobs_data.sort(key=lambda b: b[1])

            # 2️⃣ 自動分三排（用平均切）
            row1 = blobs_data[0:4]
            row2 = blobs_data[4:8]
            row3 = blobs_data[8:12]

            rows = [row1, row2, row3]

            result = []

            for row in rows:
                # 3️⃣ 每排依 x 排序
                row.sort(key=lambda b: b[0])

                for b in row:
                    result.append(b[2])

            #print(result)

            combined = []

            for i in range(0, 12, 3):
               num = result[i] * 100 + result[i+1] * 10 + result[i+2]
               combined.append(num)

            print(combined)

            img.draw_string(0,0,"OK", color=(0,255,0))
            DataToSend = [combined[0], combined[1], combined[2], combined[3], 1, 0, 0, 0]

        else:
            img.draw_string(0,0,"NO", color=(255,0,0))
            DataToSend[4] = 0

        #Send Data to LEGO Brick
        mode=lpf2.current_mode
        if mode==0:
             lpf2.load_payload('Int16',DataToSend)
