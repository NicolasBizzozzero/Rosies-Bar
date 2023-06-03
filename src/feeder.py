import ast
import datetime
import os.path

from logger import logger


class Feeder:
    def __init__(self, motor, path_file_last_feed: str):
        logger.info("Initialize Feeder")
        self.motor = motor
        self.path_file_last_feed = path_file_last_feed

        # Check that last time feed timestamp file as been created
        if not os.path.isfile(self.path_file_last_feed):
            self.feed()
            self._set_last_time_feed(date=datetime.datetime.now())

    def feed(self):
        pass

    def _get_last_time_feed(self) -> datetime.datetime:
        with open(self.path_file_last_feed) as fp:
            last_time_feed = fp.read()
            last_time_feed = last_time_feed.strip()
            return ast.literal_eval(last_time_feed)

    def _set_last_time_feed(self, date: datetime.datetime):
        with open(self.path_file_last_feed, "w") as fp:
            fp.write(date.__str__())
