from MatrixSparseDOK import MatrixSparseDOK
from MessageHandler import MessageHandler
from Time import Time
from MQTT import MQTT
import ntptime
import machine



print("Hello, ESP32!")
 
vc = ((5, 4), 0.0, (7.4, 7.5, 5.5, 5.6, 7.8, 6.7, 0.0), (7, 7, 5, 5, 7, 6, -1), (1, 2, 0))

vd = MatrixSparseDOK.decompress(vc)
print(len(vd))
print(vd)
vd.zero = 7.5
print(len(vd))
print(vd)


def d1(msg):
  print("cmd")
  print(msg)

def d2(msg):
  print("data")
  print(msg)

def d3(msg):
  print("net")
  print(msg)

handler = MessageHandler(MQTT)
handler.run()

while(1):
  pass