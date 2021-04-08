import io


class Stdout():

    def __init__(self):
        self._stream = io.StringIO()

    def print(self, string):
        self._stream.write(string + "\n")

    def getvalue(self):
        return self._stream.getvalue()