import logging
from spaceone.core.manager import BaseManager
from spaceone.inventory.plugin.collector.lib import *
from ..connector.metric_connector import MetricConnector

_LOGGER = logging.getLogger("cloudforet")

class MetricManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "SpaceONE"
        self.cloud_service_type = "metric"
        self.provider = "spaceone_company"
        self.metadata_path = "metadata/spaceone/metric.yaml"

    def collect_resources(self, options, secret_data):
        try:
            yield from self.collect_cloud_service_type(options, secret_data)
            yield from self.collect_cloud_service(options, secret_data)
        except Exception as e:
            yield make_error_response(
                error=e,
                provider=self.provider,
                cloud_service_group=self.cloud_service_group,
                cloud_service_type=self.cloud_service_type,
            )

    def collect_cloud_service_type(self, options, secret_data):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True,
        )

        yield make_response(
            cloud_service_type=cloud_service_type,
            match_keys=[["name", "reference.resource_id", "account", "provider"]],
            resource_type="inventory.CloudServiceType",
        )

    def collect_cloud_service(self, options, secret_data):
        metric_connector = MetricConnector(secret_data=secret_data)
        metric_instances = metric_connector.get_metric_list()
        # metric_group_instances = metric_connector.get_metric_group_list()

        data = metric_instances['metrics']
        for metric in data:
            metric_data = {
                'dataType': metric['dataType'],
                'desc': metric['desc'],
                'dimensions': metric['dimensions'],
                'idDimension': metric['idDimension'],
                'metric': metric['metric'],
                'options': metric['options'],
                'prodKey': metric['prodKey'],
                'unit': metric['unit']
            }

            cloud_service = make_cloud_service(
                name=metric['metric'],
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=metric_data,
            )
            yield make_response(
                cloud_service=cloud_service,
                match_keys=[["name", "reference.resource_id", "account", "provider"]]
            )













