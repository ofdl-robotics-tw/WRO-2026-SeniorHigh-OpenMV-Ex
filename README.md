# WRO 2026 Senior High - OpenMV Mosaic Color Reading Solution

https://github.com/user-attachments/assets/98428324-91ca-499b-8688-3b2581e33abf

An open-source computer vision solution developed by OFDL Taiwan for the WRO 2026 Senior High category. This project provides robust OpenMV MicroPython scripts for high-speed 12-block mosaic color reading and LPF2 data transmission to LEGO SPIKE Prime or EV3 hubs.

## Features

* **12-Block Mosaic Auto-Sorting**: Sorts detected blobs by Y-axis (3 rows) and X-axis (4 columns) to ensure precise 3x4 grid mapping.
* **LPF2 Data Compression**: Packs 12 color codes into 4 compressed integer packets (`combined[0..3]`) conforming to LEGO LPF2 limits.
* **Reliability Check**: Enforces strict count validation (`len == 12`) to eliminate false detections, with runtime LED status feedback.

## Color Mapping

| Color | Code | LAB Threshold Range |
| :--- | :---: | :--- |
| Green | 1 | `(24, 42, -55, -22, -8, 19)` |
| White | 2 | `(86, 100, 3, 127, -128, 27)` |
| Blue | 3 | `(100, 30, -128, 127, -128, -28)` |
| Yellow | 4 | `(100, 0, -50, 5, 29, 67)` |

## Hardware
You can use SPIKE Ultrasonic sensor breakout board, or cut a wire to connect to SPIKE Hub, and connnect the wire as:
```
OpenMV Pins<------> SPIKE Pins
       GND <------> Pin 3 GND
       VIN <------> Pin 4 3V3
       Tx  <------> Pin 6 Rx
       Rx  <------> Pin 5 Tx
```
