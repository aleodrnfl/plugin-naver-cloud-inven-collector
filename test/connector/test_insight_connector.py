import os
import logging
from spaceone.core import utils
from spaceone.tester import TestCase, print_json

from spaceone_company.connector.insight_connector import InsightConnector

_LOGGER = logging.getLogger(__name__)


class TestInsightConnector(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get("SPACEONE_TEST_CONFIG_FILE", "./config.yml")
    )
    global_config = config.get("GLOBAL", {})
    endpoints = global_config.get("ENDPOINTS", {})
    secrets = global_config.get("SECRETS", {})

    insight_connector = InsightConnector(secret_data=secrets)

    def test_get_dashboard_list(self):
        dashboard_instances = self.insight_connector.get_dashboard_list()

        print(dashboard_instances)