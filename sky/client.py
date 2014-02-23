# -*- coding: utf-8 -*-
import requests
import json

from . import resources
from . import timestamp as ts


class SkyClient(object):

    def __init__(self, host='127.0.0.1', port=8585, use_ssl=False):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl

    # TABLE API

    def __getattr__(self, name):
        return self.get_table(name)

    def get_tables(self):
        tables = []
        response = self.send('get', '/tables')
        for data in response:
            tables.append(resources.Table().from_dict(data))
        return tables


    def get_table(self, name):
        response = self.send('get', '/tables/%s' % name)
        return resources.Table().from_dict(response)

    def create_table(self, table):
        response = self.send('post', '/tables', table.to_dict())
        table.client = self
        return table.from_dict(response)

    def delete_table(self, table):
        self.send('delete', '/tables/%s' % table.name)
        return None

    # PROPERTIES API

    def get_properties(self, table):
        properties = []
        response = self.send('get', '/tables/%s/properties' % table.name)
        for data in response:
            properties.append(resources.Property().from_dict(data))
        return properties

    def get_property(self, table, name):
        response = self.send(
            'get',
            '/tables/%s/properties/%s' % (table.name, name)
        )
        return resources.Property().from_dict(response)

    def create_property(self, table, prop):
        response = self.send(
            'post',
            '/tables/%s/properties' % table.name,
            prop.to_dict()
        )
        return prop.from_dict(response)

    def update_property(self, table, property_name, prop):
        response = self.send(
            'patch',
            '/tables/%s/properties/%s' % (table.name, property_name),
            prop.to_dict()
        )
        return prop.from_dict(response)

    def delete_property(self, table, prop):
        self.send(
            'delete',
            '/tables/%s/properties/%s' % (table.name, prop.name)
        )
        return None

    # EVENT API

    def get_events(self, table, object_id):
        events = []
        response = self.send(
            'get',
            '/tables/%s/objects/%s/events' % (table.name, object_id)
        )
        for data in response:
            events.append(resources.Event().from_dict(data))
        return events

    def get_event(self, table, object_id, timestamp):
        timestamp = ts.dumps(timestamp)
        response = self.send(
            'get',
            '/tables/%s/objects/%s/events/%s' % (
                table.name,
                object_id,
                timestamp
            )
        )
        return resources.Event().from_dict(response)

    def create_event(self, table, object_id, event, replace=True):
        method = 'patch'
        if replace:
            method = 'put'
        timestamp = ts.dumps(event.timestamp)
        response = self.send(
            method,
            '/tables/%s/objects/%s/events/%s' % (
                table.name,
                object_id,
                timestamp
            ),
            event.to_dict()
        )
        return resources.Event().from_dict(response)

    def delete_event(self, table, object_id, event):
        timestamp = ts.dumps(event.timestamp)
        self.send(
            'delete',
            '/tables/%s/objects/%s/events/%s' % (
                table.name,
                object_id,
                timestamp
            ),
        )
        return None

    # QUERY API

    def query(self, table, q):
        if isinstance(q, list):
            q = {'steps': q}
        return self.send(
            'get',
            '/tables/%s/query' % table.name,
            q
        )

    # UTILITY API

    def ping(self):
        try:
            self.send('get', '/ping')
        except Exception:
            return False
        else:
            return True

    # HTTP METHODS

    def send(self, method, path, data=None):
        methods = {
            'get': requests.get,
            'post': requests.post,
            'put': requests.put,
            'patch': requests.patch,
            'delete': requests.delete
        }
        func = methods.get(method, None)
        if func is None:
            raise ValueError("%s is not a recognised http method" % method)

        headers = {'content-type': 'application/json'}
        url = self.make_url(path)

        if data:
            data = json.dumps(data, sort_keys=True)

        kwargs = {
            'data': data,
            'headers': headers
        }
        if self.use_ssl:
            kwargs['verify'] = False # Bad! but currently needed

        response = func(url, **kwargs)
        response.raise_for_status()
        return response.json

    def make_url(self, path):

        protocol = "http"
        if self.use_ssl:
            protocol = 'https'
        return "%s://%s:%d%s" % (
            protocol,
            self.host,
            self.port,
            path
        )
