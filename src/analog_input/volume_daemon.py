#!/usr/bin/python3

import os
import pwd
import grp
import time

import logging
import logging.handlers
import argparse

from signal import signal, SIGINT, SIGTERM
from sys import exit
from mcp3008 import MCP3008
from analog_in import AnalogIn

mcp = MCP3008(0, 1)

mcp.open()

chan0 = AnalogIn(mcp, 0)

last_read = 0       
tolerance = 100

volume_last = 0
vol_step = 2

max_adc = 65472 # 65535
min_adc = 0

# Deafults
DEFAULT_SHUTDOWN_VOL = 'mute'
LOG_FILENAME = "/var/log/volume-control.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

def drop_privileges(uid_name='nobody', gid_name='nogroup'):
    if os.getuid() != 0:
        # We're not root so, like, whatever dude
        return
    # Get the uid/gid from the name
    running_uid = pwd.getpwnam(uid_name).pw_uid
    running_gid = grp.getgrnam(gid_name).gr_gid
    # Reset group access list
    os.initgroups(uid_name, running_gid)
    # Try setting the new uid/gid
    os.setgid(running_gid)
    os.setuid(running_uid)
    # Ensure a very conservative umask
    mask = int('077', 8)
    old_umask = os.umask(mask)

def get_shutdown_handler(message=None):
    """
    Build a shutdown handler, called from the signal methods
    :param message:
        The message to show on the second line of the LCD, if any. Defaults to None
    """
    def handler(signum, frame):
        # If we want to do anything on shutdown, such as stop motors on a robot,
        # you can add it here.
        logger.info("Shutdown: Set volume to {}".format(DEFAULT_SHUTDOWN_VOL))
        set_vol_cmd = 'volumio volume {}'.format(DEFAULT_SHUTDOWN_VOL)
        os.system(set_vol_cmd)
        mcp.close()
        exit(0)
    return handler

# Do anything you need to do before changing to the 'volumio' user (our service
# script will run as root initially so we can do things like bind to low
# number network ports or memory map GPIO pins)
# Become 'volumio' to avoid running as root
drop_privileges(uid_name='volumio', gid_name='volumio')

def remap_range(value, left_min, left_max, right_min, right_max):
    # this remaps a value from original (left) range to new (right) range
    # Figure out how 'wide' each range is
    left_span = left_max - left_min
    right_span = right_max - right_min
 
    # Convert the left range into a 0-1 range (int)
    valueScaled = int(value - left_min) / int(left_span)
 
    # Convert the 0-1 range into a value in the right range.
    return int(right_min + (valueScaled * right_span))

if __name__ == '__main__':

    signal(SIGINT, get_shutdown_handler('SIGINT received'))
    signal(SIGTERM, get_shutdown_handler('SIGTERM received'))

    # Define and parse command line arguments
    parser = argparse.ArgumentParser(description="Analog volume control python service")
    parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")

    # If the log file is specified on the command line then override the default
    args = parser.parse_args()
    if args.log:
            LOG_FILENAME = args.log

    # Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
    # Give the logger a unique name (good practice)
    logger = logging.getLogger(__name__)
    # Set the log level to LOG_LEVEL
    logger.setLevel(LOG_LEVEL)
    # Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
    handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
    # Format each log message like this
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    # Attach the formatter to the handler
    handler.setFormatter(formatter)
    # Attach the handler to the logger
    logger.addHandler(handler)

    while True:
        trim_pot = chan0.value
        pot_adjust = abs(trim_pot - last_read)
        if pot_adjust > tolerance:
            # convert 16bit adc0 (0-65535) trim pot read into 0-100 volume level
            set_volume = remap_range(trim_pot, max_adc, 0, 0, 100)
            logger.debug('Volume = {volume}%' .format(volume = set_volume)) 
            if (set_volume % vol_step) == 0:
                logger.info('Change volume to  {volume}%' .format(volume = set_volume)) 
                set_vol_cmd = 'volumio volume {volume}'.format(volume = set_volume)
                import os
                os.system(set_vol_cmd)
            # save the potentiometer reading for the next loop
            last_read = trim_pot
        time.sleep(0.5)