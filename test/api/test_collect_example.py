import os
import logging
from spaceone.core import utils
from spaceone.tester import TestCase, print_json

_LOGGER = logging.getLogger(__name__)


class TestCollectExample(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get("SPACEONE_TEST_CONFIG_FILE", "./config.yml")
    )
    endpoints = config.get("ENDPOINTS", {})

    def test_init(self):
        v_info = self.inventory.Collector.init({"options": {}})
        print_json(v_info)

    def test_collect(self):
        options = {}
        params = {"options": options, "secret_data": {}}

        res_stream = self.inventory.Collector.collect(params)

        for res in res_stream:
            print_json(res)
