import serial.tools.list_ports
from pymodbus.client.sync import ModbusSerialClient
from tqdm import tqdm

# Common baud rates (OWEN devices typically use 9600, 19200, or 115200)
BAUD_RATES = [9600, 19200, 115200, 38400, 57600]

# OWEN devices typically use slave IDs 1-32
SLAVE_IDS = range(1, 33)
#SLAVE_IDS = range(1, 247) # if you want to scan all possible IDs incomment this line 

# Timeout (OWEN devices can be slow to respond)
TIMEOUT = 2

# Common parity settings to try
PARITY_OPTIONS = ["E", "N"]  # Even parity first, then None

def get_serial_ports():
    """Auto-detect all available COM ports"""
    ports = serial.tools.list_ports.comports()
    # Prioritize OWEN USB converters
    owen_ports = [p.device for p in ports if "USB" in p.description.upper()]
    other_ports = [p.device for p in ports if p.device not in owen_ports]
    return owen_ports + other_ports

print('=== MODBUS SCANNER FOR  USB-RS485 ===\n', flush=True)

# Auto-detect COM ports
available_ports = get_serial_ports()
print(f"[INFO] Found {len(available_ports)} COM port(s): {', '.join(available_ports)}\n", flush=True)

if not available_ports:
    print("[ERROR] No COM ports detected!")
    print("[HELP] Make sure  USB-RS485 driver is installed")
    #print("       Download from: https://owen.ru\n")
    exit()

device_found = False
found_port = None
found_baud = None
found_slave = None
found_parity = None

# Calculate total iterations for progress bar
total_iterations = len(available_ports) * len(PARITY_OPTIONS) * len(BAUD_RATES) * len(SLAVE_IDS)

# Create progress bar
with tqdm(total=total_iterations, desc="Scanning", unit="probe") as pbar:
    for port in available_ports:
        if device_found:
            pbar.update(len(PARITY_OPTIONS) * len(BAUD_RATES) * len(SLAVE_IDS))
            break
        
        for parity in PARITY_OPTIONS:
            if device_found:
                pbar.update(len(BAUD_RATES) * len(SLAVE_IDS))
                break
                
            parity_name = {"E": "Even", "N": "None", "O": "Odd"}[parity]
            
            for baud in BAUD_RATES:
                if device_found:
                    pbar.update(len(SLAVE_IDS))
                    break
                    
                pbar.set_description(f"Scanning {port} @ {baud} baud ({parity_name})")

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
                        pbar.update(len(SLAVE_IDS))
                        continue
                    
                    for slave in SLAVE_IDS:
                        try:
                            result = client.read_holding_registers(address=0, count=1, unit=slave)
                            
                            # Check if we got a valid response
                            if not result.isError():
                                pbar.close()  # Close progress bar before printing
                                

                                print("\n" + "="*50)
                                print("  DEVICE FOUND (УСТРОЙСТВО НАЙДЕНО)!")
                                print("="*50)
                                print(f"  COM Port (COM-порт):  {port}")
                                print(f"  Baud Rate (Скорость): {baud}")
                                print(f"  Parity (Четность):    {parity_name}")
                                print(f"  Slave ID (Адрес):  {slave}")
                                print("="*50 + "\n")
                                
                                found_port = port
                                found_baud = baud
                                found_slave = slave
                                found_parity = parity
                                device_found = True
                                break
                                
                        except Exception:
                            pass
                        
                        pbar.update(1)
                        
                        if device_found:
                            break

                    client.close()
                    
                    if device_found:
                        break
                        
                except Exception:
                    pbar.update(len(SLAVE_IDS))

if not device_found:
    print("\n[RESULT] No Modbus devices found (Устройства Modbus не найдены)")
    print("\n[TROUBLESHOOTING](УСТРАНЕНИЕ НЕПОЛАДОК)")
    print("  1. Check USB-RS485 converter is plugged in (Проверьте, подключен ли преобразователь USB-RS485)")
    print("  2. Check OWEN driver is installed (Проверьте, установлен ли драйвер OWEN)")
    print("  3. Verify RS485 A/B wiring is correct (Проверьте правильность подключения RS485 A/B)")
    print("  4. Check device power supply (Проверьте питание устройства)")
    print("  5. Verify device is in Modbus RTU mode (Убедитесь, что устройство работает в режиме Modbus RTU)")

print("\n=== SCAN COMPLETE ===")
