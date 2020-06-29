from ina219 import INA219
from RPi_AS3935 import RPi_AS3935
import RPi.GPIO as GPIO
import threading
import smbus2
import bme280
import time

def multiSense():
    port = 1
    address = 0x76
    bus = smbus2.SMBus(port)

    calibration_params = bme280.load_calibration_params(bus, address)

    # the sample method will take a single reading and return a
    # compensated_reading object
    data = bme280.sample(bus, address, calibration_params)

    # the compensated_reading class has the following attributes

    print("Sensor: BME280")
    print("Address: 0x76")
    print(str(round(data.temperature)) + "C")
    print(str(round(data.pressure)) + "hPa")
    print(str(round(data.humidity)) + "%")

def powerSense():
    SHUNT_OHMS = 0.1
    MAX_EXPECTED_AMPS = 0.25

    ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
    ina.configure(ina.RANGE_16V, ina.GAIN_AUTO)

    print("Sensor: INA219")
    print("Address: 0x40")
    print("Bus Voltage    : %.3f V" % ina.voltage())
    print("Bus Current    : %.3f mA" % ina.current())
    print("Supply Voltage : %.3f V" % ina.supply_voltage())
    print("Shunt voltage  : %.3f mV" % ina.shunt_voltage())
    print("Power          : %.3f mW" % ina.power())

def strikeSense():
    GPIO.setmode(GPIO.BCM)

    global sensor
    sensor = RPi_AS3935(address=0x03, bus=1)
    print("Calibrating lightning sensor...")
    sensor.set_indoors(False)
    sensor.set_noise_floor(0)
    sensor.calibrate(tun_cap=0x07)
    print("Calibration complete: ✓")

    def handle_interrupt(channel):
        time.sleep(0.003)
        reason = sensor.get_interrupt()
        if reason == 0x01:
            print("Noise level too high - adjusting")
            sensor.raise_noise_floor()
        elif reason == 0x04:
            print("Noise event detected - masking")
            sensor.set_mask_disturber(True)
        elif reason == 0x08:
            distance = sensor.get_distance()
            print("Sensor: AS3935")
            print("Address: 0x03")
            print("Lightning detected")
            print(str(distance) + "km away. (%s)" % now)

    pin = 17

    GPIO.setup(pin, GPIO.IN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=handle_interrupt)

    while True:
        time.sleep(1.0)


###########################################################################
#Lightning service must be event driven therefore requiring its own thread#
###########################################################################
x = threading.Thread(target=strikeSense)

print("Starting lightning service...\n")

try:
    x.start()
    print("Lightning service started: ✓\n")
except:
    print("Failed to start lightning service: X\n")

###########
#Main loop#
###########
while True:
    multiSense()
    powerSense()

    time.sleep(300)
