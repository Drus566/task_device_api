from random import randrange

def get_mac_address():
    mac = []
    for byte in range(6):
        byte = hex(randrange(256)).replace('0x', '').zfill(2)
        mac.append(byte)
    mac = ':'.join(mac)
    return mac

def is_even(num):
    if num % 2 == 0:
        return True 
    else:
        return False

