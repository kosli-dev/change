

def flushing_capsys(capsys):
    """
    If tests do not flush capsys then the
    captured stdout and stderr are dumped to
    the console, even for passing tests.
    This makes it harder to spot the output
    related to failing tests.
    """
    return FlushingCapsys(capsys)


class FlushingCapsys(object):
    def __init__(self, capsys):
        self._capsys = capsys

    def __enter__(self):
        pass

    def __exit__(self, _type, _value, _traceback):
        self._capsys.readouterr()
