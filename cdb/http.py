import json
import os

import requests as req
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def http_get_json(url, api_token):
    print("Getting this endpoint: " + url)
    resp = req.get(url, auth=HTTPBasicAuth(api_token, 'unused'))
    print(resp.text)
    return resp.json()


def put_payload(payload, url, api_token):
    headers = {"Content-Type": "application/json"}
    print("Putting this payload:")
    print(json.dumps(payload, sort_keys=True, indent=4))
    print("To url: " + url)
    if os.getenv('CDB_DRY_RUN', "FALSE") != "TRUE":
        resp = req.put(url, data=json.dumps(payload), headers=headers, auth=HTTPBasicAuth(api_token, 'unused'))
        print(resp.text)
    else:
        print("DRY RUN: Put not sent")


def http_post_payload(payload, url, api_token):
    headers = {"Content-Type": "application/json"}
    print("Posting this payload:")
    print(json.dumps(payload, sort_keys=True, indent=4))
    print("To url: " + url)
    if os.getenv('CDB_DRY_RUN', "FALSE") != "TRUE":
        resp = retry_http().post(url, data=json.dumps(payload), headers=headers, auth=HTTPBasicAuth(api_token, 'unused'))
        print(resp.text)
    else:
        print("DRY RUN: POST not sent")


def retry_http():
    # The backoff_factor controls how long to sleep between retries. The algorithm is
    # {backoff factor} * (2 ** ({number of total retries} - 1))
    # So for 1, the 5 retry sleeps are [ 0.5, 1, 2, 4, 8 ]
    # for a total sleep of 15.5 seconds
    strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[503],
        allowed_methods=["POST"]
    )
    adapter = HTTPAdapter(max_retries=strategy)
    s = req.Session()
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s
