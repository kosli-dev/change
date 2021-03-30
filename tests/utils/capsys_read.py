
def capsys_read(capsys, streams=None):
    out, err = capsys.readouterr()
    if streams is None:
        streams = ["out", "err"]
    actual = ""
    for stream in streams:
        if stream == "out":
            actual += out
        if stream == "err":
            actual += err
    return actual
