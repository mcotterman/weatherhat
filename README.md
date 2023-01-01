# STILL IN DEVELOPMENT AND NOT CONFIRMED WORKING

# WeatherHat MQTT Sample
Forked from [kevinmcaleer](https://github.com/kevinmcaleer/weatherhat_to_mqtt)

This is a sample of using an MQTT broker to collect information in from the [Pimoroni Weather Hat](https://shop.pimoroni.com/products/weather-hat). In Kevin's example he is using Grafana with the MQTT plugin.

## My Plan:
* Sensor setup: An RPi Zero W attached to the weatherhat.
* Consumer: RPi 4 8GB attached to a 10 inch touchscreen running
    * [Mosquitto MQTT broker](https://mosquitto.org/)
    * [Graphana](https://grafana.com/)

## My Changes
* Remove the hard coded information from the script into a .env file

### Sample .env file:
```
MQTT_SERVER=weatherdisplay
MQTT_PORT=1883
MQTT_USERNAME=weather
MQTT_PASSWORD=weatherpassword
MQTT_TOPIC=weather/data
WEATHER_UPDATE_FREQ=30
```

### Required Libraries:
Install the following libraries with pip3:
* weatherhat
* python-dotenv
* paho-mqtt