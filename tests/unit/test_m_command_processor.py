from commands import Context, command_processor, CommandError

from tests.utils import verify_approval, ScopedEnvVars, ScopedFileCopier, CDB_DRY_RUN


def test_raises_when_merkely_command_not_set(capsys):
    ev = {
        # "MERKELY_COMMAND": "declare_pipeline",
        "MERKELY_API_TOKEN": "MY_SUPER_SECRET_API_TOKEN",
        "MERKELY_HOST": "https://test.merkely.com"
    }

    with ScopedEnvVars({**CDB_DRY_RUN, **ev}) as env:
        status_code = command_processor.execute(make_context(env))

    assert status_code == 23
    verify_approval(capsys)


def make_context(env):
    context = type('context', (), {})()
    context.env = env
    return context


