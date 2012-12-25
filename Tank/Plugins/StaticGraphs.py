#!/usr/bin/env python
"""
Show how to make date plots in matplotlib using date tick locators and
formatters.  See major_minor_demo1.py for more information on
controlling major and minor ticks

All matplotlib date plotting is done by converting date instances into
days since the 0001-01-01 UTC.  The conversion, tick locating and
formatting is done behind the scenes so this is most transparent to
you.  The dates module provides several converter functions date2num
and num2date

"""
#import datetime
import numpy as np
import scipy.stats as st
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
#import matplotlib.cbook as cbook
from itertools import groupby


class PhoutReader(object):
    def __init__(self, filename):
        self.file = open(filename, 'rb')

    def __iter__(self):
        line = self.file.readline()
        while line:
            #time, tag, interval_real, connect_time, send_time, latency, receive_time, interval_event, size_out, size_in, net_code, proto_code = line.split()
            fields = line.strip().split("\t")
            yield fields
            line = self.file.readline()


class Aggregator(object):
    def __init__(self, reader):
        self.reader = reader

    def __iter__(self):
        return groupby(self.reader, lambda x: int(float(x[0]) + float(x[2]) / 1000000))


class Analyser(object):
    def __init__(self, aggregator):
        self.aggregator = aggregator

    def __iter__(self):
        return ((k, self.analyze(g)) for (k, g) in self.aggregator)

    def analyze(self, data):
        data_array = np.array([[int(field) for field in [interval_real, connect_time, send_time, latency, receive_time, interval_event, size_out, size_in, net_code, proto_code]]
            for (time, tag, interval_real, connect_time, send_time, latency, receive_time, interval_event, size_out, size_in, net_code, proto_code) in data])
        resp_times = data_array[:, 0]
        return (st.describe(resp_times), st.scoreatpercentile(resp_times, 90))


class Plotter(object):
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def plot(self):
        data = np.array(list(self.analyzer))

ag = Analyser(Aggregator(PhoutReader("/tmp/phout.log")))

#for k in ag:
#    print k
    #print np.array([[int(field) for field in [interval_real, connect_time, send_time, latency, receive_time, interval_event, size_out, size_in, net_code, proto_code]]
    #    for (time, tag, interval_real, connect_time, send_time, latency, receive_time, interval_event, size_out, size_in, net_code, proto_code) in g])
