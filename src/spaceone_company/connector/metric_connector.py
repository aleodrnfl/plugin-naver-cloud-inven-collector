import logging
from spaceone.core.connector import BaseConnector
import hashlib
import hmac
import base64
import requests
import time
import json

_LOGGER = logging.getLogger("cloudforet")

def make_signature(access_key, secret_key, method, uri, timestamp):
    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    secret_key = bytes(secret_key, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey

class MetricConnector(BaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.access_key = kwargs['secret_data']['ncloud_access_key_id']
        self.secret_key = kwargs['secret_data']['ncloud_secret_key']
        self.prod_key = kwargs['secret_data']['ncloud_prod_key']

    def get_metric_list(self): ##SearchMetricList api 사용
        metric_list = []
        url = 'https://cw.apigw.ntruss.com/cw_fea/real/cw/api/rule/group/metric/search'
        method = 'POST'
        timestamp = str(int(time.time() * 1000))

        headers = {
            'x-ncp-apigw-signature-v2': make_signature(self.access_key, self.secret_key, method,
                                                       '/cw_fea/real/cw/api/rule/group/metric/search',
                                                       timestamp).decode(),
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': self.access_key,
            'Content-Type': 'application/json'
        }

        payload = {
            "prodKey": self.prod_key
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            metrics = data['metrics']
            for metric in metrics:
                tem_list = []
                tem_list.append(f"metric: {metric['metric']}")
                tem_list.append(f"idDimension: {metric['idDimension']}")
                metric_list.append(tem_list)

        else:
            print(f"Error: {response.status_code}, {response.text}")

        return metric_list

    def get_metric_group_list(self):
        metric_group_list = []

        url = f'https://cw.apigw.ntruss.com/cw_fea/real/cw/api/rule/group/metrics/query/{self.prod_key}'
        method = 'GET'
        timestamp = str(int(time.time() * 1000))

        headers = {
            'x-ncp-apigw-signature-v2': make_signature(self.access_key, self.secret_key, method,
                                                       f'/cw_fea/real/cw/api/rule/group/metrics/query/{self.prod_key}',
                                                       timestamp).decode(),
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': self.access_key
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            for item in data['metricsGroups']:
                for metric_item in item['metrics']:
                    temp_list = []
                    temp_list.append(f"metric: {metric_item['metric']}")
                    temp_list.append(f"GroupId: {metric_item['metricGroupItemId']}")
                    temp_list.append(f"idDimension: {item['idDimension']}")
                    metric_group_list.append(temp_list)
            # print(metric_group_list)
        else:
            print(f"Error: {response.status_code}, {response.text}")
        return metric_group_list