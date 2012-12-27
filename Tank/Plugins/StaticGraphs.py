'''Static Graph plotter plugin that plots static graphs and save them to picture files'''

from Tank.Plugins.Aggregator import AggregateResultListener, AggregatorPlugin
from tankcore import AbstractPlugin
#import logging
#import string


class StaticGraphsPlugin(AbstractPlugin, AggregateResultListener):
    '''Static graphs plotter'''

    SECTION = 'static_graphs'

    @staticmethod
    def get_key():
        return __file__

    def __init__(self, core):
        AbstractPlugin.__init__(self, core)
        self.overall_data = []
        self.cases_data = {}

    @staticmethod
    def __analyse(time, data):
        return (
            time,
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
            data.avg_response_time
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

    def aggregate_second(self, data):
        """
        @data: SecondAggregateData
        """
        self.overall_data.append((StaticGraphsPlugin.__analyze(data.time, data.overall)))
        for k, v in data.cases:
            if not (k in self.cases_data):
                self.cases_data[k] = []
            self.cases_data[k].append((StaticGraphsPlugin.__analyze(data.time, v)))

    def post_process(self, retcode):
        for data in self.overall_data:
            print data
