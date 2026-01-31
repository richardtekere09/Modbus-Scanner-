import serial.tools.list_ports
from pymodbus.client.sync import ModbusSerialClient
import time

# Common baud rates
BAUD_RATES = [9600, 19200, 38400, 57600, 115200]

# Slave ID range
SLAVE_IDS = range(1, 247)

# Timeout
TIMEOUT = 0.5


def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    # Filter only USB serial ports (avoids AirPods/Bluetooth on macOS)
    return [p.device for p in ports if "usb" in p.device.lower()]


def scan_port(port):
    print(f"\n Scanning port: {port}")

    for baud in BAUD_RATES:
        print(f"   Trying baud rate: {baud}")

        client = ModbusSerialClient(
            method="rtu",
            port=port,
            baudrate=baud,
            stopbits=1,
            bytesize=8,
            parity="N",
            timeout=TIMEOUT,
        )

        if not client.connect():
            continue

        for slave_id in SLAVE_IDS:
            try:
                result = client.read_holding_registers(
                    address=0, count=1, slave=slave_id
                )
                if result and not result.isError():
                    print("\n MODBUS DEVICE FOUND!")
                    print(f"   Port      : {port}")
                    print(f"   Baud rate : {baud}")
                    print(f"   Slave ID  : {slave_id}")
                    client.close()
                    return True
            except Exception:
                pass

        client.close()

    return False


def main():
    ports = get_serial_ports()
    if not ports:
        print(" No COM ports found")
        return

    print("Found COM ports:", ports)

    for port in ports:
        if scan_port(port):
            print("\n Scan complete")
            return

    print("\nNo Modbus devices detected")


if __name__ == "__main__":
    main()
