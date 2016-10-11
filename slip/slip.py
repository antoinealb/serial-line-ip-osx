END = bytes((0xc0, ))
ESC = bytes((0xdb, ))
ESC_ESC = bytes((0xdd, ))
ESC_END = bytes((0xdc, ))

def decode(conn):
    current_packet = bytes()
    while True:
        byte = conn.read(1)
        if byte == END:
            yield current_packet
            current_packet = bytes()
            continue
        elif byte == ESC:
            byte = conn.read(1)
            if byte == ESC_END:
                byte = END
            elif byte == ESC_ESC:
                byte = ESC
            else:
                raise ValueError("Unknown escape sequence.")
        current_packet = current_packet + byte

def encode(data):
    data = data.replace(ESC, ESC + ESC_ESC)
    data = data.replace(END, ESC + ESC_END)
    return data + END
