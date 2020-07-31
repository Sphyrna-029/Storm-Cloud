from ina219 import INA219
from RPi_AS3935 import RPi_AS3935
from datetime import datetime, timezone
import RPi.GPIO as GPIO
import threading
import requests
import smbus2
import socket
import uuid
import json
import hashlib
import bme280
import time

##########
# Config #
##########

endpoint = "http://192.168.1.185/events"
port     = 8081


dataPayload = {}


def dateTime():
    local_time = datetime.now(timezone.utc).astimezone()

    dataPayload.update( { 'datetime' : local_time.isoformat() } )


def IdGen():
    #generate a ID unique to the station from static attributes (stateless and persists on reboot barring ip change)
    host_name = socket.gethostname()
    host_mac = hex(uuid.getnode())
    hashstr = host_name + host_mac

    hash = hashlib.md5(hashstr.encode('utf-8')).hexdigest()

    dataPayload.update( { 'stationid' : hash } )

    return hash


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
    dataPayload.update( { 'temperature' : round(data.temperature, 2) } )
    print(str(round(data.pressure)) + "hPa")
    dataPayload.update( { 'pressure' : round(data.pressure, 2) } )
    print(str(round(data.humidity)) + "%")
    dataPayload.update( { 'humidity' : round(data.humidity, 2) } )

def powerSense():
    SHUNT_OHMS = 0.1
    MAX_EXPECTED_AMPS = 0.25

    ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
    ina.configure(ina.RANGE_16V, ina.GAIN_AUTO)

    print("Sensor: INA219")
    print("Address: 0x40")
    print("Bus Voltage    : %.3f V" % ina.voltage())
    dataPayload.update( { 'busvoltage' : round(ina.voltage(), 2) } )
    print("Bus Current    : %.3f mA" % ina.current())
    dataPayload.update( { 'buscurrent' : round(ina.current(), 2) } )
    print("Supply Voltage : %.3f V" % ina.supply_voltage())
    dataPayload.update( { 'supplyvoltage' : round(ina.supply_voltage(), 2) } )
    print("Shunt voltage  : %.3f mV" % ina.shunt_voltage())
    dataPayload.update( { 'shuntvoltage' : round(ina.shunt_voltage(), 2) } )
    print("Power          : %.3f mW" % ina.power())
    dataPayload.update( { 'power' : round(ina.power(), 2) } )

def strikeSense():
    GPIO.setmode(GPIO.BCM)

    global sensor
    sensor = RPi_AS3935(address=0x03, bus=1)
    print("Calibrating lightning sensor...")
    sensor.reset()
    sensor.set_indoors(False)
    sensor.set_noise_floor(0)
    time.sleep(2)
    sensor.calibrate(tun_cap=0x0F)
    time.sleep(2)
    print("Calibration complete: ✓")

    def handle_interrupt(channel):
        time.sleep(0.003)
        reason = sensor.get_interrupt()
        if reason == 0x01:
            print("Noise level too high - adjusting")
            nf = sensor.raise_noise_floor()
            print("Noise floor: " + str(nf))
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
    print("Station ID: " + IdGen())
    dateTime()
    multiSense()
    powerSense()

    json_payload = json.dumps(dataPayload, indent = 4)
    print(json_payload)

    try:
        r = requests.post('http://192.168.1.132:8081/events', data=json_payload)
        print(r.status_code, r.reason)
    except:
        pass

    dataPayload = {}

    time.sleep(300)
