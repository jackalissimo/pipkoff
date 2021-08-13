from datetime import datetime


def date_format(datetime_: datetime, shift='+03:00'):
    return datetime_.strftime("%Y-%m-%dT%H:%M:%S{0}".format(shift))
