from datetime import datetime


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
