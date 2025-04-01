"""
Code for a PC to communicate with another device through MQTT.
Use verbatim except where TODO's indicate.
"""

import paho.mqtt.client

UNIQUE_ID = "DavidMutchler1019"  # TODO: Use something no one else will use

PC_TO_DEVICE_TOPIC = UNIQUE_ID + "/pc_to_device"
DEVICE_TO_PC_TOPIC = UNIQUE_ID + "/device_to_pc"

# TODO: Un-comment if you want to communicate from PC Run 2 to PC Run 1
# PC_TO_DEVICE_TOPIC = UNIQUE_ID + "/device_to_pc"
# DEVICE_TO_PC_TOPIC = UNIQUE_ID + "/pc_to_device"

BROKER = "broker.emqx.io"  # Or: "broker.hivemq.com", but must match Pico
TCP_PORT = 1883


class MyMqttClient(paho.mqtt.client.Client):
    def __init__(self):
        super().__init__(paho.mqtt.client.CallbackAPIVersion.VERSION2)
        self.on_connect = on_connect
        self.on_subscribe = on_subscribe
        self.on_message = on_message

        # ---------------------------------------------------------------------
        # TODO: Put your GUI items here as needed, all set to None
        # ---------------------------------------------------------------------
        self.label_for_message_from_device = None  # Set later

        print("Connecting to the broker...")
        self.connect(BROKER, TCP_PORT)
        self.loop_start()
        self.subscribe(DEVICE_TO_PC_TOPIC)


def on_connect(mqtt_client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"CONNECTED to MQTT broker {BROKER}")
    else:
        print("Failed to connect to broker, return code %d\n", reason_code)


def on_subscribe(client, userdata, mid, reason_code_list, properties):
    if reason_code_list[0].is_failure:
        print(f"Broker rejected your subscription: {reason_code_list[0]}")
    else:
        print(f"Broker granted quality-of-service (QoS): {reason_code_list[0].value}")
        print(f"SUBSCRIBED to {DEVICE_TO_PC_TOPIC}")
        print(f"PUBLISHING to {PC_TO_DEVICE_TOPIC}")


def on_message(mqtt_client, userdata, message_packet):
    """Called when a message arrives.  Display it on Console and in GUI."""
    message = message_packet.payload.decode()
    print("Received message:", message)  # Show on the Console

    # -------------------------------------------------------------------------
    # TODO: Modify as needed for your GUI
    # -------------------------------------------------------------------------
    mqtt_client.label_for_message_from_device["text"] = message  # Show in GUI


# -----------------------------------------------------------------------------
# TODO: CALL (do NOT modify) as needed for your GUI
# -----------------------------------------------------------------------------
def send_via_mqtt(message, mqtt_client):
    """Publish (send to other device) the given string."""
    print("Sending", message)  # For debugging, as needed
    mqtt_client.publish(PC_TO_DEVICE_TOPIC, message)


# -----------------------------------------------------------------------------
# TODO: Replace/augment as needed for your GUI
# -----------------------------------------------------------------------------
def send_contents_of_entry_box_via_mqtt(entry, mqtt_client):
    """Publish (send to other device) the string in the given ttk.Entry."""
    message = entry.get()
    send_via_mqtt(message, mqtt_client)
