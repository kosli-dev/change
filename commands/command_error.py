
class CommandError(Exception):
    def __init__(self, status_code, message):
        super().__init__(message)
        self._status_code = status_code

    @property
    def status_code(self):
        return self._status_code
