import json
import logging
from spaceone.core.manager import BaseManager
from spaceone.inventory.plugin.collector.lib import *
from spaceone_company.connector.server_connector import ServerConnector

_LOGGER = logging.getLogger("cloudforet")


class ServerManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "SpaceONE"
        self.cloud_service_type = "Server"
        self.provider = "naver cloud"
        self.metadata_path = "metadata/spaceone/server.yaml"

    def collect_resources(self, options, secret_data, schema):
        try:
            yield from self.collect_cloud_service_type(options, secret_data, schema)
            yield from self.collect_cloud_service(options, secret_data, schema)
        except Exception as e:
            yield make_error_response(
                error=e,
                provider=self.provider,
                cloud_service_group=self.cloud_service_group,
                cloud_service_type=self.cloud_service_type,
            )

    def collect_cloud_service_type(self, options, secret_data, schema):
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

    def collect_cloud_service(self, options, secret_data, schema):
        server_connector = ServerConnector(secret_data=secret_data)
        server_instances = server_connector.list_server_instance()
        for server_instance in server_instances:
            server_instance_dict = server_instance.__dict__
            cloud_service = make_cloud_service(
                name="sa",
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=server_instance_dict,
            )
            yield make_response(
                cloud_service=cloud_service,
                match_keys=[["name", "reference.resource_id", "account", "provider"]],
            )
