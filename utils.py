from requests.exceptions import HTTPError

from datetime import datetime

def rounded_unicode(value):
        return unicode(round(float(value), 2))

def get_device(devicename, client):
    try:
        device = [d for d in client.devices(q=devicename) if d.name == devicename][0]
    except IndexError:
        device = client.create_device(name=devicename,
                                      description="Local Network Monitor",
                                      visibility="private")
    return device


def get_stream(device, name, numeric=True):
    try:
        stream = device.stream(name)
    except HTTPError:
        if numeric:
            stream = device.create_stream(name)
        else:
            stream = device.create_stream(name, type='alphanumeric')
    return stream

def get_streams(device, *names, **kwargs):
    streams = []
    numeric = kwargs.get('numeric', True)
    # Get the stream if it exists, if not create the stream.
    for name in names:
        streams.append(get_stream(device, name, numeric))
    return streams


def to_datetime(time_string):
    return datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S.%fZ')