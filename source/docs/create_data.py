from commands import Command, External


def create_data():
    """
    Called from docs.merkely.com/source/conf.py
    """
    # Looking into saving all Docs data into a json file
    # and then retrieving the json file. This would be
    # a nice Separation of Concerns and it would also
    # allow a Go client to generate the equivalent json.
    data = {
        'docker': {},
        'bitbucket': {},
        'github': {}
    }
    command_names = sorted(Command.names())
    for command_name in command_names:
        command = command_for(command_name)
        data['docker'][command_name] = {
            'volume_mounts': command.doc_volume_mounts(),
            'env_vars': {}
        }
        data['bitbucket'][command_name] = {
            'env_vars': {}
        }
        data['github'][command_name] = {
            'env_vars': {}
        }
        for var in command.merkely_env_vars:
            data['docker'][command_name]['env_vars'][var.name] = {
                'name': var.name,
                'is_required': var.is_required,
            }
            data['github'][command_name]['env_vars'][var.name] = {
                'name': var.name,
                'is_required': var.is_required,
                'example': var.doc_example('github', command_name),
                'note': var.doc_note('github', command_name)
            }
            data['bitbucket'][command_name]['env_vars'][var.name] = {
                'name': var.name,
                'is_required': var.is_required,
                'example': var.doc_example('bitbucket', command_name),
                'note': var.doc_note('bitbucket', command_name)
            }
    return data


def command_for(name):
    cls = Command.named(name)
    env = {"MERKELY_COMMAND": name}
    external = External(env=env)
    return cls(external)
