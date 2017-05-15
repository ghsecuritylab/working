/* Example: NfcTagDisplay (Displays the content of the EEPROM after changing the NDef record with a NFC phone/Smartcard reader)
   Arduino library for ST M24SR Dynamic NFC/RFID tag IC with EEPROM, NFC Forum Type 4 Tag and I2C interface
   (c) 2014 by ReNa http://regnerischernachmittag.wordpress.com/ 
*/

#include <PN532.h>
#include <NfcAdapter.h>
#include <Wire.h>
#include <crc16.h>
#include <M24SR.h>



#define gpo_pin 7
M24SR m24sr(gpo_pin);

//http://playground.arduino.cc/Code/AvailableMemory
int freeRam () {
  extern int __heap_start, *__brkval; 
  int v; 
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval); 
}

void setup()
{
  Serial.begin(9600);
  //for debug purpose
  //m24sr._verbose = true;
  //m24sr._cmds = true;
  m24sr._setup();

  displayFreeRAM();
  m24sr.displaySystemFile();

  displayNDefRecord();
 Serial.print(F("STARTED"));
}

void loop()
{
}

void displayNDefRecord() {
    //read NDef message from memory
    NdefMessage* pNDefMsg = m24sr.getNdefMessage();
    displayFreeRAM();
    if (pNDefMsg != NULL) {
       pNDefMsg->print();
       NdefRecord rec = pNDefMsg->getRecord(0);
//       String txt = rec.toString();
       Serial.print(F("NDefRecord: "));
//       Serial.println(txt);
Serial.println(rec.getType());
Serial.println(rec.getId());


       delete pNDefMsg;
    }
}

void displayFreeRAM() {
  Serial.print(F("\r\nfree RAM: "));
  Serial.println(freeRam(), DEC);
}

