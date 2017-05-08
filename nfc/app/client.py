#from Adafruit_GPIO import I2C

# https://github.com/adafruit/Adafruit_Python_GPIO/blob/master/Adafruit_GPIO/I2C.py
# https://github.com/adafruit/Adafruit_Python_GPIO/blob/master/tests/test_I2C.py

#device = I2C.get_i2c_device(0x2d)
#print(device)
#print(dir(device))
#!/usr/bin/env python
#
# Basic example of using Python-SMBus and a PCF8574
# Use at your own risk.
#
#  1 Write 0x55AA to device
#  2 Check for I/O error (no device connected)
#  3 Read the device
#  4 Display result
#
# Assumes PCF8575 at I2C address 0x20 (see i2c_addr)
#   Nothing connected to PCF8575 that will cause problems
#
#   This version requires Python V2.6+
#      Not Python 3
#
# PC Services PCF8575/Python-smbus example
# November 2012

# define I2C address of PCF8575 (0x20 to 0x27 are valid)
i2c_addr = 0x2d<<1

# import libraries
import smbus as smbus

#configure I2C bus for functions
i2c = smbus.SMBus(1)

# value to send
#temp = 0xAC0200A4040007D276000085011010035c0
temp = 0xAC
# Set PCF8575 outputs
try :
   print 'PCF8575 at address 0x{0:02x} WRITE 0x{1:04x}'.format( i2c_addr, temp )
   i2c.write_byte_data( i2c_addr, temp & 0xff, ( temp & 0xff ) >> 8 )
except IOError :
   print 'PCF8575 Device not found at I2C address 0x{1:02x}'.format( i2c_addr )
   error = 1
else :
   # Now read from PCF8575
   temp = i2c.read_word_data( i2c_addr, 0 )
   print 'PCF8575 at address 0x{0:02x} READ 0x{1:04x}'.format( i2c_addr, temp )


