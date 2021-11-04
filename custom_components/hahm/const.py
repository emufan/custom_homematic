"""Constants."""

from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_HEAT,
    DEVICE_CLASS_MOISTURE,
    DEVICE_CLASS_MOTION,
    DEVICE_CLASS_OPENING,
    DEVICE_CLASS_PRESENCE,
    DEVICE_CLASS_PROBLEM,
    DEVICE_CLASS_SAFETY,
    DEVICE_CLASS_WINDOW,
)
from homeassistant.components.sensor import (
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLTAGE,
)
from homeassistant.const import ENTITY_CATEGORY_DIAGNOSTIC

DOMAIN = "hahm"

ATTR_INSTANCE_NAME = "instance_name"
ATTR_ADD_ANOTHER_INTERFACE = "add_another_interface"
ATTR_INTERFACE = "interface"
ATTR_INTERFACE_NAME = "interface_name"
ATTR_JSON_TLS = "json_tls"

SERVICE_VIRTUAL_KEY = "virtual_key"
SERVICE_RECONNECT = "reconnect"
SERVICE_SET_VARIABLE_VALUE = "set_variable_value"
SERVICE_SET_DEVICE_VALUE = "set_device_value"
SERVICE_SET_INSTALL_MODE = "set_install_mode"
SERVICE_PUT_PARAMSET = "put_paramset"

PARAMETER_BINARY_SENSOR_DEVICE_CLASSES = {
    "ALARMSTATE": DEVICE_CLASS_SAFETY,
    "DUTY_CYCLE": DEVICE_CLASS_PROBLEM,
    "HEATER_STATE": DEVICE_CLASS_HEAT,
    "LOW_BAT": DEVICE_CLASS_BATTERY,
    "LOWBAT": DEVICE_CLASS_BATTERY,
    "MOISTURE_DETECTED": DEVICE_CLASS_MOISTURE,
    "MOTION": DEVICE_CLASS_MOTION,
    "PRESENCE_DETECTION_STATE": DEVICE_CLASS_PRESENCE,
    "RAINING": DEVICE_CLASS_MOISTURE,
    "SABOTAGE": DEVICE_CLASS_SAFETY,
    "WATERLEVEL_DETECTED": DEVICE_CLASS_MOISTURE,
    "WINDOW_STATE": DEVICE_CLASS_WINDOW,
}

PARAMETER_SENSOR_DEVICE_CLASSES = {
    "ACTUAL_TEMPERATURE": DEVICE_CLASS_TEMPERATURE,
    "AVERAGE_ILLUMINATION": DEVICE_CLASS_ILLUMINANCE,
    "CARRIER_SENSE_LEVEL": DEVICE_CLASS_SIGNAL_STRENGTH,
    "CURRENT": DEVICE_CLASS_CURRENT,
    "CURRENT_ILLUMINATION": DEVICE_CLASS_ILLUMINANCE,
    "DUTY_CYCLE_LEVEL": DEVICE_CLASS_SIGNAL_STRENGTH,
    "ENERGY_COUNTER": DEVICE_CLASS_ENERGY,
    # "FREQUENCY",
    "HIGHEST_ILLUMINATION": DEVICE_CLASS_ILLUMINANCE,
    "HUMIDITY": DEVICE_CLASS_HUMIDITY,
    "ILLUMINATION": DEVICE_CLASS_ILLUMINANCE,
    "LOWEST_ILLUMINATION": DEVICE_CLASS_ILLUMINANCE,
    "OPERATING_VOLTAGE": DEVICE_CLASS_VOLTAGE,
    "POWER": DEVICE_CLASS_POWER,
    # "RAIN_COUNTER",
    "RSSI_DEVICE": DEVICE_CLASS_SIGNAL_STRENGTH,
    "RSSI_PEER": DEVICE_CLASS_SIGNAL_STRENGTH,
    "SET_POINT_TEMPERATURE": DEVICE_CLASS_TEMPERATURE,
    "SUNSHINEDURATION": DEVICE_CLASS_ILLUMINANCE,
    "VOLTAGE": DEVICE_CLASS_VOLTAGE,
    # "WIND_DIR",
    # "WIND_DIR_RANGE",
    # "WIND_SPEED",
}


PARAMETER_ENTITY_CATEGORIES = {
    "DUTY_CYCLE": ENTITY_CATEGORY_DIAGNOSTIC,
    "LOW_BAT": ENTITY_CATEGORY_DIAGNOSTIC,
    "LOWBAT": ENTITY_CATEGORY_DIAGNOSTIC,
    "OPERATING_VOLTAGE": ENTITY_CATEGORY_DIAGNOSTIC,
    "RSSI_DEVICE": ENTITY_CATEGORY_DIAGNOSTIC,
    "RSSI_PEER": ENTITY_CATEGORY_DIAGNOSTIC,
    "IP_ADDRESS": ENTITY_CATEGORY_DIAGNOSTIC,
    "SABOTAGE": ENTITY_CATEGORY_DIAGNOSTIC,
}
