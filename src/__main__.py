import configparser
from pathlib import Path

from common import parse_path
from feeder import Feeder
from motor import MotorInterface

from logger import logger


def main():
    # Load config file
    config = configparser.ConfigParser()
    config.read(Path(__file__).parent.parent / "config.ini")

    # Setup paths
    path_file_log = parse_path(config["logging"]["path_file_log"])
    path_file_last_feed = parse_path(config["path"]["path_file_last_feed"])

    motor = MotorInterface()
    feeder = Feeder(motor=motor, path_file_last_feed=path_file_last_feed)


if __name__ == "__main__":
    main()
