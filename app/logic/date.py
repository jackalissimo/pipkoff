from datetime import datetime, timedelta
from dateutil import parser as dparser


def date_format(datetime_: datetime) -> str:
    """
    :return: str date acceptable by tinkoff api
    """
    tzinfo = datetime_.tzinfo
    if tzinfo:
        z = datetime_.strftime('%z')
        tz_h = z[:-2]
        tz_m = z[-2:]
        shift = "{0}:{1}".format(tz_h, tz_m)
    else:
        shift = '+03:00'
    return datetime_.strftime("%Y-%m-%dT%H:%M:%S{0}".format(shift))


def get_date_from(date_to: str, interval: str) -> str:
    dt2 = dparser.parse(date_to)
    delta = get_timedelta(interval)
    dt1 = dt2 - delta
    return date_format(dt1)


def get_timedelta(interval: str):
    if interval == 'hour':
        return timedelta(hours=7 * 24)
    elif interval == 'day':
        return timedelta(days=90)
    elif interval == 'week':
        return timedelta(weeks=104)
    elif interval == 'month':
        return timedelta(weeks=150)
    elif interval == '30min':
        return timedelta(hours=24)
    elif interval == '15min' or interval == '10min':
        return timedelta(hours=24)
    elif interval == '5min' or interval == '3min':
        return timedelta(hours=12)
    elif interval == '1min' or interval == '2min':
        return timedelta(hours=4)
    else:
        return timedelta(days=7)


def get_from_to_intervals(interval: str, dt_from: datetime, dt_to: datetime) -> list:
    """
    :return: [(from_N, to_N), ...], where from_N, to_N - str acceptable by tinkoff api
    """
    if dt_from.timestamp() >= dt_to.timestamp():
        return []
    delta = get_timedelta(interval)
    end = dt_to
    start = get_startpoint(end - delta, dt_from)
    res = []
    res.append((date_format(start), date_format(end)))
    while start.timestamp() > dt_from.timestamp():
        end = start
        start = get_startpoint(end - delta, dt_from)
        res.append((date_format(start), date_format(end)))
    return res

def get_startpoint(dt0, dt_from):
    if dt0.timestamp() > dt_from.timestamp():
        return dt0
    else:
        return dt_from
