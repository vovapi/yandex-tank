'''Static Graph plotter plugin that plots static graphs and save them to picture files'''

from Tank.Plugins.Aggregator import AggregateResultListener, AggregatorPlugin
from tankcore import AbstractPlugin
from collections import defaultdict
import logging
import time
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
#import string


class StaticGraphsPlugin(AbstractPlugin, AggregateResultListener):
    '''Static graphs plotter'''

    SECTION = 'static_graphs'

    @staticmethod
    def get_key():
        return __file__

    def __init__(self, core):
        AbstractPlugin.__init__(self, core)
        self.log = logging.getLogger(__name__)
        self.overall_data = []
        self.cases_data = defaultdict(list)

    @staticmethod
    def __analyze(timestamp, data):
        return (
            int(time.mktime(timestamp.timetuple())),
            data.planned_requests,
            data.active_threads,
            data.selfload,
            data.RPS,
            data.dispersion,
            data.input,
            data.output,
            data.avg_connect_time,
            data.avg_send_time,
            data.avg_latency,
            data.avg_receive_time,
            data.avg_response_time,
        ) + tuple(data.quantiles)
        #    data.http_codes,
        #    data.net_codes,
        #    data.times_dist,
        #    data.quantiles,

    def configure(self):
        '''Read configuration'''
        #file_prefix = self.get_option("file_prefix", "")
        aggregator = self.core.get_plugin_of_type(AggregatorPlugin)
        aggregator.add_result_listener(self)
        self.log.info("Configured StaticGraphs plugin")

    def aggregate_second(self, data):
        """
        @data: SecondAggregateData
        """
        self.overall_data.append(StaticGraphsPlugin.__analyze(data.time, data.overall))
        for k, v in data.cases.iteritems():
            self.cases_data[k].append(StaticGraphsPlugin.__analyze(data.time, v))

    def post_process(self, retcode):
        self.log.info("Plotting data")
        StaticGraphsPlugin.__plot(self.overall_data)
        self.log.info("Writing aggregated data to a file")
        with open('graph_data.dat', 'w') as datafile:
            for data in self.overall_data:
                datafile.write("\t".join(str(element) for element in data) + "\n")

    @staticmethod
    def __plot(data):
        np_data = np.array(data)
        plt.plot(np_data[:, 1:])
        plt.savefig('graph.png')
