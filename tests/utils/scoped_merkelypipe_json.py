from .scoped_file_copier import ScopedFileCopier


def scoped_merkelypipe_json(filename=None):
    if filename is None:
        filename = "/app/tests/data/Merkelypipe.json"
    return ScopedFileCopier(filename, "/Merkelypipe.json")

