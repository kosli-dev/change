import json
import os

import requests as req
from requests.auth import HTTPBasicAuth
from cdb.http_retry import http_retry


def http_get_json(url, api_token):
    print("Getting this endpoint: " + url)
    resp = req.get(url, auth=HTTPBasicAuth(api_token, 'unused'))
    print(resp.text)
    return resp.json()


def http_put_payload(url, payload, api_token):
    headers = {"Content-Type": "application/json"}
    print("Putting this payload:")
    print(json.dumps(payload, sort_keys=True, indent=4))
    print("To url: " + url)
    if os.getenv('CDB_DRY_RUN', "FALSE") != "TRUE":
        resp = http_retry().put(url, data=json.dumps(payload), headers=headers, auth=HTTPBasicAuth(api_token, 'unused'))
        print(resp.text)
    else:
        print("DRY RUN: Put not sent")


def http_post_payload(url, payload, api_token):
    headers = {"Content-Type": "application/json"}
    print("Posting this payload:")
    print(json.dumps(payload, sort_keys=True, indent=4))
    print("To url: " + url)
    if os.getenv('CDB_DRY_RUN', "FALSE") != "TRUE":
        resp = http_retry().post(url, data=json.dumps(payload), headers=headers, auth=HTTPBasicAuth(api_token, 'unused'))
        print(resp.text)
    else:
        print("DRY RUN: POST not sent")
