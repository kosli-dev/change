import os


class FileFingerprintEnvVar:

    def __init__(self, command, protocol, artifact_name):
        self._command = command
        self._protocol = protocol
        self._artifact_name = artifact_name

    @property
    def notes(self):
        return "\n".join([
            'The string `file://` followed by the full path of the file to fingerprint.',
            'The full path must be volume-mounted.',
            'Example:',
            'docker run ... \\',
            '    --env MERKELY_FINGERPRINT=”file://${YOUR_FILE_PATH} \\',
            '    --volume=${YOUR_FILE_PATH}:${YOUR_FILE_PATH} \\',
            '    ...',
        ])

    @property
    def artifact_name(self):
        return self._artifact_name

    @property
    def artifact_basename(self):
        return os.path.basename(self.artifact_name)

    @property
    def sha(self):
        return self._command.file_fingerprinter(self._protocol, self.artifact_name)

