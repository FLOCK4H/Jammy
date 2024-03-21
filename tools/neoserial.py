import serial
import serial.tools.list_ports
import time
from tools.colors import cprint, iprint, wprint, cinput, RED, GREEN, WHITE, MAGENTA, BLUE, RESET, BRIGHT, CYAN, YELLOW, LIGHT_GREEN, BLACK, LIGHT_YELLOW, LIGHT_RED, LIGHT_BLUE, LIGHT_CYAN, LIGHT_MAGENTA, LIGHT_WHITE

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    available_ports = []
    index = 0
    for port, desc, hwid in sorted(ports):
        index += 1
        cprint(f"{index}) {port}: {desc} [{hwid}]")
        available_ports.append(port)
    return available_ports

def connect_to_repl_and_send_command(port, command, baudrate=115200):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)
        ser.reset_input_buffer()

        time.sleep(1)
        while ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)

        ser.write((command + '\r\n').encode('utf-8'))
        ser.flush()

        
        time.sleep(1)
        while ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)

    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
    finally:
        ser.close()