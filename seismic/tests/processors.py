# -*- coding: utf-8 -*-
import datetime
from structlog import DropEvent
from .. import processors
import os
os.environ['SEISMIC_APP'] = 'test_app'

import unittest

class SeismicProcessorTest(unittest.TestCase):
    def test_app(self):
        event_dict = processors.app({}, 'msg', {})
        self.assertIn('app', event_dict.keys())
        self.assertEqual(os.environ.get('SEISMIC_APP'), event_dict.get('app'))

    def test_timestamp(self):
        event_dict = processors.timestamp({}, 'msg', {})
        self.assertIsInstance(event_dict.get('timestamp'), str)
        event_dict = processors.timestamp({}, 'msg', {'timestamp': datetime.datetime.utcnow()})
        self.assertIsInstance(event_dict.get('timestamp'), str)
        ts = datetime.datetime.utcnow().isoformat()
        event_dict = processors.timestamp({}, 'msg', {'timestamp': ts})
        self.assertIsInstance(event_dict.get('timestamp'), str)
        self.assertEqual(ts, event_dict.get('timestamp'))

    def test_uid(self):
        with self.assertRaises(DropEvent):
            processors.uid({}, 'msg', {})

        with self.assertRaises(DropEvent):
            event_dict = processors.uid({}, 'msg', {'timestamp': 1})
        with self.assertRaises(DropEvent):
            event_dict = processors.uid({}, 'msg', {'timestamp': datetime.datetime.utcnow()})
        event_dict = processors.uid(
            {}, 'msg', {'timestamp': datetime.datetime.utcnow().isoformat()})
        self.assertTrue(event_dict.get('uid') is not None)
        self.assertEqual(len(event_dict.get('uid')), 16)

    def test_action_version(self):
        self.assertIsNotNone(processors.action_version({}, 'msg', {}).get('version'))

        def v(x):
            return x.get('version')

        v1 = processors.action_version({}, 'msg', {'a': 1})
        v2 = processors.action_version({}, 'msg', {'b': 1})
        v3 = processors.action_version({}, 'msg', {'a': 9999})

        self.assertNotEqual(v(v1), v(v2))
        self.assertEqual(v(v1), v(v3))

        v4 = processors.action_version({}, 'msg', {'a': 1, 'b': {'x': 19898998}})
        v5 = processors.action_version({}, 'msg', {'a': 1, 'b': {'y': 19898998}})
        self.assertNotEqual(v(v4), v(v5))

        v6 = processors.action_version({}, 'msg', {'a': 1, 'b': 123, 'x': 888})
        self.assertEqual(v(v4), v(v6))
