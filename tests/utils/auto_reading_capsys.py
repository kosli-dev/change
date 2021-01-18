

def auto_reading(capsys):
    """
    We only want output when there are failing tests.
    If tests do not read capsys then the captured stdout/stderr
    are dumped to the terminal, even for passing tests.
    """
    return AutoReadingCapsys(capsys)


class AutoReadingCapsys(object):
    def __init__(self, capsys):
        self._capsys = capsys

    def __enter__(self):
        pass

    def __exit__(self, _type, _value, _traceback):
        self._capsys.readouterr()
