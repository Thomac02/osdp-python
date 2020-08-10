#!/usr/bin/env python3

from sys import argv
import os
import stat
from osdp import *

print("Starting OSDP Peripheral Device test...")

if len(argv) < 4:
    print("Incorrect usage -> osdp_test.py DEVICE ADDRESS USE_SC")
    exit()

os.chmod(argv[1], 666)

addr = 0
if argv[2].startswith("0x"):
    addr = int(argv[2][2:], 16)
else:
    addr = int(argv[2], 10)
print("Running poll loop at address " + argv[2])

conn = SerialPortOsdpConnection(port=argv[1], baud_rate=9600)
cp = ControlPanel()
bus_id = cp.start_connection(conn)
 
cp.add_device(connection_id=bus_id, address=addr, use_crc= True, use_secure_channel=argv[3])

keyset = cp.keyset(connection_id=bus_id, address=addr)
if keyset:
    print("New encryption key set")

id_report = cp.id_report(connection_id=bus_id, address=addr)
print(id_report)

device_capabilities = cp.device_capabilities(connection_id=bus_id, address=addr)
print(device_capabilities)

local_status = cp.local_status(connection_id=bus_id, address=addr)
print(local_status)

input_status = cp.input_status(connection_id=bus_id, address=addr)
print(input_status)

output_status = cp.output_status(connection_id=bus_id, address=addr)
print(output_status)

cp.shutdown()
