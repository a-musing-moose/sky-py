# -*- coding: utf-8 -*-
import pytz

from datetime import datetime
from unittest import TestCase
from mock import Mock, patch

from sky import resources


class TestEvent(TestCase):

    def setUp(self):
        self.dt = datetime(
            year=2014,
            month=2,
            day=21,
            hour=10,
            minute=10,
            second=23,
            microsecond=203,
            tzinfo=pytz.utc
        )
        self.dts = "2014-02-21T10:10:23.000203Z"

    def test_from_dict_no_data(self):
        obj = {
            'timestamp': self.dts,
            'data': {
                'num': 123,
                'fake': 'data'
            }
        }
        event = resources.Event()
        event.from_dict(obj)
        self.assertEquals(event.timestamp, self.dt)
        self.assertEquals(event.data, obj['data'])

    def test_from_dict_with_no_timestamp(self):
        obj = {
            'data': {
                'num': 123,
                'fake': 'data'
            }
        }
        event = resources.Event()
        event.from_dict(obj)
        self.assertIsNotNone(event.timestamp)
        self.assertEquals(event.data, obj['data'])

    def test_to_dict(self):
        event = resources.Event(data={}, timestamp=self.dt)
        obj = event.to_dict()
        self.assertEquals(obj['data'], {})
        self.assertEquals(obj['timestamp'], self.dts)

    @patch('sky.resources.datetime')
    def test_timestamp_default_to_now(self, mock_dt):
        mock_dt.utcnow = Mock(return_value=self.dt)
        event = resources.Event()
        self.assertEquals(event.timestamp, self.dt)


class TestProperty(TestCase):

    def test_from_dict(self):
        obj = {
            'id': 23,
            'name': 'username',
            'transient': True,
            'data_type': 'string',
        }
        prop = resources.Property()
        prop.from_dict(obj)
        self.assertEquals(prop.object_id, 23)
        self.assertEquals(prop.name, 'username')
        self.assertTrue(prop.transient)
        self.assertEquals(prop.data_type, 'string')

    def test_to_dict(self):
        prop = resources.Property(
            property_id=13,
            name='age',
            transient=False,
            data_type='integer'
        )
        obj = prop.to_dict()
        self.assertEquals(obj['id'], 13)
        self.assertEquals(obj['name'], 'age')
        self.assertFalse(obj['transient'])
        self.assertEquals(obj['data_type'], 'integer')

    def test_only_accepts_valid_data_types(self):
        with self.assertRaises(ValueError):
            resources.Property(data_type='custard')


class TestTable(TestCase):

    def setUp(self):
        self.dt = datetime(
            year=2014,
            month=2,
            day=21,
            hour=10,
            minute=10,
            second=23,
            microsecond=203,
            tzinfo=pytz.utc
        )
        self.dts = "2014-02-21T10:10:23.000203Z"

    def test_to_dict(self):
        table = resources.Table(client=None, name='test_table')
        expected = {
            'name': 'test_table'
        }
        self.assertEquals(table.to_dict(), expected)

    def test_from_dict(self):
        obj = {
            'name': 'test_table'
        }
        table = resources.Table().from_dict(obj)
        self.assertEquals(table.name, obj['name'])

    def test_properties(self):
        client = Mock()
        client.get_properties = Mock(return_value=[])
        table = resources.Table(name='test', client=client)
        table.get_properties()
        client.get_properties.assert_called_once_with(table)

    def test_get_property(self):
        client = Mock()
        client.get_property = Mock(return_value={})
        table = resources.Table(name='test', client=client)
        table.get_property('test-prop')
        client.get_property.assert_called_once_with(table, 'test-prop')

    def test_create_property(self):
        client = Mock()
        client.create_property = Mock(return_value={})
        table = resources.Table(name='test', client=client)
        prop = resources.Property(name='test-prop')
        table.create_property(prop)
        client.create_property.assert_called_once_with(table, prop)

    def test_update_property(self):
        client = Mock()
        client.update_property = Mock(return_value={})
        table = resources.Table(name='test', client=client)
        prop = resources.Property(name='test-prop')
        table.update_property('test-prop', prop)
        client.update_property.assert_called_once_with(
            table,
            'test-prop',
            prop
        )

    def test_delete_property(self):
        client = Mock()
        client.delete_property = Mock(return_value=None)
        table = resources.Table(name='test', client=client)
        prop = resources.Property(name='test-prop')
        table.delete_property(prop)
        client.delete_property.assert_called_once_with(
            table,
            prop
        )

    def test_get_events(self):
        client = Mock()
        client.get_events = Mock(return_value=[])
        table = resources.Table(name='test', client=client)
        table.get_events(123)
        client.get_events.assert_called_once_with(table, 123)

    def test_get_event(self):
        client = Mock()
        client.get_event = Mock(return_value={})
        table = resources.Table(name='test', client=client)
        table.get_event(123, self.dts)
        client.get_event.assert_called_once_with(
            table,
            123,
            self.dts
        )

    def test_add_event(self):
        client = Mock()
        client.add_event = Mock(return_value={})
        table = resources.Table(name='test', client=client)
        event = resources.Event(timestamp=self.dt)
        table.add_event(123, event)
        client.add_event.assert_called_once_with(
            table,
            123,
            event
        )

    def test_delete_event(self):
        client = Mock()
        client.delete_event = Mock(return_value=None)
        table = resources.Table(name='test', client=client)
        event = resources.Event(timestamp=self.dt)
        table.delete_event(123, event)
        client.delete_event.assert_called_once_with(
            table,
            123,
            event
        )

    def test_query(self):
        client = Mock()
        client.query = Mock(return_value={})
        table = resources.Table(name='test', client=client)
        table.query({})
        client.query.assert_called_once_with(table, {})
