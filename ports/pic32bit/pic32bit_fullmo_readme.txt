2025-09-05 oliver.heggelbacher@fullmo.de
Micropython integration in MPLAB X / PIC32MZ / XC32 v2.50 / Harmony v1.11

- Based on https://github.com/micropython/micropython master
v1.9.4
Commit 5ed578e5
by Paul Sokolovsky, 26.10.2018 21:27
committed by Damien George, 20.12.2018 07:52

- fullmo specific additions: ports\pic32bit
  (based on ports\pic16bit, modifications, e.g. for pic32bit: #define MPZ_DIG_SIZE (16)

- Added helper ports/pic32bit/pic32bit-make-qstr-port.py
  to allow adding new QSTR in mcdrive.c, mccom.c, a.s.o without recompiling micropython via 
  GNU make / Makefile
