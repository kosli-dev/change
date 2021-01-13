import os

from cdb.http import http_put_payload, http_post_payload


def test_put_dry_run_doesnt_call(mocker):
    requests = mocker.patch('cdb.http.req')
    os.environ["CDB_DRY_RUN"] = "TRUE"
    http_put_payload("https://www.example.com", {}, "")
    requests.put.assert_not_called()


def test_post_dry_run_doesnt_call(mocker):
    requests = mocker.patch('cdb.http.req')
    os.environ["CDB_DRY_RUN"] = "TRUE"
    http_post_payload("https://www.example.com", {}, "")
    requests.post.assert_not_called()
