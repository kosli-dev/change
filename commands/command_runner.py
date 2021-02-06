from commands import *


def run(context):
    try:
        cmd = build_command(context)
        if cmd is not None:
            print(f"MERKELY_COMMAND={cmd.name.value}")
            for env_var in list(cmd.env_vars):
                env_var.verify()
            return cmd()
    except CommandError as exc:
        print(f"Error: {str(exc)}")
        return 144


