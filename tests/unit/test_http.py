from cdb.http import http_put_payload, http_post_payload

from tests.utils import auto_reading, cdb_dry_run


def test_put_dry_run_doesnt_call(mocker, capsys):
    requests = mocker.patch('cdb.http.req')

    with auto_reading(capsys), cdb_dry_run():
        http_put_payload("https://www.example.com", {}, "")

    requests.put.assert_not_called()


def test_post_dry_run_doesnt_call(mocker, capsys):
    requests = mocker.patch('cdb.http.req')

    with auto_reading(capsys), cdb_dry_run():
        http_post_payload("https://www.example.com", {}, "")

    requests.post.assert_not_called()
