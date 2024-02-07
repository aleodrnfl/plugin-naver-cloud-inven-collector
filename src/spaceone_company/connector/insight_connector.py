import logging
from spaceone.core.connector import BaseConnector
import hashlib
import hmac
import base64
import requests
import time

_LOGGER = logging.getLogger("cloudforet")

def make_signature(access_key, secret_key, method, uri, timestamp):
    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    secret_key = bytes(secret_key, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey

class InsightConnector(BaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.access_key = kwargs['secret_data']['ncloud_access_key_id']
        self.secret_key = kwargs['secret_data']['ncloud_secret_key']

    def get_dashboard_list(self):
        dashboard_list = []

        url = 'https://cw.apigw.ntruss.com/cw_fea/real/cw/api/chart/dashboard'
        method = 'GET'
        timestamp = str(int(time.time() * 1000))

        headers = {
            'x-ncp-apigw-signature-v2': make_signature(self.access_key, self.secret_key, method, '/cw_fea/real/cw/api/chart/dashboard', timestamp).decode(),
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': self.access_key
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            dashboards = response.json()
            if dashboards:
                for dashboard in dashboards:
                    dashboard_list.append(dashboard)
            else:
                _LOGGER.warning("대시보드가 비어 있습니다.")
        else:
            _LOGGER.error(f"대시보드 목록을 가져오는 중 오류가 발생했습니다. 응답 코드: {response.status_code}")

        return dashboard_list

    # @staticmethod
    # def get_dashboard_list() -> dict:
    #     return {
    #         'dashboard_list': [
    #             {"id": "df_457958429047263232", "name": "Server(VPC)"},
    #             {"id": "df_618514435065122816", "name": "Object Storage"}
    #         ]
    #     }