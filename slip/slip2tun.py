#!/usr/bin/env python3
"""
Bridge between a serial port sending packets using SLIP protocol and a network
tunnel (TUN) device.
"""
import argparse
import serial
import time
import subprocess
import os
import sys

import threading
from slip import decode, encode

def rx_thread(conn, tun_fd):
    """
    Thread reading from the serial connection and forwarding it on the TUN
    device.
    """
    decoder = decode(conn)
    for packet in decoder:
        os.write(tun_fd, packet)


def tx_thread(conn, tun_fd):
    """
    Thread reading from the TUN device and forwarding it to the serial connection.
    """
    while True:
        packet = os.read(tun_fd, 1500)
        packet = encode(packet)
        conn.write(packet)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("-p", "--port",
                        help="serial port to use (e.g. /dev/ttyUSB0)",
                        required=True)
    parser.add_argument("-b", "--baudrate", help="Baudrate (default 115200)",
                        default=115200, type=int)

    parser.add_argument("-i", "--interface", default="tun0",
                        help="network interface to use (default tun0)")

    return parser.parse_args()

def main():
    args = parse_args()

    if os.getuid() != 0:
        print("slip2tun must run as root.")
        sys.exit(1)

    conn = serial.Serial(args.port, baudrate=args.baudrate)
    tun_fd = os.open("/dev/{}".format(args.interface), os.O_RDWR)
    subprocess.call("ifconfig {} 192.168.3.1 192.168.3.2".format(args.interface).split())

    rx_thd = threading.Thread(target=rx_thread, args=(conn, tun_fd))
    tx_thd = threading.Thread(target=tx_thread, args=(conn, tun_fd))

    rx_thd.start()
    tx_thd.start()

    rx_thd.join()
    tx_thd.join()



if __name__ == '__main__':
    main()
