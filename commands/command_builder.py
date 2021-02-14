from commands import *

COMMANDS = {
    "declare_pipeline": DeclarePipeline,
    "log_artifact": LogArtifact,
    "log_deployment": LogDeployment,
    "log_evidence": LogEvidence,
    "log_approval": LogApproval,
    "log_test": LogTest,
    "control_deployment": ControlDeployment,
}


def build_command(context):
    name = Command(context).name.value
    klass = COMMANDS.get(name)
    if klass is not None:
        return klass(context)
    else:
        raise CommandError(f"Unknown command: {name}")
