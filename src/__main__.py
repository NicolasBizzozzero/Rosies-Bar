""" Main entry point of the software. """

import ast
import configparser
import signal
from pathlib import Path

from common import parse_path, every
from feeder import Feeder
from motor import MotorInterface

from logger import logger


def main():
    # Load configuration file
    config = configparser.ConfigParser()
    config.read(Path(__file__).parent.parent / "config.ini")

    # Initialize the feeder and check if it's feeding time every `checking_every` seconds.
    feeder = Feeder(
        feeding_hours=ast.literal_eval(config["parameters"]["feeding_hours"]),
        path_file_last_feed=parse_path(config["path"]["path_file_last_feed"]),
    )
    every(feeder.check_feeding_time, delay=int(config["parameters"]["checking_every"]))


if __name__ == "__main__":
    main()
