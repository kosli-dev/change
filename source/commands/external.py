import json
import os
from errors import ChangeError
from fingerprinters import *


class External:
    """
    Holds (some) external dependencies to make Classic style testing easier.
    """
    def __init__(self,
                 *,
                 env=None,
                 docker_fingerprinter=None,
                 file_fingerprinter=None,
                 sha256_fingerprinter=None):

        self.__env = env
        self.__docker_fingerprinter = docker_fingerprinter
        self.__file_fingerprinter = file_fingerprinter
        self.__sha256_fingerprinter = sha256_fingerprinter

        if self.__env is None:
            self.__env = os.environ

        if self.__docker_fingerprinter is None:
            self.__docker_fingerprinter = DockerFingerprinter()

        if self.__file_fingerprinter is None:
            self.__file_fingerprinter = FileFingerprinter()

        if self.__sha256_fingerprinter is None:
            self.__sha256_fingerprinter = Sha256Fingerprinter()

    @property
    def merkelypipe(self):
        owner = self.env.get('MERKELY_OWNER', None)
        pipeline = self.env.get('MERKELY_PIPELINE', None)
        if owner and pipeline:
            return {
                'owner': owner,
                'name': pipeline
            }

        pipe_path = self.env.get('MERKELY_PIPE_PATH', '/data/Merkelypipe.json')
        if os.path.exists(pipe_path):
            return self.load_json(pipe_path)
        else:
            raise ChangeError(f"{pipe_path} file not found.")


    @property
    def env(self):
        return self.__env

    def fingerprinter_for(self, string):
        d = self.__docker_fingerprinter
        f = self.__file_fingerprinter
        s = self.__sha256_fingerprinter
        if d.handles_protocol(string):
            return d
        elif f.handles_protocol(string):
            return f
        elif s.handles_protocol(string):
            return s
        else:
            raise ChangeError(f"Unknown protocol: {string}")

    def load_json(self, filename):
        try:
            with open(filename) as file:
                return json.load(file)
        except FileNotFoundError:
            raise ChangeError(f"{filename} file not found.")
        except IsADirectoryError:
            # Note: If you do this...
            # --volume ${MERKELYPIPE}:/data/Merkelypipe.json
            # And ${MERKELYPIPE} does not exist (on the client)
            # then it is created as an empty directory on the
            # client and inside the container.
            raise ChangeError(f"{filename} is a directory.")
        except json.decoder.JSONDecodeError as exc:
            raise ChangeError(f"{filename} invalid json - {str(exc)}")
