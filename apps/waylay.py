from m5stack import *
from m5stack_ui import *
from uiflow import *
import urequests
import wifiCfg
import time
import json

import unit

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xaa3838)
Ultrasonic_1 = unit.get(unit.ULTRASONIC, unit.PORTA)
pir_1 = unit.get(unit.PIR, unit.PORTB)


status = None
json_data = None
DoorStatus = None
DataMap = None

wifiCfg.autoConnect(lcdShow=True)
UsStatus2 = M5Label('Text', x=163, y=127, color=0x000, font=FONT_MONT_14, parent=None)
image0 = M5Img("res/window.png", x=220, y=37, parent=None)
image1 = M5Img("res/door.png", x=34, y=37, parent=None)
image2 = M5Img("res/waylay.png", x=110, y=204, parent=None)
HttpStatus = M5Label('Text', x=34, y=215, color=0x000, font=FONT_MONT_14, parent=None)
ps = M5Label('Text', x=238, y=215, color=0x000, font=FONT_MONT_14, parent=None)
PirLabel1 = M5Label('PIR:Not Detected', x=9, y=113, color=0x000, font=FONT_MONT_14, parent=None)
UsStatus1 = M5Label('US:Not Detected', x=193, y=113, color=0x000, font=FONT_MONT_14, parent=None)


# Describe this function...
def SendPOST():
  global status, json_data, DoorStatus, DataMap
  status = 'No Status'
  try:
    req = urequests.request(method='POST', url='Fill-in-your-webscript-url',data=json_data, headers={'Content-Type':'application/json'})
    ps.set_text_color(0x006600)
    wait(5)
    status = req.status_code
    ps.set_text('Data sent')
  except:
    ps.set_text_color(0x990000)
    wait(5)
    ps.set_text('Not sent')
  wait(5)
  HttpStatus.set_text(str(status))



import custom.urequests as urequests
while True:
  if (pir_1.state) == 1:
    PirLabel1.set_text(str('PIR: Detected'))
    DoorStatus = 1
    DataMap = {'WindowStatus':1}
    json_data = json.dumps(DataMap)
    wait(1)
    SendPOST()
  else:
    PirLabel1.set_text('PIR: Not detected')
  wait(1)
  UsStatus2.set_text(str((str('Distance: ') + str(((str((Ultrasonic_1.distance)) + str(' mm')))))))
  if (Ultrasonic_1.distance) < 300:
    UsStatus1.set_text('US: Detected')
    DoorStatus = 1
    DataMap = {'DoorStatus':1}
    json_data = json.dumps(DataMap)
    wait(1)
    SendPOST()
  else:
    UsStatus1.set_text('US: Not detected')
  wait_ms(2)

