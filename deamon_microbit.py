import time
import sys
import asyncio
import websockets
from bluezero import microbit

ubit = microbit.Microbit(adapter_addr='DC:A6:32:16:77:A8',
                         device_addr='DA:B9:23:9F:EB:82',
                         accelerometer_service=True,
                         button_service=True,
                         led_service=True,
                         magnetometer_service=False,
                         pin_service=True,
                         temperature_service=True)




async def connectToWebSocket():
  uri = "ws://localhost:8080"
  async with websockets.connect(uri) as websocket:
    print("[connected to websocket]")
    while True:
      io_pin = ubit._io_pin_data.value
      pin, value = [int(v) for v in io_pin]

      if pin == 0 and value == 1:
        print('>> PIN 0 button pressed')
        await websocket.send("button")

      if ubit.button_a:
        print('>> A Button')
        await websocket.send("button") # useless only for debug (hardware always connected button)

      if ubit.button_b:
        print(">> B Button")
        print("[disconnecting progress]")
        ubit.disconnect()   

def startConnect():
  print("[connection to micro:bit] ...")
  try:
      ubit.connect()
      print("[connected]")
      ubit.set_pin(0, True, False) # Set Micro:bit pin 0 to read digital value

      main_loop = asyncio.get_event_loop()
      main_loop.run_until_complete(connectToWebSocket()) # Connect to websocket only when connected to micro:bit
      
  except OSError as err:
      print("OS error: {0}".format(err))
  except ValueError:
      print("[error occured w/ micro:bit]")
  except:
      print("Unexpected error:", sys.exc_info()[0])
      ubit.disconnect()
      time.sleep(2)
      startConnect()
    


startConnect()