import logging
from spaceone.core.manager import BaseManager
from spaceone.inventory.plugin.collector.lib import *
from ..connector.insight_connector import InsightConnector

_LOGGER = logging.getLogger("cloudforet")

class InsightManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "SpaceONE"
        self.cloud_service_type = "Insight"
        self.provider = "spaceone_company"
        self.metadata_path = "metadata/spaceone/insight.yaml"

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

    def collect_cloud_service_type(self, options, secret_data): #dashboard는 인자에 schema 없어도 됨.
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type, #insight
            group=self.cloud_service_group, #SpaceONE
            provider=self.provider, #spaceone_company
            metadata_path=self.metadata_path, #insight.yaml
            is_primary=True,
            is_major=True,
        )

        yield make_response(
            cloud_service_type=cloud_service_type,
            match_keys=[["name", "reference.resource_id", "account", "provider"]], #이거 내용 바꿔도 될듯
            resource_type="inventory.CloudServiceType",
        )

    def collect_cloud_service(self, options, secret_data):
        insight_connector = InsightConnector(secret_data=secret_data)
        dashboard_lists = insight_connector.get_dashboard_list()
        for dashboard_list in dashboard_lists:
            cloud_service = make_cloud_service(
                name=dashboard_list["name"],
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=dashboard_list,
            )
            yield make_response(
                cloud_service=cloud_service,
                match_keys=[["name", "reference.resource_id", "account", "provider"]] #얘도 똑같이 내용 바꿔도 될듯
            )












