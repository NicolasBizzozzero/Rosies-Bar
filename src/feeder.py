import ast
import datetime
import os.path
from zoneinfo import ZoneInfo

from logger import logger
from motor import MotorInterface


class Feeder:
    def __init__(self, feeding_hours: list[str], path_file_last_feed: str):
        logger.debug("Initialize Feeder")
        self.feeding_hours = self._typecast_feeding_hours(feeding_hours)
        self.path_file_last_feed = path_file_last_feed
        self.motor = MotorInterface()

        # Check that last time feed timestamp file as been created
        if not self._check_last_time_feed_timestamp_exists():
            logger.debug("First time starting feeder. Creating timestamp")
            self.feed()

    def feed(self):
        logger.info("Feeding [NOT IMPLEMENTED]")
        self._set_last_time_feed(date=datetime.datetime.now())

    def check_feeding_time(self):
        logger.debug("Checking if it is feeding time")
        last_time_feed = self._get_last_time_feed()
        next_feed_time = self._get_next_feed_time(last_time_feed)

        # hard set next feed time to 0 seconds
        next_feed_time = next_feed_time.replace(second=0, microsecond=0)

        current_time = datetime.datetime.now()
        if current_time >= next_feed_time:
            logger.info(
                f"Feeding time ! Current time : {current_time}, next feed time : {next_feed_time}"
            )
            self.feed()
        else:
            logger.info(
                f"Not feeding time yet. Current time : {current_time}, next feed time : {next_feed_time}"
            )

    def _get_last_time_feed(self) -> datetime.datetime:
        logger.debug("Retrieving last time feed")
        with open(self.path_file_last_feed) as fp:
            last_time_feed = fp.read()
            last_time_feed = last_time_feed.strip()

            return datetime.datetime.strptime(last_time_feed, "%Y-%m-%d %H:%M:%S.%f")

    def _set_last_time_feed(self, date: datetime.datetime):
        # Hard cast timedate to the max number of seconds and microseconds to correct a weird bug.
        date = date.replace(second=59, microsecond=99)

        logger.debug(f"Setting last time feed to {date}")
        with open(self.path_file_last_feed, "w") as fp:
            fp.write(date.__str__())

    def _get_next_feed_time(
        self, last_time_feed: datetime.datetime
    ) -> datetime.datetime:
        """Get the next feed time wrt. the last feed time and the given feeding hours."""
        # feeding_hours : ["08:00", "17:00"]
        # Cases :
        # last_time_feed : "23:59", 02 juin -> "08:00", 03 juin [Case 1]
        # last_time_feed : "07:59", 03 juin -> "08:00", 03 juin [Case 3, 08:00]
        # last_time_feed : "08:01", 03 juin -> "17:00", 03 juin [
        # last_time_feed : "16:59", 03 juin -> "17:00", 03 juin
        # last_time_feed : "17:01", 03 juin -> "08:00", 04 juin [Case 1 or 2]
        # last_time_feed : "00:01", 04 juin -> "08:00", 04 juin
        # last_time_feed : "17:00", 05 juin -> "08:00", 06 juin

        # Updates feeding hours with "now" data (except for the hours and minutes)
        now = datetime.datetime.now()
        for idx_feeding_hour in range(len(self.feeding_hours)):
            feeding_hour = self.feeding_hours[idx_feeding_hour]
            self.feeding_hours[idx_feeding_hour] = now
            self.feeding_hours[idx_feeding_hour] = self.feeding_hours[
                idx_feeding_hour
            ].replace(hour=feeding_hour.hour, minute=feeding_hour.minute)

        logger.debug(
            f"Finding in which case we are. feeding_hours={self.feeding_hours}, last_time_feed={last_time_feed} now={now}"
        )

        # Case 1 : If last feed time day < today, returns the first feed time hours
        if last_time_feed.day < now.day:
            logger.debug(f"Case 1")
            return self.feeding_hours[0]

        if last_time_feed.day == now.day:
            # Case 2 : Same day, last feed time > last feeding hour, then we return the first feeding hour tomorrow
            if last_time_feed > self.feeding_hours[-1]:
                logger.debug(f"Case 2")
                return self.feeding_hours[0] + datetime.timedelta(days=1)

            # Case 3 : Same day, checking between which hours we are
            for idx_feeding_hour in range(len(self.feeding_hours)):
                logger.debug(f"Case 3")
                if last_time_feed < self.feeding_hours[idx_feeding_hour]:
                    logger.debug(
                        f"last_time_feed < feeding_hour {self.feeding_hours[idx_feeding_hour]}"
                    )
                    return self.feeding_hours[idx_feeding_hour]
                elif last_time_feed >= self.feeding_hours[idx_feeding_hour]:
                    logger.debug(
                        f"last_time_feed >= feeding_hour {self.feeding_hours[idx_feeding_hour]}"
                    )
                    return self.feeding_hours[idx_feeding_hour + 1]

        # We should never reach this case
        raise ValueError(
            f"Not implemented case. now={now}, last_time_feed={last_time_feed}, feeding_hours={self.feeding_hours}"
        )

    def _check_last_time_feed_timestamp_exists(self) -> bool:
        return os.path.isfile(self.path_file_last_feed)

    @staticmethod
    def _typecast_feeding_hours(feeding_hours) -> list[datetime.datetime]:
        assert type(feeding_hours) is list
        assert all(type(hours) is str for hours in feeding_hours)
        assert all(len(hours) == 5 for hours in feeding_hours)

        now = datetime.datetime.now()
        new_feeding_hours = []
        for feeding_hour in feeding_hours:
            hours, minutes = feeding_hour.split(":")
            new_feeding_hours.append(
                datetime.datetime(
                    year=now.year,
                    month=now.month,
                    day=now.day,
                    hour=int(hours),
                    minute=int(minutes),
                )
            )
        return new_feeding_hours
