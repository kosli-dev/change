
def silence(capsys):
    return capsys.readouterr()


def silent(capsys):
    """
    Most approval-tests use capsys to verify against an ...approved.txt file.
    silent() is for tests that want to silence output noise from the
    code under test. We only want output when there are failing tests.
    """
    return ScopedCapsysReader(capsys)


class ScopedCapsysReader(object):
    def __init__(self, capsys):
        self._capsys = capsys

    def __enter__(self):
        pass

    def __exit__(self, _type, _value, _traceback):
        self._capsys.readouterr()
