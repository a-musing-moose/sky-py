# -*- coding: utf-8 -*-
import pytz

from unittest import TestCase
from datetime import datetime

from sky import timestamp


class TestDatetimeMarshalling(TestCase):

    def setUp(self):
        self.dt = datetime(
            year=2014,
            month=2,
            day=21,
            hour=10,
            minute=10,
            second=23,
            microsecond=203,
        )
        self.dts = '2014-02-21T10:10:23.000203Z'

    def test_dumps_of_naive_datetime(self):
        s = timestamp.dumps(self.dt)
        self.assertEquals(s, self.dts)

    def test_dumps_of_aware_datetime(self):
        utc_date = self.dt.replace(tzinfo=pytz.utc)
        local = pytz.timezone('Australia/Melbourne')
        local_dt = utc_date.astimezone(local)
        s = timestamp.dumps(local_dt)
        self.assertEquals(s, self.dts)

    def test_loads_with_no_timezone(self):
        utc_date = self.dt.replace(tzinfo=pytz.utc)
        dt = timestamp.loads(self.dts)
        self.assertEquals(dt, utc_date)

    def test_loads_with_with_timezone(self):
        tz = pytz.timezone('Australia/Melbourne')
        local_dt = self.dt.replace(tzinfo=tz)
        dt = timestamp.loads(self.dts, tz)
        self.assertEquals(dt, local_dt)
