from os import path
from shutil import copytree, rmtree


class ScopedDirCopier(object):
    class Error(ValueError):
        pass

    def __init__(self, source_dir, target_dir):
        if not path.isdir(source_dir):
            raise self.Error("source dir '{} does not exist".format(source_dir))
        if path.exists(target_dir):
            raise self.Error("target dir '{}' already exists".format(target_dir))
        self._source_dir = source_dir
        self._target_dir = target_dir

    def __enter__(self):
        copytree(self._source_dir, self._target_dir)

    def __exit__(self, _type, _value, _traceback):
        rmtree(self._target_dir)

