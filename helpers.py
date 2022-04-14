def flip_endian(hex_string):
    return bytes.fromhex(hex_string)[::-1].hex()