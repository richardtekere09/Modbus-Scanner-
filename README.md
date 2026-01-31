import serial.tools.list_ports
from pymodbus.client.sync import ModbusSerialClient

# Common baud rates (OWEN devices typically use 9600, 19200, or 115200)
BAUD_RATES = [9600, 19200, 115200, 38400, 57600]

# OWEN devices typically use slave IDs 1-32
SLAVE_IDS = range(1, 33)

# Timeout (OWEN devices can be slow to respond)
TIMEOUT = 2  # Increased to 2 seconds for reliability

# Common parity settings to try
PARITY_OPTIONS = ["E", "N"]  # Even parity first, then None

# Common register addresses to probe
REGISTER_MAP = {
    "Device Info (0-10)": (0, 10),
    "Device Model/Serial (100-110)": (100, 10),
    "Configuration (200-210)": (200, 10),
    "Sensor Values (300-310)": (300, 10),
    "Status Registers (1000-1010)": (1000, 10),
}

def get_serial_ports():
    """Auto-detect all available COM ports"""
    ports = serial.tools.list_ports.comports()
    # Prioritize OWEN USB converters (they often show up with specific VID/PID)
    owen_ports = [p.device for p in ports if "USB" in p.description.upper()]
    other_ports = [p.device for p in ports if p.device not in owen_ports]
    return owen_ports + other_ports  # Check OWEN devices first

def read_device_info(client, slave_id):
    """Try to read additional information from the device"""
    print("\n📋 Reading additional device information...\n")
    
    for description, (start_addr, count) in REGISTER_MAP.items():
        try:
            result = client.read_holding_registers(address=start_addr, count=count, unit=slave_id)
            
            if not result.isError() and hasattr(result, 'registers'):
                # Filter out registers with all zeros (often unused)
                non_zero_regs = [r for r in result.registers if r != 0]
                
                if non_zero_regs:
                    print(f"  ✓ {description}")
                    print(f"    Registers: {result.registers}")
                    # Try to interpret as ASCII text
                    try:
                        # Convert registers to bytes (each register = 2 bytes)
                        bytes_data = b''.join(r.to_bytes(2, 'big') for r in result.registers)
                        # Try to decode as ASCII, ignore non-printable chars
                        text = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_data)
                        if text.strip('.'):  # If there's actual text
                            print(f"    ASCII: {text}")
                    except:
                        pass
                    print()
                    
        except Exception:
            # Silently skip registers that don't respond
            pass

print('=== MODBUS SCANNER FOR OWEN USB-RS485 ===\n', flush=True)

# Auto-detect COM ports
available_ports = get_serial_ports()
print(f"[INFO] Found {len(available_ports)} COM port(s): {', '.join(available_ports)}\n", flush=True)

if not available_ports:
    print("[ERROR] No COM ports detected!")
    print("[HELP] Make sure OWEN USB-RS485 driver is installed")
    print("       Download from: https://owen.ru\n")
    exit()

device_found = False
found_client = None
found_port = None
found_baud = None
found_slave = None
found_parity = None

for port in available_ports:
    if device_found:
        break
    
    print(f"[SCAN] Scanning port: {port}", flush=True)
    
    for parity in PARITY_OPTIONS:
        if device_found:
            break
            
        parity_name = {"E": "Even", "N": "None", "O": "Odd"}[parity]
        print(f"  → Trying parity: {parity_name}", flush=True)
        
        for baud in BAUD_RATES:
            if device_found:
                break
                
            print(f"    → Trying baud rate: {baud}", flush=True)

            try:
                client = ModbusSerialClient(
                    method="rtu",
                    port=port,
                    baudrate=baud,
                    stopbits=1,
                    bytesize=8,
                    parity=parity,
                    timeout=TIMEOUT
                )
                
                if not client.connect():
                    continue
                
                for slave in SLAVE_IDS:
                    try:
                        result = client.read_holding_registers(address=0, count=1, unit=slave)
                        
                        # Check if we got a valid response
                        if not result.isError():
                            print("\n" + "="*50)
                            print("🎯 OWEN DEVICE FOUND!")
                            print("="*50)
                            print(f"  COM Port:  {port}")
                            print(f"  Baud Rate: {baud}")
                            print(f"  Parity:    {parity_name}")
                            print(f"  Slave ID:  {slave}")
                            print("="*50)
                            
                            # Save info for detailed reading
                            found_client = client
                            found_port = port
                            found_baud = baud
                            found_slave = slave
                            found_parity = parity
                            device_found = True
                            break  # Break slave loop
                            
                    except Exception:
                        pass  # Ignore errors, keep scanning

                if not device_found:
                    client.close()
                
                if device_found:
                    break  # Break baud loop
                    
            except Exception as e:
                print(f"    [ERROR] {e}", flush=True)

# If device was found, read additional info
if device_found and found_client:
    read_device_info(found_client, found_slave)
    found_client.close()
    print("[INFO] Connection closed")
else:
    print("\n[RESULT] No Modbus devices found")
    print("\n[TROUBLESHOOTING]")
    print("  1. Check USB-RS485 converter is plugged in")
    print("  2. Check OWEN driver is installed")
    print("  3. Verify RS485 A/B wiring is correct")
    print("  4. Check device power supply")
    print("  5. Verify device is in Modbus RTU mode")

print("\n=== SCAN COMPLETE ===")