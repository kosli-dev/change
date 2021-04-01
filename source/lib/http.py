from lib.http_retry import HttpRetry
import json
from requests.auth import HTTPBasicAuth


def http_get_json(url, api_token):
    auth = HTTPBasicAuth(api_token, 'unused')
    response = HttpRetry().get(url, auth=auth)
    return response


def http_put_payload(url, payload, api_token):
    auth = HTTPBasicAuth(api_token, 'unused')
    headers = json_content_header()
    data = json.dumps(payload)
    response = HttpRetry().put(url, auth=auth, headers=headers, data=data)
    return response


def http_post_payload(url, payload, api_token):
    auth = HTTPBasicAuth(api_token, 'unused')
    headers = json_content_header()
    data = json.dumps(payload)
    response = HttpRetry().post(url, auth=auth, headers=headers, data=data)
    return response


def json_content_header():
    return {"Content-Type": "application/json"}
