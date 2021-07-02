import sys
import logging
import threading
import minimalmodbus
from os import path
from time import sleep
from typing import Final
from queue import Queue
from datetime import datetime


class BaudRate:

    BPS38400: Final[int] = 38400
    BPS9600: Final[int] = 9600


class SlaveAddress:

    ADDRESS1: Final[int] = 1
    ADDRESS2: Final[int] = 2
    ADDRESS3: Final[int] = 3
    ADDRESS4: Final[int] = 4
    ADDRESS5: Final[int] = 5
    ADDRESS6: Final[int] = 6
    ADDRESS7: Final[int] = 7
    ADDRESS8: Final[int] = 8
    ADDRESS9: Final[int] = 9
    ADDRESS10: Final[int] = 10
    ADDRESS11: Final[int] = 11
    ADDRESS12: Final[int] = 12
    ADDRESS13: Final[int] = 13
    ADDRESS14: Final[int] = 14
    ADDRESS15: Final[int] = 15
    ADDRESS16: Final[int] = 16
    ADDRESS17: Final[int] = 17
    ADDRESS18: Final[int] = 18
    ADDRESS19: Final[int] = 19
    ADDRESS20: Final[int] = 20
    ADDRESS21: Final[int] = 21
    ADDRESS22: Final[int] = 22
    ADDRESS23: Final[int] = 23
    ADDRESS24: Final[int] = 24
    ADDRESS25: Final[int] = 25
    ADDRESS26: Final[int] = 26
    ADDRESS27: Final[int] = 27
    ADDRESS28: Final[int] = 28
    ADDRESS29: Final[int] = 29
    ADDRESS30: Final[int] = 30
    ADDRESS31: Final[int] = 31
    ADDRESS32: Final[int] = 32


class D6FD010A32:

    BYTE_SIZE = 8
    STOP_BIT = 1
    TIMEOUT = 1
    ADDRESS_MIN = 1
    ADDRESS_MAX = 32
    TOTAL_REGISTER_COUNT = 14

    FUNC_READ_HOLDING_REGISTERS = 3

    def __init__(self, com_port: str, slave_address: SlaveAddress, baudrate: BaudRate, samping_period: int = 1, logger: str = None):
        self.logger = None
        if logger:
            self.logger = logging.getLogger(logger)
        self.com_port = com_port
        self.slave_address = slave_address
        self.baudrate = baudrate
        self.sampling_period = samping_period
        self.__data = Queue(maxsize=20)
        self._parameter_check()
        self._initialize_modbus()
        self._run()

    def _initialize_modbus(self):
        self.__instrument = minimalmodbus.Instrument(
            self.com_port, self.slave_address)
        self.__instrument.serial.baudrate = self.baudrate
        self.__instrument.serial.bytesize = self.BYTE_SIZE
        self.__instrument.serial.stopbits = self.STOP_BIT
        self.__instrument.serial.timeout = self.TIMEOUT
        self.__instrument.serial.parity = minimalmodbus.serial.PARITY_NONE

    def _com_port_check(self) -> bool:
        try:
            # type check
            if type(self.com_port) is not str:
                raise TypeError(
                    f"Argument 'com_port' has incompatible type '{type(self.baudrate).__name__}'; expected 'str'")

            # port check
            if not path.exists(self.com_port):
                raise ValueError(
                    f"COM port '{self.com_port}' is not connected")

            return True

        except Exception as e:
            if self.logger:
                self.logger.warning(f"{type(e).__name__}: {e}")
            else:
                print(f"{type(e).__name__}: {e}")
            return False

    def _baudrate_check(self) -> bool:
        try:
            # type check
            if type(self.slave_address) is not int:
                raise TypeError(
                    f"Argument 'baudrate' has incompatible type '{type(self.baudrate).__name__}'; expected 'int'")

            # value check
            if self.baudrate != self.BAUDRATE_38400 and self.baudrate != self.BAUDRATE_9600:
                raise ValueError(
                    f"Value of argument 'baudrate' is invalid. Valid baudrate are {self.BAUDRATE_9600} and {self.BAUDRATE_38400}")

            return True

        except Exception as e:
            if self.logger:
                self.logger.warning(f"{type(e).__name__}: {e}")
            else:
                print(f"{type(e).__name__}: {e}")
            return False

    def _slave_address_check(self) -> bool:
        try:
            # type check
            if type(self.slave_address) is not int:
                raise TypeError(
                    f"Argument 'slave_address' has incompatible type '{type(self.slave_address).__name__}'; expected 'int'")

            # value check
            if self.slave_address not in range(self.ADDRESS_MIN, self.ADDRESS_MAX+1):
                raise IndexError(
                    f"Argument 'slave_address' is not in range. Valid address range is from {self.ADDRESS_MIN} to {self.ADDRESS_MAX}")

            return True

        except Exception as e:
            if self.logger:
                self.logger.warning(f"{type(e).__name__}: {e}")
            else:
                print(f"{type(e).__name__}: {e}")
            return False

    def _parameter_check(self) -> bool:
        if not all(
            [self._com_port_check(),
             self._baudrate_check(),
             self._slave_address_check()]):
            sys.exit()

    def _convert_int_to_signed_16bit(self, value: int) -> int:
        return -(0xFFFF - value) if value > 0x7FFF else value

    def _read_sensor_data(self):
        while True:
            try:
                raw_data = self.__instrument.read_registers(
                    self.slave_address - 1, self.TOTAL_REGISTER_COUNT, self.FUNC_READ_HOLDING_REGISTERS)

                if self.__data.full():
                    self.__data.get()

                self.__data.put({
                    "sensor_data": {
                        "ins_velocity_x": self._convert_int_to_signed_16bit(raw_data[0]) / 1000,
                        "ins_velocity_y": self._convert_int_to_signed_16bit(raw_data[1]) / 1000,
                        "ave_velocity_x": self._convert_int_to_signed_16bit(raw_data[2]) / 1000,
                        "ave_velocity_y": self._convert_int_to_signed_16bit(raw_data[3]) / 1000,
                        "max_velocity_x": self._convert_int_to_signed_16bit(raw_data[4]) / 1000,
                        "max_velocity_y": self._convert_int_to_signed_16bit(raw_data[5]) / 1000,
                        "min_velocity_x": self._convert_int_to_signed_16bit(raw_data[6]) / 1000,
                        "min_velocity_y": self._convert_int_to_signed_16bit(raw_data[7]) / 1000,
                        "ins_velocity": raw_data[8] / 1000,
                        "ins_angle": raw_data[9] / 100,
                        "ave_velocity": raw_data[10] / 1000,
                        "ave_angle": raw_data[11] / 100,
                        "max_velocity": raw_data[12] / 1000,
                        "min_velocity": raw_data[13] / 1000,
                        "velocity_unit": "m/s",
                        "angle_unit": "degrees"
                    },
                    "timestamp": int(datetime.utcnow().timestamp())
                })

            except KeyboardInterrupt:
                sys.exit()

            except Exception as e:
                if self.logger:
                    self.logger.warning(f"{type(e).__name__}: {e}")
                else:
                    print(f"{type(e).__name__}: {e}")

            finally:
                sleep(self.sampling_period)

    def get_measurement(self) -> dict:
        if self.__data.empty():
            return {}

        return self.__data.get()

    def _run(self):
        threading.Thread(target=self._read_sensor_data, daemon=True).start()
