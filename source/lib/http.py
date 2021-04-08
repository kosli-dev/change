from lib.http_retry import HttpRetry
import json
from requests.auth import HTTPBasicAuth


class Http:

    def __init__(self, stdout):
        self._stdout = stdout

    def get_json(self, url, api_token):
        auth = HTTPBasicAuth(api_token, 'unused')
        return self._retry().get(url, auth=auth)

    def put_payload(self, url, payload, api_token):
        auth = HTTPBasicAuth(api_token, 'unused')
        headers = self._json_content_header()
        data = json.dumps(payload)
        return self._retry().put(url, auth=auth, headers=headers, data=data)

    def post_payload(self, url, payload, api_token):
        auth = HTTPBasicAuth(api_token, 'unused')
        headers = self._json_content_header()
        data = json.dumps(payload)
        return self._retry().post(url, auth=auth, headers=headers, data=data)

    def _retry(self):
        return HttpRetry(self._stdout)

    @staticmethod
    def _json_content_header():
        return {"Content-Type": "application/json"}
