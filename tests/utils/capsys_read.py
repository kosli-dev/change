
def capsys_read(capsys):
    out, err = capsys.readouterr()
    return out + err
