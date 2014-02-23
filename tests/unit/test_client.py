# -*- coding: utf-8 -*-
import pytz

from unittest import TestCase
from mock import Mock, patch
from datetime import datetime

from sky.client import SkyClient
from sky import resources


@patch('sky.client.requests')
class TestSkyClient(TestCase):

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

    def get_mock_response(self, payload):
        response = Mock()
        response.raise_for_status = Mock()
        response.json = payload
        return response

    def test_get_tables(self, requests):
        requests.get = Mock(return_value=self.get_mock_response(
            [
                {"name": "users"}
            ]
        ))
        client = SkyClient()
        tables = client.get_tables()
        requests.get.assert_called_once_with(
            'http://127.0.0.1:8585/tables',
            headers={'content-type': 'application/json'},
            data=None
        )
        self.assertEquals(tables[0].name, 'users')

    def test_get_table(self, requests):
        requests.get = Mock(
            return_value=self.get_mock_response({})
        )
        client = SkyClient()
        client.get_table('users')
        requests.get.assert_called_once_with(
            'http://127.0.0.1:8585/tables/users',
            headers={'content-type': 'application/json'},
            data=None
        )

    def test_magic_get(self, requests):
        requests.get = Mock(
            return_value=self.get_mock_response({})
        )
        client = SkyClient()
        client.users
        requests.get.assert_called_once_with(
            'http://127.0.0.1:8585/tables/users',
            headers={'content-type': 'application/json'},
            data=None
        )

    def test_create_table(self, requests):
        requests.post = Mock(
            return_value=self.get_mock_response({})
        )

        table = resources.Table(name='users')

        client = SkyClient()
        client.create_table(table)
        requests.post.assert_called_once_with(
            'http://127.0.0.1:8585/tables',
            headers={'content-type': 'application/json'},
            data='{"name": "users"}'
        )

    def test_delete_table(self, requests):
        requests.delete = Mock(
            return_value=self.get_mock_response({})
        )

        table = resources.Table(name='users')

        client = SkyClient()
        client.delete_table(table)
        requests.delete.assert_called_once_with(
            'http://127.0.0.1:8585/tables/users',
            headers={'content-type': 'application/json'},
            data=None
        )

    def test_get_properties(self, requests):
        requests.get = Mock(
            return_value=self.get_mock_response(
                [
                    {
                        "id": 213,
                        "name": "prop",
                        "transient": False,
                        "data_type": 'string'
                    }
                ]
            )
        )

        table = resources.Table(name='users')

        client = SkyClient()
        props = client.get_properties(table)
        requests.get.assert_called_once_with(
            'http://127.0.0.1:8585/tables/users/properties',
            headers={'content-type': 'application/json'},
            data=None
        )
        self.assertEquals(props[0].object_id, 213)
        self.assertEquals(props[0].name, 'prop')
        self.assertEquals(props[0].transient, False)
        self.assertEquals(props[0].data_type, 'string')

    def test_get_property(self, requests):
        requests.get = Mock(return_value=self.get_mock_response({}))
        table = resources.Table(name='users')

        client = SkyClient()
        client.get_property(table, 'age')
        requests.get.assert_called_once_with(
            'http://127.0.0.1:8585/tables/users/properties/age',
            headers={'content-type': 'application/json'},
            data=None
        )

    def test_create_property(self, requests):
        requests.post = Mock(return_value=self.get_mock_response({}))
        table = resources.Table(name='users')

        prop = resources.Property(1, 'age', False, 'string')

        client = SkyClient()
        client.create_property(table, prop)
        requests.post.assert_called_once_with(
            'http://127.0.0.1:8585/tables/users/properties',
            headers={'content-type': 'application/json'},
            data='{"transient": false, "name": "age", "data_type": "string", "id": 1}' #NOQA
        )

    def test_update_property(self, requests):
        requests.patch = Mock(return_value=self.get_mock_response({}))
        table = resources.Table(name='users')

        prop = resources.Property(1, 'ysb', False, 'string')

        client = SkyClient()
        client.update_property(table, 'age', prop)
        requests.patch.assert_called_once_with(
            'http://127.0.0.1:8585/tables/users/properties/age',
            headers={'content-type': 'application/json'},
            data='{"transient": false, "name": "ysb", "data_type": "string", "id": 1}' #NOQA
        )

    def test_delete_property(self, requests):
        requests.delete = Mock(return_value=self.get_mock_response({}))
        table = resources.Table(name='users')

        prop = resources.Property(1, 'age', False, 'string')

        client = SkyClient()
        client.delete_property(table, prop)
        requests.delete.assert_called_once_with(
            'http://127.0.0.1:8585/tables/users/properties/age',
            headers={'content-type': 'application/json'},
            data=None
        )

    def test_get_events(self, requests):
        requests.get = Mock(
            return_value=self.get_mock_response(
                [
                    {
                        'data': {},
                        'timestamp': self.dts
                    }
                ]
            )
        )

        client = SkyClient()
        table = resources.Table(name='users')
        events = client.get_events(table, 123)

        requests.get.assert_called_once_with(
            'http://127.0.0.1:8585/tables/users/objects/123/events',
            headers={'content-type': 'application/json'},
            data=None
        )

        self.assertEquals(events[0].timestamp, self.dt)

    def test_get_event(self, requests):
        requests.get = Mock(return_value=self.get_mock_response({}))

        client = SkyClient()
        table = resources.Table(name='users')

        client.get_event(table, 123, self.dt)
        requests.get.assert_called_once_with(
            'http://127.0.0.1:8585/tables/users/objects/123/events/%s' % self.dts, #NOQA
            headers={'content-type': 'application/json'},
            data=None
        )

    def test_create_event_with_replace(self, requests):
        requests.put = Mock(return_value=self.get_mock_response({}))
        client = SkyClient()
        table = resources.Table(name='users')
        event = resources.Event(timestamp=self.dt)
        client.create_event(table, 123, event)
        requests.put.assert_called_once_with(
            'http://127.0.0.1:8585/tables/users/objects/123/events/%s' % self.dts, #NOQA
            headers={'content-type': 'application/json'},
            data='{"timestamp": "2014-02-21T10:10:23.000203Z", "data": {}}'
        )

    def test_create_event_without_replace(self, requests):
        requests.patch = Mock(return_value=self.get_mock_response({}))
        client = SkyClient()
        table = resources.Table(name='users')
        event = resources.Event(timestamp=self.dt)
        client.create_event(table, 123, event, False)
        requests.patch.assert_called_once_with(
            'http://127.0.0.1:8585/tables/users/objects/123/events/%s' % self.dts, #NOQA
            headers={'content-type': 'application/json'},
            data='{"timestamp": "2014-02-21T10:10:23.000203Z", "data": {}}'
        )

    def test_delete_event(self, requests):
        requests.delete = Mock(return_value=self.get_mock_response({}))

        client = SkyClient()
        table = resources.Table(name='users')

        event = resources.Event(timestamp=self.dt)

        client.delete_event(table, 123, event)
        requests.delete.assert_called_once_with(
            'http://127.0.0.1:8585/tables/users/objects/123/events/%s' % self.dts, #NOQA
            headers={'content-type': 'application/json'},
            data=None
        )

    def test_query_with_dict(self, requests):
        requests.get = Mock(return_value=self.get_mock_response({}))

        client = SkyClient()
        table = resources.Table(name='users')
        client.query(table, {})

        requests.get.assert_called_once_with(
            "http://127.0.0.1:8585/tables/users/query",
            headers={'content-type': 'application/json'},
            data={}
        )

    def test_query_with_list(self, requests):
        requests.get = Mock(return_value=self.get_mock_response({}))

        client = SkyClient()
        table = resources.Table(name='users')
        client.query(table, [])

        requests.get.assert_called_once_with(
            "http://127.0.0.1:8585/tables/users/query",
            headers={'content-type': 'application/json'},
            data='{"steps": []}'
        )

    def test_ping(self, requests):
        requests.get = Mock(return_value=self.get_mock_response({}))
        client = SkyClient()
        ping = client.ping()
        requests.get.assert_called_once_with(
            'http://127.0.0.1:8585/ping',
            headers={'content-type': 'application/json'},
            data=None
        )
        self.assertTrue(ping)

    def test_failed_ping(self, requests):
        requests.get = Mock(side_effect=Exception(''))
        client = SkyClient()
        ping = client.ping()
        self.assertFalse(ping)

    def test_make_url(self, requests):
        client = SkyClient()
        self.assertEquals(
            client.make_url('/bob'),
            "http://127.0.0.1:8585/bob"
        )

    def test_make_url_when_using_ssl(self, requests):
        client = SkyClient(use_ssl=True)
        self.assertEquals(
            client.make_url('/bob'),
            "https://127.0.0.1:8585/bob"
        )

    def test_send_with_invalid_method(self, requests):
        client = SkyClient()
        self.assertRaises(
            ValueError,
            client.send,
            'custard',
            '/path'
        )

    def test_send_with_use_ssl(self, requests):
        requests.get = Mock(return_value=self.get_mock_response({}))
        client = SkyClient(use_ssl=True)
        client.send('get', '/path')

        requests.get.assert_called_once_with(
            'https://127.0.0.1:8585/path',
            headers={'content-type': 'application/json'},
            data=None,
            verify=False
        )

