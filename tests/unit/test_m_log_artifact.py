import command_processor
from tests.utils import verify_approval, ScopedEnvVars, ScopedFileCopier, CDB_DRY_RUN


def test_command_processor_log_artifact_file(capsys):
    commit = "abc50c8a53f79974d615df335669b59fb56a4ed3"
    env = {
        "MERKELY_COMMAND": "log_artifact",
        "MERKELY_API_TOKEN": "MY_SUPER_SECRET_API_TOKEN",
        "MERKELY_FINGERPRINT": "file://coverage.txt",
        "MERKELY_CI_BUILD_URL": "https://gitlab/build/1456",
        "MERKELY_CI_BUILD_NUMBER": "23",
        "MERKELY_ARTIFACT_GIT_URL": "http://github/me/project/commit/" + commit,
        "MERKELY_ARTIFACT_GIT_COMMIT": commit,
    }

    with ScopedEnvVars({**CDB_DRY_RUN, **env}) as ev:
        with ScopedFileCopier("/app/tests/data/coverage.txt", "/coverage.txt"):
            with ScopedFileCopier("/app/tests/data/Merkelypipe.json", "/Merkelypipe.json"):
                assert ev.get("MERKELY_COMMAND") == "log_artifact"
                status_code = command_processor.execute(ev)

    assert status_code == 0
    verify_approval(capsys)

