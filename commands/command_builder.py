from commands import *


COMMANDS = {
    "declare_pipeline": DeclarePipelineCommand,
    "log_artifact": LogArtifactCommand,
    "log_deployment": LogDeploymentCommand,
    "log_evidence": LogEvidenceCommand,
}


class UnknownCommand(Command):

    def __call__(self):
        raise self.unknown_command_error()

    @property
    def _env_var_names(self):
        raise self.unknown_command_error()

    def unknown_command_error(self):
        return CommandError(f"Unknown command: {self.name.value}")


def build_command(context):
    name = Command(context).name.value
    return COMMANDS.get(name, UnknownCommand)(context)
