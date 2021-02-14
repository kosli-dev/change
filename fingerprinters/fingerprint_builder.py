from commands import CommandError
from fingerprinters import *

FINGERPRINTERS = {
    "docker_fingerprinter": DockerFingerprinter,
    "file_fingerprinter": FileFingerprinter,
    "sha256_fingerprinter": Sha256Fingerprinter,
}


def build_fingerprinter(name):
    klass = FINGERPRINTERS.get(name)
    if klass is None:
        return CommandError(f"Unknown fingerprinter: {name}")
    else:
        return klass()
