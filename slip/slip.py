END = 0xc0
ESC = 0xdb
ESC_ESC = 0xdd
ESC_END = 0xdc

def decode(conn):
    current_packet = bytes()
    while True:
        byte = ord(conn.read(1))
        if byte == END:
            yield current_packet
            current_packet = bytes()
            continue
        elif byte == ESC:
            byte = ord(conn.read(1))
            if byte == ESC_END:
                byte = END
            elif byte == ESC_ESC:
                byte = ESC
            else:
                raise ValueError("Unknown escape sequence.")
        current_packet = current_packet + bytes([byte])

def encode(data):
    data = data.replace(bytes((ESC, )), bytes((ESC, ESC_ESC)))
    data = data.replace(bytes((END, )), bytes((ESC, ESC_END)))
    return data + bytes((END, ))
