from commands import Command, External


def test_summary():
    env = {"MERKELY_COMMAND": "unused"}
    external = External(env=env)
    for klass in Command.all().values():
        command = klass(external)
        if klass.__name__ == 'ControlPullRequest':
            continue
        if klass.__name__ == 'LogApproval':
            continue
        assert len(command.summary('github')) > 0, klass.__name__


def test_invocation_strings():
    env = {"MERKELY_COMMAND": "unused"}
    external = External(env=env)
    for klass in Command.all().values():
        command = klass(external)
        assert len(command.invocation('full', 'github')) > 0
        assert len(command.invocation('minimum', 'bitbucket')) > 0


