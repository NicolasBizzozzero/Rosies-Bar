import datetime
import os.path


def parse_path(path: str) -> str:
    if "{date}" in path:
        path = path.format(date=get_date_today())
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    return path

def get_date_today() -> str:
    """Returns today's date in a readable YYYY-MM-DD format. """
    return datetime.datetime.now().date().__str__()