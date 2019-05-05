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

