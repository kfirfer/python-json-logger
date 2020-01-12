import atexit
import os
import sys
import threading
import time
import traceback
from datetime import datetime
from multiprocessing import Queue
from time import sleep

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from custom.util import Singleton

q = None
bulk_size = 10
if "ELASTICSEARCH_MONITOR_HOSTS" in os.environ:
    queue_size = 10000
    if 'ELASTICSEARCH_MONITOR_QUEUE_SIZE' in os.environ:
        queue_size = int(os.environ['ELASTICSEARCH_MONITOR_QUEUE_SIZE'])
    q = Queue(queue_size)
if "ELASTICSEARCH_MONITOR_BULK_SIZE" in os.environ:
    bulk_size = int(os.environ['ELASTICSEARCH_MONITOR_BULK_SIZE'])
tags = {"component": "general"}
if 'ELASTICSEARCH_MONITOR_TAGS' in os.environ:
    try:
        tags = os.environ['ELASTICSEARCH_MONITOR_TAGS']
        tags = dict(item.split(":") for item in tags.split(","))
    except:
        print("Error parse ELASTICSEARCH_MONITOR_TAGS", file=sys.stderr)
        tags = {"component": "general"}


def index_log_to_elastic(body=None):
    try:
        if not q.full():
            q.put(body)
    except Exception as e:
        traceback.format_exc()


class ElasticSearchLogger:
    r"""
    Logger to console or/and elasticsearch.


    Environments variables:

    * LOGGER_LEVEL
        Possible values: "debug", "info", "warn", "error"

    * ELASTICSEARCH_MONITOR_HOSTS
        Elasticsearch logger host, can be multiple hosts separated by ":", for example:"10.0.0.1:9200,10,0.0.2:9200" ]

    * ELASTICSEARCH_MONITOR_QUEUE_SIZE
        Queue size, defaults to 10000

    * ELASTICSEARCH_MONITOR_BULK_SIZE
        How many message will be store before sending to elasticsearch

    * ELASTICSEARCH_MONITOR_TAGS
        Additional properties added to elasticsearch documents

    Examples usage:

    import os

    from util.loggers import Logger

    os.environ["ELASTICSEARCH_MONITOR_HOST"] = "127.0.0.1:9200"

    log = Logger()

    log.info("Some log")

    log.debug(generic_custom_field="hello world")
    """

    logger = None
    es_client = None
    kwargs = None
    is_es_enabled = True

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if "ELASTICSEARCH_MONITOR_HOSTS" in os.environ:
            es_hosts = os.environ["ELASTICSEARCH_MONITOR_HOSTS"]
            try:
                es_hosts = dict(item.split(":") for item in es_hosts.split(","))
            except:
                print("Error parse ELASTICSEARCH_MONITOR_HOSTS", file=sys.stderr)
                self.is_es_enabled = False
                return
            hosts = []
            for es_host, es_port in es_hosts.items():
                hosts.append({"host": es_host, "port": es_port})
            self.is_es_enabled = True
            ElasticSearchMonitorLogger(name='monitor', hosts=hosts)

    def external_logger(self, body):
        if self.is_es_enabled:
            index_log_to_elastic(body)


class ElasticSearchMonitorLogger(threading.Thread, metaclass=Singleton):
    hosts = None
    es_client = None
    bulk_data = []

    def __init__(self, target=None, name=None, hosts=None):
        super(ElasticSearchMonitorLogger, self).__init__()
        atexit.register(self.exit_handler)
        self.setDaemon(True)
        self.target = target
        self.name = name
        self.hosts = hosts
        self.start()

    def run(self):
        self.connect_es()
        self.bulk_data = []
        while True:
            try:
                body = q.get()
            except:
                traceback.format_exc()
                sleep(0.05)
                continue
            index = 'logs-{}'.format(datetime.today().strftime('%Y%m%d'))
            data_dict = {
                '_op_type': 'index',
                '_index': index,
                '_source': body
            }
            self.bulk_data.append(data_dict)
            if len(self.bulk_data) < bulk_size:
                continue

            try:
                bulk(client=self.es_client, actions=self.bulk_data)
            except:
                print(traceback.format_exc(), file=sys.stderr)
                sleep(60)
                self.connect_es()

            self.bulk_data = []

    def connect_es(self):
        self.es_client = Elasticsearch(hosts=self.hosts, timeout=600, retry_on_timeout=True, request_timeout=60.0,
                                       max_retries=0)

    def exit_handler(self):
        time.sleep(0.2)
        if len(self.bulk_data) > 0:
            try:
                bulk(client=self.es_client, actions=self.bulk_data)
            except:
                s = None  # Do nothing
