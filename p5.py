import RPi.GPIO as GPIO
import threading
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from time import time

# Define global variables
chan = None # SPI channel
thread = None # thread of print_adc_thread
sample_rates = [1, 5, 10] # list of sample rates to toggle through
sr_idx = 0 # start with sample rate of 1s

# Function to set up SPI for the ADC
def spi_setup():
    global chan
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI) # create the spi bus
    cs = digitalio.DigitalInOut(board.D5) # create the cs (chip select)
    mcp = MCP.MCP3008(spi, cs) # create the mcp object
    chan = AnalogIn(mcp, MCP.P1) # create an analog input channel on pin 1

# Function to set up gpio for pushbutton
def gpio_setup():
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) # set button on pin18 as input with pullup resistor
    GPIO.add_event_detect(24, GPIO.FALLING, callback=toggle_samp_rate, bouncetime=500) # set callback & debounce

# Function to print sensor value every 10 seconds
def print_adc():
    global chan, thread, sample_rates, sr_idx
    thread = threading.Timer(sample_rates[sr_idx], print_adc) # execute every <interval> seconds
    thread.daemon = True # Stop thread if program stops
    thread.start()

    runtime = int(time() - starttime) # calculate runtime

    # Calculate temp
    # From datasheet: Vout = Tc * Ta + V0
    # => Ta = (Vout - V0) / Tc
    Tc = 10.0 # temp coeff from datasheet
    V0 = 0.5 # [V] Vout at T=0C from datasheet
    temp = (chan.voltage - V0)/Tc

    # print adc value
    print(runtime,"s\t",chan.value,"\t\t",temp," C",sep="")

# Callback fn for button to toggle sampling rate
def toggle_samp_rate(channel):
    global thread, sample_rates, sr_idx
    sr_idx = (sr_idx + 1) % 3
    
    if thread.is_alive():
        thread.cancel() # cancel currently running thread
        print_adc()

if __name__ == "__main__":
    spi_setup()
    gpio_setup()
    
    print("Runtime\tADC Reading\tTemperature")
    starttime = time() # get start time
    print_adc()

    while time() - starttime < 61:
        pass # run for 1 min

