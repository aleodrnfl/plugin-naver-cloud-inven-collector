import os
import logging
from spaceone.core import utils
from spaceone.tester import TestCase, print_json

from spaceone_company.connector.metric_connector import MetricConnector

_LOGGER = logging.getLogger(__name__)


class TestMetricConnector(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get("SPACEONE_TEST_CONFIG_FILE", "./config.yml")
    )
    global_config = config.get("GLOBAL", {})
    endpoints = global_config.get("ENDPOINTS", {})
    secrets = global_config.get("SECRETS", {})

    metric_connector = MetricConnector(secret_data=secrets)

    def test_get_metric_list(self):
        metric_instances = self.metric_connector.get_metric_list()
        print(metric_instances)

    def test_get_metric_group_list(self):
        metric_group_instances = self.metric_connector.get_metric_group_list()
        print(metric_group_instances)