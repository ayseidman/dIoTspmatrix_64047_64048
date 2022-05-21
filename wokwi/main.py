from MatrixSparseDOK import MatrixSparseDOK
# from MessageHandler import MessageHandler
# from Time import Time
# from MQTT import MQTT



print("Hello, ESP32!")

# vc = ((5, 4), 0.0, (7.4, 7.5, 5.5, 5.6, 7.8, 6.7, 0.0), (7, 7, 5, 5, 7, 6, -1), (1, 2, 0))

# vd = MatrixSparseDOK.decompress(vc)
# print(len(vd))
# print(vd)
# vd.zero = 7.5
# print(len(vd))
# print(vd)


#screen = OLED()

#screen.text('Hello, Wokwi!', 10, 10, 1)
#screen.show()

#from WokwiTests import HeatMapTFT, PIRSensor

#testSensor = PIRSensor()

#testTFT = HeatMapTFT()
#testTFT.random()
# from Time import now

# def den(value=None):
#     print("ALIVE:")

# _last_checked_time = now()
# def _check_new_day(value=None):
#         global _last_checked_time
#         """ Check if it is a new day. If so, insert yesterday's log in logger. """
#         print("Check if it is new day!")
#         present_time = now()
#         if _last_checked_time.day != present_time:
#             """ New Day. Write logs and clear matrix"""
#             print("New Day!")
#             print("Logging is done!")

#         _last_checked_time = present_time

# from machine import Timer
# tim1 = Timer(0)
# tim1.init(period=10000,mode=Timer.PERIODIC, callback=_check_new_day)

# tim2 = Timer(3)
# tim2.init(period=10000,mode=Timer.PERIODIC, callback=den)



from SparseMatrixProcessingEngine import SparseMatrixProcessingEngine
app = SparseMatrixProcessingEngine()
app.run()


#handler = MessageHandler(MQTT)
#handler.run()



while (1):
    pass