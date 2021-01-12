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


RETRY_COUNT = 5  # See LoggingRetry comment below.


def retry_http():
    strategy = LoggingRetry(
        total=RETRY_COUNT,
        backoff_factor=1,
        status_forcelist=[503],
        allowed_methods=["POST"]
    )
    adapter = HTTPAdapter(max_retries=strategy)
    s = req.Session()
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s


class LoggingRetry(Retry):
    """"
    Retry documentation is https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html
    It says the backoff algorithm is:
       {backoff factor} * (2 ** ({number of total retries} - 1))
    With backoff_factor==1, this gives successive sleeps of:
       [ 0.5, 1, 2, 4, 8, 16, 32, ... ]
    However, the self.get_backoff_time() values are actually:
       [ 0, 2, 4, 8 16, 32, ... ]
    Zero would look strange in a log message so not using it.
    0+2+4+8+16==30 seconds, about right, so RETRY_COUNT==5
    """
    def increment(self, *args, **kwargs):
        count = len(self.history)
        if count > 0:
            request = self.history[-1]
            if count == 1:
                print("{} failed".format(request.method))
                print("URL={}".format(request.url))
                print("STATUS={}".format(request.status))
            backoff_time = 2 ** count
            if backoff_time != (2 ** RETRY_COUNT):
                # The last time increment() is called is _after_ the last retry.
                print("Retry {}/{} in {} seconds".format(count, RETRY_COUNT-1, backoff_time), flush=True)
        return super().increment(*args, **kwargs)

