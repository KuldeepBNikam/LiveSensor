from sensor.exception import SensorException
import os
import sys

from sensor.logger import logging

def test_exception():
    try:
        logging.info("We'll get one error by division by zero")
        a=1/0
    except Exception as e:
        raise SensorException(e,sys)
       


if __name__ == "__main__":    #ensures some codes only runs when file is executed not imported
    try:
        test_exception()
    except Exception as e:
        print(e)
