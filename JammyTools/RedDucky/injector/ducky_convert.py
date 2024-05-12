from JammyTools.RedDucky.injector.hid import Key, Mod
from .helpers import log
from JammyTools.RedDucky.injector.colors import cprint, iprint, wprint, cinput, RED, GREEN, WHITE, MAGENTA, BLUE, RESET, BRIGHT, CYAN, YELLOW, LIGHT_GREEN, BLACK, LIGHT_YELLOW, LIGHT_RED, LIGHT_BLUE, LIGHT_CYAN, LIGHT_MAGENTA, LIGHT_WHITE

def send_string(client, string_to_send, start_pos=0):
    log.debug(f"{YELLOW}Sending string: {string_to_send}")
    for char in string_to_send[start_pos:]:
        log.debug(f"{BLUE}Sending character: {char}")
        client.send_ascii(char)

def send_command(client, command):
    log.debug(f"{LIGHT_MAGENTA}Processing command: {command}")
    if '+' in command:
        print(f"{YELLOW}Most likely a Shortcut")
        keys = command.split('+')
        keys = [k.strip() for k in keys]
        keycodes = []

        for key in keys:
            if hasattr(Key, key):
                keycodes.append(getattr(Key, key))
            elif hasattr(Mod, key):
                keycodes.append(getattr(Mod, key))

        log.debug(f"{CYAN}Sending keycodes: {keycodes}")

        # Send keycodes
        for keycode in keycodes:
            client.send_keypress(keycode)

        # Release keys
        for keycode in reversed(keycodes):
            client.send_keypress(keycode)
    else:
        if hasattr(Key, command):
            client.send_keypress(getattr(Key, command))
        elif hasattr(Mod, command):
            client.send_keypress(getattr(Mod, command))

def get_mod_key(mod_str):
    mod_map = {
        'CONTROL': Mod.LeftControl,
        'SHIFT': Mod.LeftShift,
        'ALT': Mod.LeftAlt,
        'META': Mod.LeftMeta,
        'GUI': Mod.LeftMeta,
    }
    return mod_map.get(mod_str)

def get_key(key_str):
    if hasattr(Key, key_str):
        return getattr(Key, key_str)
    return None

def send_ducky_command(client, command):
    log.debug(f"{LIGHT_YELLOW}Processing ducky command: {command}")
    keys = command.split()
    keycodes = []

    for key in keys:
        if hasattr(Key, key):
            keycodes.append(getattr(Key, key))
        elif hasattr(Mod, key):
            keycodes.append(getattr(Mod, key))
        else:
            key = get_mod_key(key) or get_key(key)
            if key:
                keycodes.append(key)

    if keycodes:
        log.debug(f"{CYAN}Sending ducky keycodes: {keycodes}")
        client.send_keyboard_report(*keycodes)
        client.send_keyboard_report()  # Release keys
