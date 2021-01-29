from cdb.http import http_put_payload, http_post_payload

from tests.utils import silent, ScopedEnvVars, CDB_DRY_RUN


def test_put_dry_run_doesnt_call(mocker, capsys):
    requests = mocker.patch('cdb.http.req')

    with silent(capsys), ScopedEnvVars(CDB_DRY_RUN):
        http_put_payload("https://www.example.com", {}, "")

    requests.put.assert_not_called()


def test_post_dry_run_doesnt_call(mocker, capsys):
    requests = mocker.patch('cdb.http.req')

    with silent(capsys), ScopedEnvVars(CDB_DRY_RUN):
        http_post_payload("https://www.example.com", {}, "")

    requests.post.assert_not_called()
