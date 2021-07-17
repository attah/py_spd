#!/usr/bin/env python3
import hid
import hexdump
import sys
import argparse

vid = 0x0483
pid = 0x1230

def readData(h):
    r=h.read(64)
    # print(r, file=sys.stderr)
    return r

parser = argparse.ArgumentParser()
parser.add_argument("--bin", help="output raw binary",
                    action="store_true")
args = parser.parse_args()

data = bytearray(b'')

with hid.Device(vid, pid) as h:
    print(f'Device manufacturer: {h.manufacturer}', file=sys.stderr)
    print(f'Product: {h.product}', file=sys.stderr)
    print(f'Serial Number: {h.serial}', file=sys.stderr)
    h.write(b'BT-VER001')
    readData(h)
    h.write(b'BT-MCUID')
    readData(h)
    h.write(b'BT-I2C1WR6C064E5931393038')
    readData(h)
    h.write(b'BT-I2C1RD')
    readData(h)
    print("-"*76, file=sys.stderr)
    for addr in range(0, 256, 8):
      cmd = bytearray(b'BT-I2C2RD50')
      cmd.extend('{:02x}'.format(addr).encode('ascii'))
      cmd.extend("08".encode('ascii'))
      h.write(bytes(cmd))
      r = readData(h)
      data.extend(bytes.fromhex(r[2:25].decode('ascii')))

if args.bin:
  sys.stdout.buffer.write(data)
else:
  hexdump.hexdump(data)

#Write:
#BT-I2C2WR50000892110B01031A0008
