import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

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

    print(’Raw ADC Value: ’, chan.value)
    print(’ADC Voltage: ’ + str(chan.voltage) + ’V’)

if __name__ == "__main__":
    print_adc_thread() # start print thread

    while True:
        pass # run indefinitely
