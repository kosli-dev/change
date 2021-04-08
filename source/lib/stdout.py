import builtins


class Stdout():

    def print(self, string):
        # Intention is write string to a io.StringIO
        # object and then drop capsys in all tests.
        builtins.print(string)
