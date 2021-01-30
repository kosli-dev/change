from os import path, remove
from shutil import copyfile


class ScopedFileCopier(object):
    def __init__(self, source_file, target_file):
        if not path.isfile(source_file):
            raise self.Error("source file '{} does not exist".format(source_file))
        if path.exists(target_file):
            raise self.Error("target file '{}' already exists".format(target_file))
        self._source_file = source_file
        self._target_file = target_file

    def __enter__(self):
        copyfile(self._source_file, self._target_file)

    def __exit__(self, _type, _value, _traceback):
        remove(self._target_file)

    class Error(ValueError):
        pass