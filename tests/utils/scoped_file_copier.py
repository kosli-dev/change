from os import path, remove
from shutil import copyfile


def scoped_merkelypipe_json():
    return ScopedFileCopier("/app/tests/data/Merkelypipe.json", "/Merkelypipe.json")


class ScopedFileCopier(object):
    class Error(ValueError):
        pass

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
