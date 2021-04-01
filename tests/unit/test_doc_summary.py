from commands import Command, External


def test_doc_summary():
    for name in Command.names():
        klass = Command.named(name)
        command = klass(External())
        if klass.__name__ == 'ControlPullRequest':
            continue
        assert len(command.doc_summary('github')) > 0, klass.__name__


