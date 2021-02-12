import os


class FileFingerprintEnvVar:

    def __init__(self, command, protocol, artifact_name):
        self.__command = command
        self.__protocol = protocol
        self.__artifact_name = artifact_name

    @property
    def notes(self):
        return "\n".join([
            f'The string `{self.__protocol}` followed by the full path of the file to fingerprint.',
            'The full path must be volume-mounted.',
            'Example:',
            'docker run ... \\',
            f'    --env MERKELY_FINGERPRINT=”{self.__protocol}${{YOUR_FILE_PATH}} \\',
            '    --volume=${YOUR_FILE_PATH}:${YOUR_FILE_PATH} \\',
            '    ...',
        ])

    @property
    def artifact_name(self):
        return self.__artifact_name

    @property
    def artifact_basename(self):
        return os.path.basename(self.artifact_name)

    @property
    def sha(self):
        return self.__command.file_fingerprinter(self.__protocol, self.artifact_name)

