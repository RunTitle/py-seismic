# -*- coding: utf-8 -*-
import calendar
import iso8601
import datetime
import zlib
import collections
import random
import os

from future.utils import listitems

from structlog import DropEvent


def _get_keys(event_dict):
    keys = []
    stack = listitems(event_dict)
    while stack:
        k, v = stack.pop()
        keys.append(k)
        if isinstance(v, collections.Mapping):
            stack.extend(listitems(v))
    keys.sort()
    return keys


def action_version(logger, method_name, event_dict):
    event_dict['version'] = zlib.adler32(",".join(_get_keys(event_dict)).encode())
    return event_dict


def uid(logger, method_name, event_dict):
    # timestamp: 8 bytes
    # hostname: 4
    # uid version: 1
    # rando: 3
    ts = event_dict.get('timestamp')
    if ts is None:
        raise DropEvent
    try:
        time_component = hex(calendar.timegm(iso8601.parse_date(ts).utctimetuple()))[2:]
    except:
        raise DropEvent
    hostname = os.getenv('HOSTNAME', 'ABCD')[:4]
    uid_version = "0"
    rando = hex(random.randint(0, 4095))[-3:]
    event_dict['uid'] = "".join([time_component, hostname, uid_version, rando])
    return event_dict


def timestamp(logger, method_name, event_dict):
    ts = event_dict.get('timestamp', datetime.datetime.utcnow())
    if isinstance(ts, datetime.datetime):
        event_dict['timestamp'] = ts.isoformat()
        return event_dict
    else:
        return event_dict


def app(logger, method_name, event_dict):
    if event_dict.get('app') is None:
        event_dict['app'] = os.environ.get('SEISMIC_APP','UNKNOWN_APP')
    return event_dict

def action_normalizer(logger, method_name, event_dict):
    val = event_dict.get('action')
    if val is not None:
        event_dict['action'] = val.lower()
    return event_dict
