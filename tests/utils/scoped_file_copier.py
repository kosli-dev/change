from os import path, remove
from shutil import copyfile


class ScopedFileCopier(object):
    class Error(ValueError):
        pass

    def __init__(self, source_file, target_file):
        if not path.isfile(source_file):
            raise self.Error(f"source file '{source_file}' does not exist")
        if path.exists(target_file):
            raise self.Error(f"target file '{target_file}' already exists")
        self._source_file = source_file
        self._target_file = target_file

    def __enter__(self):
        copyfile(self._source_file, self._target_file)

    def __exit__(self, _type, _value, _traceback):
        remove(self._target_file)
