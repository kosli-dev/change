from lib.http_retry import HttpRetry
import json
from requests.auth import HTTPBasicAuth


class Http:

    def __init__(self):
        pass

    def get_json(self, url, api_token):
        auth = HTTPBasicAuth(api_token, 'unused')
        return HttpRetry().get(url, auth=auth)

    def put_payload(self, url, payload, api_token):
        auth = HTTPBasicAuth(api_token, 'unused')
        headers = json_content_header()
        data = json.dumps(payload)
        return HttpRetry().put(url, auth=auth, headers=headers, data=data)

    def post_payload(self, url, payload, api_token):
        auth = HTTPBasicAuth(api_token, 'unused')
        headers = json_content_header()
        data = json.dumps(payload)
        return HttpRetry().post(url, auth=auth, headers=headers, data=data)

def json_content_header():
    return {"Content-Type": "application/json"}
