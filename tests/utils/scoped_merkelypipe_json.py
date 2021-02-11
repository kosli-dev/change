from .scoped_file_copier import ScopedFileCopier


def scoped_merkelypipe_json(*, directory=None, filename=None):
    if directory is None:
        directory = "/app/tests/data"
    if filename is None:
        filename = "Merkelypipe.json"
    return ScopedFileCopier(f"{directory}/{filename}", "/Merkelypipe.json")

