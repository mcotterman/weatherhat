# Kevin McAleer 
# 18 February 2022
# This enables data from the Pimoroni WeatherHat to be sent to a local MQTT server

import weatherhat
import paho.mqtt.client as mqtt
from time import sleep
from datetime import datetime
import os
from dotenv import load_dotenv
import socket

load_dotenv()

mqtt_server = os.getenv('MQTT_SERVER')
mqtt_port = int(os.getenv('MQTT_PORT'))
mqtt_username = os.getenv('MQTT_USERNAME')
mqtt_password = os.getenv('MQTT_PASSWORD')
mqtt_topic = os.getenv('MQTT_TOPIC')

client_id = "weatherhat"

update_frequency_in_seconds = int(os.getenv('WEATHER_UPDATE_FREQ'))

sensor = weatherhat.WeatherHAT()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.mqtt_topic+" "+str(msg.payload))

client = mqtt.Client(client_id=client_id)
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(mqtt_server, mqtt_port)

payload = "{something:true}"

# Wait until the network is and host name resolution is available:

def hostAvail(hostname):
    try:
        socket.gethostbyname(hostname)
        return True
    except socket.error:
        return False
    return False

while not hostAvail(mqtt_server):
    print(f"Waiting for {mqtt_server}")
    sleep(2)

# Continue with code here...

while True:

    # update the sensor readings
    sensor.update(interval=1.0)
    
    # sleep for update frequency second 
    sleep(update_frequency_in_seconds)

    # build the payload
    now = datetime.now()
    payload = f'{{"datetime":{datetime.timestamp(now)}, "temperature":{sensor.temperature}, \
              "pressure":{sensor.pressure}, \
              "humidity":{sensor.humidity}, \
              "relative_humidity": {sensor.relative_humidity}, \
              "dewpoint":{sensor.dewpoint}, \
              "light":{sensor.lux}, \
              "wind_direction": {sensor.wind_direction}, \
              "wind_speed":{sensor.wind_speed}, \
              "rain": {sensor.rain}, \
              "rain_total":{sensor.rain_total} }}'
    client.publish(topic=mqtt_topic, payload=payload, qos=0, retain=False)
    print(f"sending {payload} to {mqtt_server}")