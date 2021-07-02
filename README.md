# Omron-D6F

## Introduction

Python-based driver for [Omron D6F-D010A32-00](https://components.omron.com/product-detail?partNumber=D6F-D) MEMS 2-axis flow sensor. Tested on Raspberry Pi 3B+/4B  

### Wiring

Serial converter cable, such as [FTDI USB-RS485-WE](https://ftdichip.com/products/usb-rs485-we-1800-bt/) is required to communicate with Omron D6F-D010A32-00. The cable end has to be joined with ethernet cable to fit RJ-45 port on sensor body.  
Please refer table below for wire mapping.

| RJ-45 Connector | Color | RS485 Interface | FTDI Wire Color |
| :---: | :---: | :---: | :---: |
| Pin 1 | white/orange | VCC | red |
| Pin 2 | orange | GND | black |
| Pin 3 | white/green | NC | |
| Pin 4 | blue | B (Data -) | yellow |
| Pin 5 | white/blue | A (Data +) | orange |
| Pin 6 | green | NC | |
| Pin 7 | white/brown | GND | black |
| Pin 8 | brown | VCC | red |

### Example

```python
from time import sleep
from d6fd010a32 import D6FD010A32, SlaveAddress, BaudRate


flow_sensor = D6FD010A32(com_port='/dev/ttyUSB0', slave_address=SlaveAddress.ADDRESS1,
                         baudrate=BaudRate.BPS38400, sampling_period=1)
                         
while True:
    print(flow_sensor.get_measurement())
    sleep(1)
```

### Output data format  

```none
{
    "sensor_data": {
        "ins_velocity_x": <class 'float'>, // instantaneous velocity (x-axis)
        "ins_velocity_y": <class 'float'>, // instantaneous velocity (y-axis)
        "ave_velocity_x": <class 'float'>, // average velocity (x-axis)
        "ave_velocity_y": <class 'float'>, // average velocity (y-axis)
        "max_velocity_x": <class 'float'>, // max velocity (x-axis)
        "max_velocity_y": <class 'float'>, // max velocity (y-axis)
        "min_velocity_x": <class 'float'>, // min velocity (x-axis)
        "min_velocity_y": <class 'float'>, // min velocity (y-axis)
        "ins_velocity": <class 'float'>, // instantaneous velocity (combination of both axes)
        "ins_angle": <class 'float'>, // instantaneous angle
        "ave_velocity": <class 'float'>, // average velocity (combination of both axes)
        "ave_angle": <class 'float'>, // average angle
        "max_velocity": <class 'float'>, // maximum velocity (combination of both axes)
        "min_velocity": <class 'float'>, // minimum velocity (combination of both axes)
        "velocity_unit": "m/s",
        "angle_unit": "degrees"
    },
    "timestamp": <class 'int'> // UTC timestamp in seconds
}
```

### Dependencies

* `minimalmodbus`

```
pip install minimalmodbus
```

### Todo

* Read multiple (daisy-chained) sensors  
