from datetime import datetime

from m2x.utils import to_utc

from utils import rounded_unicode, to_datetime

class StreamParser(object):

    def __init__(self, stream):
        self.stream = stream

    def current_value(self):
        '''
        Return current value and time.
        '''
        current_value = self.stream.values(limit=1)['values'][0]
        return current_value['value'], current_value['timestamp']

    def get_timestamps(self, start=None, end=None):
        pass


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
        ''' 
        Stats for a given time period
        '''
        return self.stream.stats()


class MacStreamParser(StreamParser):

    def __init__(self, stream):
        super(MacStreamParser, self).__init__(stream)

    def unique_macs(self, start=None, end=None, limit=1000):
        '''
        Return the number of unique MAC addresses that had connected
        to the WiFi network during the time between start and end.

        Start and End in ISO-8601 format.
        '''
        # M2X can return a maximum of 1000 data points in one simple request
        values = self.stream.values(start=start, end=end, limit=limit)
        
        # M2X will return the time of the request as the end time if none is specified
        endtime = values['end']

        if values['values']:
            uniques = set()

            for value in values['values']:
                macs_list = value['value'].split(', ')
                uniques.update(macs_list)

            number_uniques = len(uniques)

            if start is None:
                starttime = values['values'][-1]['timestamp']
            else:
                starttime = start

            return number_uniques, starttime, endtime

        if start is None:
            starttime = None
            return 0, starttime, endtime
        else:
            starttime = start
            return 0, starttime, endtime
