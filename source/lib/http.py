from lib.http_retry import HttpRetry
from errors import ChangeError
import json
from requests.auth import HTTPBasicAuth


def http_get_json(url, api_token):
    auth = HTTPBasicAuth(api_token, 'unused')
    response = HttpRetry().get(url, auth=auth)
    raise_unless_success(response)
    return response


def http_put_payload(url, payload, api_token):
    auth = HTTPBasicAuth(api_token, 'unused')
    headers = json_content_header()
    data = json.dumps(payload)
    response = HttpRetry().put(url, auth=auth, headers=headers, data=data)
    raise_unless_success(response)
    return response


def http_post_payload(url, payload, api_token):
    auth = HTTPBasicAuth(api_token, 'unused')
    headers = json_content_header()
    data = json.dumps(payload)
    response = HttpRetry().post(url, auth=auth, headers=headers, data=data)
    raise_unless_success(response)
    return response


def raise_unless_success(response):
    # Eg https://github.com/merkely-development/change/runs/1961998055?check_suite_focus=true
    status_code = response.status_code
    if status_code in [200, 201]:
        print(response.text)
    else:
        message = f"HTTP status=={status_code}\n{response.text}"
        raise ChangeError(message)


def json_content_header():
    return {"Content-Type": "application/json"}
