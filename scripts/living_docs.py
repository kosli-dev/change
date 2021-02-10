from commands import COMMANDS, Context


def print_living_docs():
    name = 'log_evidence'
    env = {"MERKELY_COMMAND": name}
    context = Context(env, None, None)
    command = COMMANDS[name](context)
    print(command.overview)
    for env_var in command.env_vars:
        print(f"{env_var.name} {env_var.type} {env_var.description}")

if __name__ == '__main__':
    print_living_docs()
