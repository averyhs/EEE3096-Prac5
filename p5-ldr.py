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

# create an analog input channel on pin 1
chan = AnalogIn(mcp, MCP.P1)

# Function to print sensor value every 5 seconds
def print_adc_thread():
    thread = threading.Timer(5.0, print_adc_thread) # execute every 5s
    thread.daemon = True # Exit thread when program does
    thread.start()

    runtime = time() - starttime # calculate runtime
    runtime = int(runtime)
    
    # Calculate light
    ldr_voltage = 3.3 - chan.voltage

    # print adc value
    print(runtime,"s\t",chan.value,"\t\t",ldr_voltage," V",sep="")

if __name__ == "__main__":
    starttime = time() # get start time
    print("Runtime\tADC Reading\tLDR Voltage")
    print_adc_thread() # start print thread

    while time() - starttime < 35:
        pass # run for 30 sec
