import builtins


class Stdout():

    def print(self, string):
        # Intention is write string to a io.StringIO
        # object and then drop capsys in all tests.
        #
        #    import io
        #    stdout = io.StringIO()
        #    stdout.write("Hello ")
        #    stdout.write("world")
        #    assert stdout.getvalue() == "Hello world"
        builtins.print(string)
