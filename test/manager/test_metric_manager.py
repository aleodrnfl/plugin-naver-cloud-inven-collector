import os
import logging
from spaceone.core import utils
from spaceone.tester import TestCase
from spaceone_company.manager.metric_manager import MetricManager

_LOGGER = logging.getLogger(__name__)

class TestMetricManager(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get("SPACEONE_TEST_CONFIG_FILE", "./config.yml")
    )
    global_config = config.get("GLOBAL", {})
    endpoints = global_config.get("ENDPOINTS", {})
    secrets = global_config.get("SECRETS", {})

    metric_manager = MetricManager(secret_data=secrets)
    metric_instances = metric_manager.collect_cloud_service(options={}, secret_data=secrets)

    for metric_instance in metric_instances:
        print(metric_instance)