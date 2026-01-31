# Modbus Scanner
A **Python tool** to discover Modbus devices connected to your computer via USB → RS-485 converters.  
It scans all connected COM ports, tries common baud rates, and finds Modbus slave IDs.

---

## Features

- Automatically detects all connected COM ports
- Scans common Modbus RTU baud rates: `9600, 19200, 38400, 57600, 115200`
- Scans Modbus slave IDs in the range `1–247`
- Safe **read-only** scanning (no writing to registers)
- Prints detected devices with port, baud rate, and slave ID
