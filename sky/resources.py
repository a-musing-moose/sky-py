# -*- coding: utf-8 -*-
from datetime import datetime

from . import timestamp as ts


class Resource(object):

    def to_dict(self):
        return {}

    def from_dict(self, obj):
        return self


class Event(Resource):

    def __init__(self, data={}, timestamp=None):
        super(Event, self).__init__()
        if timestamp is None:
            timestamp = datetime.utcnow()
        self.timestamp = timestamp
        self.data = data

    def to_dict(self):
        obj = super(Event, self).to_dict()
        obj['timestamp'] = ts.dumps(self.timestamp)
        obj['data'] = self.data
        return obj

    def from_dict(self, obj):
        super(Event, self).from_dict(obj)
        if 'timestamp' in obj:
            self.timestamp = ts.loads(obj['timestamp'])
        else:
            self.timestamp = datetime.utcnow(),
        self.data = obj.get('data', {})
        return self


class Property(Resource):

    DATA_TYPE_STRING = 'string'
    DATA_TYPE_INTEGER = 'integer'
    DATA_TYPE_FLOAT = 'float'
    DATA_TYPE_BOOLEAN = 'boolean'
    DATA_TYPE_FACTOR = 'factor'

    DATA_TYPES = (
        DATA_TYPE_STRING,
        DATA_TYPE_INTEGER,
        DATA_TYPE_FLOAT,
        DATA_TYPE_BOOLEAN,
        DATA_TYPE_FACTOR
    )

    def __init__(
        self,
        property_id=None,
        name=None,
        transient=False,
        data_type='string'
    ):
        self.object_id = property_id
        self.name = name
        self.transient = transient
        if data_type not in self.DATA_TYPES:
            raise ValueError('%s is not a valid data_type' % data_type)
        self.data_type = data_type

    def to_dict(self):
        obj = super(Property, self).to_dict()
        obj['name'] = self.name
        obj['transient'] = self.transient
        obj['data_type'] = self.data_type
        if self.object_id:
            obj['id'] = self.object_id
        return obj

    def from_dict(self, obj):
        super(Property, self).from_dict(obj)
        if obj.get('id', None) is not None:
            self.object_id = int(obj['id'])
        self.name = obj.get('name', '')
        self.transient = obj.get('transient', False)
        self.data_type = obj.get('data_type', '')
        return self

class Table(Resource):

    def __init__(self, name=None, client=None):
        self.client = client
        self.name = name

    # PROPERTIES API

    def get_properties(self):
        return self.client.get_properties(self)

    def get_property(self, name):
        return self.client.get_property(self, name)

    def create_property(self, prop):
        return self.client.create_property(self, prop)

    def update_property(self, property_name, prop):
        return self.client.update_property(self, property_name, prop)

    def delete_property(self, prop):
        return self.client.delete_property(self, prop)

    # EVENTS API

    def get_events(self, object_id):
        return self.client.get_events(self, object_id)

    def get_event(self, object_id, timestamp):
        return self.client.get_event(self, object_id, timestamp)

    def add_event(self, object_id, event):
        return self.client.add_event(self, object_id, event)

    def delete_event(self, object_id, event):
        return self.client.delete_event(self, object_id, event)

    # QUERY API

    def query(self, query):
        return self.client.query(self, query)

    # Encoding

    def to_dict(self):
        return {
            'name': self.name
        }

    def from_dict(self, obj):
        self.name = obj.get('name', '')
        return self
