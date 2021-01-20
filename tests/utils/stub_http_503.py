import json
import responses


def stub_http_503(method, count, url=None):
    # Eg during deployment rollover
    if url is None:
        url = "https://test.compliancedb.com/api/v1/{}/".format(method.lower())

    def request_callback(request):
        headers = {}
        if len(responses.calls) < count:
            return 503, headers, json.dumps({"error": "service unavailable"})
        else:
            return 200, headers, json.dumps({"success": 42})

    responses.add_callback(
        getattr(responses, method),
        url=url,
        callback=request_callback
    )

    if method == "GET":
        payload = None
    if method == "POST":
        payload = {"name": "cern", "template": ["artefact", "unit_test"]}
    if method == "PUT":
        payload = {"name": "git", "template": ["artefact", "coverage"]}
    api_token = ""
    return url, payload, api_token
