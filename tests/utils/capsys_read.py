
def capsys_read(capsys):
    out, _err = capsys.readouterr()
    return out
