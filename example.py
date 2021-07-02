from time import sleep
from d6fd010a32 import D6FD010A32, SlaveAddress, BaudRate


flow_sensor = D6FD010A32(com_port='/dev/ttyUSB0', slave_address=SlaveAddress.ADDRESS1,
                         baudrate=BaudRate.BPS38400, sampling_period=1)

while True:
    print(flow_sensor.get_measurement())
    sleep(1)
