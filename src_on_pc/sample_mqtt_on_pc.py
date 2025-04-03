"""
Example showing for tkinter and ttk:
  -- MQTT for communicating with another device through the Internet.

Authors: David Mutchler and his colleagues
         at Rose-Hulman Institute of Technology.
"""

import tkinter
from tkinter import ttk
import mqtt_helper_pc


def main():
    # -------------------------------------------------------------------------
    # Root (main) window and Frame on it.
    # -------------------------------------------------------------------------
    root = tkinter.Tk()
    root.title("MQTT example")
    frame = ttk.Frame(root)
    frame.grid()

    # -------------------------------------------------------------------------
    # mqtt object, properly initialized.
    # -------------------------------------------------------------------------
    mqtt_client = mqtt_helper_pc.MyMqttClient()  # NEED THIS!

    # -------------------------------------------------------------------------
    # Entry box with data to send to the other computer.
    # Button that sends data in the Entry box to the other computer.
    # Label to simulate receiving data from the other computer.
    # -------------------------------------------------------------------------
    entry = ttk.Entry(frame)
    entry.grid()

    # NEED SOMETHING LIKE THE FOLLOWING to send information to the Pico.
    button = ttk.Button(frame, text="Send Entry box data to the other computer")
    button.grid()
    button["command"] = lambda: mqtt_helper_pc.send_contents_of_entry_box_via_mqtt(
        entry, mqtt_client
    )

    # NEED SOMETHING LIKE THE FOLLOWING to display information from the Pico.
    label = ttk.Label(frame, text="No data yet")
    label.grid()
    mqtt_client.label_for_message_from_device = label

    # -------------------------------------------------------------------------
    # Stay in the event loop for the rest of the program's run, as usual.
    # -------------------------------------------------------------------------
    root.mainloop()


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()
