# -*- coding: utf-8 -*-
import pytz

from datetime import datetime


TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


def loads(s, timezone=None):
    if timezone is None:
        timezone = pytz.utc
    return datetime.strptime(s, TIMESTAMP_FORMAT).replace(tzinfo=timezone)


def dumps(timestamp):
    if timestamp.tzinfo:
        timestamp = timestamp.astimezone(pytz.utc)
    return timestamp.strftime(TIMESTAMP_FORMAT)
