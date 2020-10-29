import threading
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from time import time

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)
# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

# Function to print sensor value every 10 seconds
def print_adc_thread():
    thread = threading.Timer(10.0, print_adc_thread) # execute every 10 s
    thread.daemon = True # Exit thread when program does
    thread.start()

    runtime = time() - starttime # calculate runtime
    runtime = int(runtime)
    
    # Calculate temp
    # From datasheet: Vout = Tc * Ta + V0
    # => Ta = (Vout - V0) / Tc
    Tc = 10.0 # temp coeff from datasheet
    V0 = 0.5 # [V] Vout at T=0C from datasheet
    temp = (chan.voltage - V0)/Tc

    # print adc value
    print(runtime,"s\t",chan.value,"\t\t",temp," C",sep="")

if __name__ == "__main__":
    starttime = time() # get start time
    print("Runtime\tTemp Reading\tTemp")
    print_adc_thread() # start print thread

    while int(time() - starttime) < 65:
        pass # run for 1 min
