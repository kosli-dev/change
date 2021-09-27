from errors import ChangeError
from fingerprinters import *

FINGERPRINTERS = {
    "docker_fingerprinter": DockerFingerprinter,
    "file_fingerprinter": FileFingerprinter,
    "dir_fingerprinter": DirFingerprinter,
    "sha256_fingerprinter": Sha256Fingerprinter,
}


def build_fingerprinter(name):
    klass = FINGERPRINTERS.get(name)
    if klass is None:
        raise ChangeError(f"Unknown fingerprinter: {name}")
    else:
        return klass()
