from commands import CommandError
import json


def load_json(filename):
    try:
        with open(filename) as file:
            return json.load(file)
    except FileNotFoundError:
        raise CommandError(f"{filename} file not found.")
    except IsADirectoryError:
        # Note: If you do this...
        # --volume ${MERKELYPIPE}:/Merkelypipe.json
        # And ${MERKELYPIPE} does not exist on the client
        # volume-mount weirdness can happen and you
        # get an empty dir created on the client!
        raise CommandError(f"{filename} is a directory.")
    except json.decoder.JSONDecodeError as exc:
        raise CommandError(f"{filename} invalid json - {str(exc)}")
