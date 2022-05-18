from network import WLAN, STA_IF
from time import sleep, localtime
from Time import Time, synchronize_local_time


class CommunicationInterface:

    USER_NAME = "Wokwi-GUEST"
    PASSWORD = ""

    def __init__(self):
        self._physical_interface = WLAN(STA_IF)

    def connect(self):
        print("Connecting to WiFi")
        self._physical_interface.active(True)
        self._physical_interface.connect(CommunicationInterface.USER_NAME, CommunicationInterface.PASSWORD)
        while not self._physical_interface.isconnected():
            print(".", end="")
            sleep(0.1)
        print("\nConnected!",)
        synchronize_local_time()

    def disconnect(self):
        self._physical_interface.disconnect()

