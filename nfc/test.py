#!/usr/bin/python

import smbus
import time
from time import sleep
bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

DEVICE_ADDRESS = 0x56    #7 bit address (will be left shifted to add the read write bit)
DEVICE_REG_MODE1 = 0x00
DEVICE_REG_LEDOUT0 = 0x1d

#Write a single register
#bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, 0x80)
print(bus.write_byte(DEVICE_ADDRESS,0x26))
print("---")
#Write an array of registers
#sleep(0.098)
ledout_values = [0x00, 0xA4, 0x04, 0x00, 0x07, 0xD2,0x76,0x00,0x00,0x85,0x01,0x01,0xA6,0x09]
print(bus.write_i2c_block_data(0x56, 0x02, ledout_values))
#bus.write_i2c_block_data(0x20,0,[0x09, 0x00, 0b10101010])
b = bus.i2c_smbus_read_byte(0x56)

print(b)