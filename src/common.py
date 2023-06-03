import datetime
import os.path
import time
import traceback


def parse_path(path: str) -> str:
    if "{date}" in path:
        path = path.format(date=get_date_today())
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    return path


def get_date_today() -> str:
    """Returns today's date in a readable YYYY-MM-DD format."""
    return datetime.datetime.now().date().__str__()


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
        try:
            function()
        except Exception:
            traceback.print_exc()
            # in production code you might want to have this instead of course:
            # logger.exception("Problem while executing repetitive task.")
        # skip tasks if we are behind schedule:
        next_time += (time.time() - next_time) // delay * delay + delay
