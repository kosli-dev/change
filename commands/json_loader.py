from commands import CommandError
import json


def load_json(filename):
    try:
        with open(filename) as file:
            return json.load(file)
    except FileNotFoundError:
        raise CommandError(f"{filename} file not found.")
    except IsADirectoryError:
        raise CommandError(f"{filename} is a directory.")
    except json.decoder.JSONDecodeError as exc:
        raise CommandError(f"{filename} invalid json - {str(exc)}")
