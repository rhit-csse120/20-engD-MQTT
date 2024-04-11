# Example showing a Pico, running MicroPython (NOT CircuitPython),
# communicating with another device through MQTT.
# Author:  David Mutchler, Rose-Hulman Institute of Technology,
#          based on examples from the internet.

# These imports are for the WIFI and MQTT communication:
from machine import Pin, PWM
import network
from umqtt.simple import MQTTClient

# These imports are for simulating sending sensor data:
import random
import time

# MQTT Topics to publish/subscribe from/to Pico to/from HiveMQ Cloud
UNIQUE_ID = "DavidMutchler1019"  # Use something that no one else will use
PC_TO_DEVICE_TOPIC = UNIQUE_ID + "/pc_to_device"
DEVICE_TO_PC_TOPIC = UNIQUE_ID + "/device_to_pc"

# Load the WiFi and HiveMQ Cloud credentials from the file: secrets.py
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Connect to the configured WiFi network
print("\n\nAttempting to connect to WiFi: ", secrets["ssid"], "...")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets["ssid"], secrets["password"])
while True:
    if wlan.isconnected():
        break
    time.sleep(0.1)
print("\tConnected (probably?) to %s!\n" % secrets["ssid"])

# Set up the MQTT client.
mqtt_client = MQTTClient(
    client_id=UNIQUE_ID,
    server=secrets["broker"],
    user=secrets["mqtt_username"],
    password=secrets["mqtt_key"])


# Define what is to happen when a message is received
def on_message(topic, message):
    print("\tReceived a message:", message)


mqtt_client.set_callback(on_message)

# Connect to the Broker and Subscribe to the MQTT topic
mqtt_client.connect()
print("Connected to MQTT Broker: {}".format(secrets["broker"]))
mqtt_client.subscribe(PC_TO_DEVICE_TOPIC)

# Simulate sending sensor data to the Broker by sending random numbers.
counter = 0
loop_counter = 0
while True:
    mqtt_client.check_msg()  # Will cause on_message to run if a message has been received

    # Send a message (simulating sending sensor data):
    if counter >= 10:  # Send (publish) every 10 times through this loop
        counter = 0
        simulated_sensor_data = random.randint(1, 100)  # Simulate sensor data
        message_to_send = str(simulated_sensor_data)
        print("Sending (publishing) message:", message_to_send)
        mqtt_client.publish(DEVICE_TO_PC_TOPIC, message_to_send)

    time.sleep(0.3)  # Sleep a bit to safeguard against inundating the message-passing
    counter = counter + 1
    loop_counter = loop_counter + 1
    if loop_counter > 30:
        break

mqtt_client.disconnect()
print("Disconnected from MQTT broker: %s" % secrets["broker"])
