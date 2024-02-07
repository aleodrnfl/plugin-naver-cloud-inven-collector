import os
import logging
from spaceone.core import utils
from spaceone.tester import TestCase
from spaceone_company.manager.insight_manager import InsightManager

_LOGGER = logging.getLogger(__name__)

class TestInsightManager(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get("SPACEONE_TEST_CONFIG_FILE", "./config.yml")
    )
    global_config = config.get("GLOBAL", {})
    endpoints = global_config.get("ENDPOINTS", {})
    secrets = global_config.get("SECRETS", {})

    insight_manager = InsightManager(secret_data=secrets)
    insight_instances = insight_manager.collect_cloud_service(options={}, secret_data=secrets)

    for insight_instance in insight_instances:
        print(insight_instance)