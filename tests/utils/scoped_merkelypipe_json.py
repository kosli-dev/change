from .scoped_file_copier import ScopedFileCopier


def scoped_merkelypipe_json(*, filename=None):
    directory = "/app/tests/data"
    if filename is None:
        filename = "Merkelypipe.json"
    return ScopedFileCopier(f"{directory}/{filename}", "/Merkelypipe.json")

