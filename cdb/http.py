import json
import os

import requests as req
from requests.auth import HTTPBasicAuth


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
        print("DRY RUN: Put not requested")


def http_post_payload(payload, url, api_token):
    headers = {"Content-Type": "application/json"}
    print("Putting this payload:")
    print(json.dumps(payload, sort_keys=True, indent=4))
    print("To url: " + url)
    resp = req.post(url, data=json.dumps(payload), headers=headers, auth=HTTPBasicAuth(api_token, 'unused'))
    print(resp.text)