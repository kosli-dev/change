from commands import *


COMMANDS = {
    "declare_pipeline": DeclarePipelineCommand,
    "log_artifact": LogArtifactCommand,
    "log_deployment": LogDeploymentCommand,
    "log_evidence": LogEvidenceCommand
}


class UnknownCommand(Command):
    def __call__(self):
        raise CommandError(f"Unknown command {self.name}")


def build_command(context):
    name = Command(context).name.value
    return COMMANDS.get(name, UnknownCommand)(context)
