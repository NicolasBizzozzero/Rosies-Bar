import datetime
import functools
import os.path
import sys
import time
import traceback
from zoneinfo import ZoneInfo


def parse_path(path: str) -> str:
    if "{date}" in path:
        path = path.format(date=get_date_today())
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    return path


def get_date_today() -> str:
    """Returns today's date in a readable YYYY-MM-DD format."""
    return datetime.datetime.now().date().__str__()


def utctime_to_localtime(utc_time: datetime.datetime) -> datetime.datetime:
    utctime = utc_time.replace(tzinfo=ZoneInfo("UTC"))
    return utctime.astimezone(ZoneInfo("localtime"))


def signal_handler_exit(signal, frame):
    sys.exit(0)


def catch_all_exceptions(function):
    """Decorator catching all exceptions occurring during the function execution and logging their stacktrace.
    Logging them as warning to not halt the whole software process.
    """

    from logger import logger

    @functools.wraps(function)
    def wrapper(*arg, **kwargs):
        try:
            function(*arg, **kwargs)
        except Exception as exception:
            logger.warning(
                f'Exception "{type(exception).__name__}" caught :\n{traceback.format_exc()}'
            )

    return wrapper


@catch_all_exceptions
def every(function: callable, delay):
    """Call a function every `delay` seconds.

    This solution combines several features:
      * Exception handling: As far as possible on this level, exceptions are handled properly, i.e. get logged for
      debugging purposes without aborting our program.
      * No chaining: The common chain-like implementation (for scheduling the next event) you find in many answers is
      brittle in the aspect that if anything goes wrong within the scheduling mechanism (threading.Timer or whatever),
      this will terminate the chain. No further executions will happen then, even if the reason of the problem is
      already fixed. A simple loop and waiting with a simple sleep() is much more robust in comparison.
      * No drift: My solution keeps an exact track of the times it is supposed to run at. There is no drift depending on
      the execution time (as in many other solutions).
      * Skipping: My solution will skip tasks if one execution took too much time (e. g. do X every five seconds, but X
      took 6 seconds). This is the standard cron behavior (and for a good reason). Many other solutions then simply
      execute the task several times in a row without any delay. For most cases (e. g. cleanup tasks) this is not
      wished. If it is wished, simply use next_time += delay instead.

    Source:
      * https://stackoverflow.com/a/49801719
    """

    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        function()

        # skip tasks if we are behind schedule:
        next_time += (time.time() - next_time) // delay * delay + delay
