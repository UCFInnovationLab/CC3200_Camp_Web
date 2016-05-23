import json

from utils import rounded_unicode


class StreamParser(object):

    def __init__(self, stream):
        self.stream = stream

    def current_value(self):
        """
        Return current value and time.
        """
        current_value = self.stream.values(limit=1)['values'][0]
        return current_value['value'], current_value['timestamp']


class NumericStreamParser(StreamParser):

    def __init__(self, stream):
        super(NumericStreamParser, self).__init__(stream)
        self.stats = self.call_stats()
        self.min = self.stats['stats']['min']
        self.max = self.stats['stats']['max']
        self.mean = self.stats['stats']['avg']
        self.stddev = self.stats['stats']['stddev']
        self.count = self.stats['stats']['count']

    def get_mean(self):
        return rounded_unicode(self.mean)

    def get_min(self):
        return rounded_unicode(self.min)

    def get_max(self):
        return rounded_unicode(self.max)

    def call_stats(self):
        return self.stream.stats()


class MacStreamParser(StreamParser):

    def __init__(self, stream):
        super(MacStreamParser, self).__init__(stream)
        self.values = self.get_stream_values()

    def get_stream_values(self, start=None, end=None, limit=10000):
        # M2X can return a maximum of 10000 data points in one simple request
        return self.stream.values(start=start, end=end, limit=limit)

    def set_stream_values(self, start=None, end=None, limit=10000):
        # M2X can return a maximum of 10000 data points in one simple request
        self.values = self.stream.values(start=start, end=end, limit=limit)

    def current_value(self):
        return self.stream.values(limit=1)

    def unique_macs(self, start=None, end=None):
        """
        Return the number of unique MAC addresses that had connected
        to the WiFi network during the time between start and end.

        Start and End in ISO-8601 format.
        """
        # M2X will return the time of the request as the end time if none is
        # specified
        endtime = self.values['end']

        if self.values['values']:
            uniques = set()

            for value in self.values['values']:
                macs_list = json.loads(value['value'])
                for connect in macs_list:
                    uniques.add(connect[1])

            number_uniques = len(uniques)

            if start is None:
                starttime = self.values['values'][-1]['timestamp']
            else:
                starttime = start

            return number_uniques, starttime, endtime

        if start is None:
            starttime = None
            return 0, starttime, endtime
        else:
            starttime = start
            return 0, starttime, endtime

    def macs_vendors(self, start=None):
        """
        Return a dictionary with MAC addresses who have connected to Pyfi, the
        last time they connected and their vendor if known.

        Returns either the most recent info or info for a given range.

        Start and End in ISO-8601 format.
        """
        # M2X can return a maximum of 10000 data points in one simple request
        if start:
            values = self.values
        else:
            values = self.current_value()

        if values['values']:
            mac_addresses = {}

            for value in values['values']:
                time = value['timestamp']
                macs_list = json.loads(value['value'])
                for connect in macs_list:
                    if connect[1] not in mac_addresses:
                        mac_addresses[connect[1]] = [connect[0],
                                                     connect[2],
                                                     time]

        return mac_addresses
