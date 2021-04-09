import os
from commands import Command, External

# The Makefile volume-mounts docs.merkely.com/ to docs/
REFERENCE_DIR = '/docs/build/reference'
IMAGE_NAME = 'merkely/change:latest'


def create_txt_files():
    """
    Called from docs.merkely.com/source/conf.py
    Generates text files containing documentation fragment for each
    command (eg 'log_test') in each supported CI system (eg 'bitbucket')
    """
    for filename, lines in generate_docs().items():
        dir = os.path.dirname(filename)
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(filename, "wt") as file:
            file.writelines(line + "\n" for line in lines)


def generate_docs():
    data = create_data()
    docs = {}

    command_names = sorted(Command.names())
    for command_name in command_names:
        filename = f"{REFERENCE_DIR}/min/{command_name}.txt"
        lines = min_lines_for(data['docker'], command_name)
        docs[filename] = lines

    for command_name in command_names:
        if command_name == 'control_pull_request':
            ci_names = ['docker', 'bitbucket']
        else:
            ci_names = ['docker', 'bitbucket', 'github']
        for ci_name in ci_names:
            filename = f"{REFERENCE_DIR}/{ci_name}/{command_name}.txt"
            lines = lines_for(data, ci_name, command_name)
            docs[filename] = lines
    return docs


def lines_for(data, ci, command_name):
    if ci == 'docker':
        return lines_for_docker(data['docker'], command_name)
    if ci == 'bitbucket':
        return lines_for_bitbucket(data['bitbucket'], command_name)
    if ci == 'github':
        return lines_for_github(data['github'], command_name)


def create_data():
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
                'example': var.doc_example('github', command_name)
            }
            data['bitbucket'][command_name]['env_vars'][var.name] = {
                'name': var.name,
                'example': var.doc_example('bitbucket', command_name)
            }
    return data


def min_lines_for(data, command_name):
    tab = "    "

    def lc(string):
        line_continuation = "\\"
        return f"{string} {line_continuation}"

    def env(var):
        if var['name'] == "MERKELY_COMMAND":
            value = command_name
        elif var['name'] == 'MERKELY_FINGERPRINT':
            value = 'docker://acme/road-runner:2.3'
        else:
            value = '"' + "${" + var['name'] + "}" + '"'
        return lc(f"{tab}--env {var['name']}={value}")

    lines = [lc("docker run")]

    for _,var in data[command_name]['env_vars'].items():
        if var['name'] == "MERKELY_PIPE_PATH":
            continue
        if var['name'] == "MERKELY_HOST":
            continue
        if var['is_required']:
            lines.append(env(var))

    lines.append(lc(f"{tab}--rm"))
    
    for mount in data[command_name]['volume_mounts']:
        lines.append(lc(f"{tab}--volume {mount}"))

    lines.append(f"{tab}{IMAGE_NAME}")

    return lines


yml_name_texts = {
    'declare_pipeline': 'Declare Merkely Pipeline',
    'log_artifact': 'Log Docker image in Merkely',
    'log_deployment': 'Log deployment in Merkely',
    'log_evidence': 'Log evidence in Merkely',
    'log_test': 'Log unit test results in Merkely',
    'request_approval': 'Request approval in Merkely',
    'approve_deployment': 'Approve a deployment',
    'control_deployment': 'Fail the pipeline unless approved for deployment in Merkely',
    'control_pull_request': 'Fail the pipeline unless approved pull_request for this commit',
}


def lines_for_docker(data, command_name):
    def lc(string):
        line_continuation = "\\"
        return f"{string} {line_continuation}"

    tab = " " * 4
    def env(var):
        if var['name'] == "MERKELY_COMMAND":
            value = command_name
        else:
            value = '"' + "${" + var['name'] + "}" + '"'
        return lc(f"{tab}--env {var['name']}={value}")

    lines = [lc("docker run")]

    for _, var in data[command_name]['env_vars'].items():
        lines.append(env(var))

    lines.append(lc(f"{tab}--rm"))

    for mount in data[command_name]['volume_mounts']:
        lines.append(lc(f"{tab}--volume {mount}"))

    lines.append(f"{tab}{IMAGE_NAME}")
    
    return lines


def lines_for_github(data, command_name):
    lines = [
         "    - name: {}".format(yml_name_texts[command_name]),
        f"      uses: docker://{IMAGE_NAME}",
         "      env:",
    ]
    tab = " " * 8

    for _, var in data[command_name]['env_vars'].items():
        show, example = var['example']
        if show:
            lines.append(f"{tab}{var['name']}: {example}")

    return lines


def lines_for_bitbucket(data, command_name):
    name = yml_name_texts[command_name]
    step_name = "_".join(name.lower().split(' '))
    if command_name == 'declare_pipeline':
        export = "export_merkely_pipeline_env_vars"
    else:
        export = "export_merkely_fingerprint_env_vars"
    lines = [
       f"    - step: &{step_name}",
       f"        name: {name}",
        "        services: [ docker ]",
        "        script:",
       f"          - *{export}",
       f"          - pipe: docker://{IMAGE_NAME}",
        "            variables:",
    ]
    tab = " " * 14

    for _, var in data[command_name]['env_vars'].items():
        show, example = var['example']
        if show:
            lines.append(f"{tab}{var['name']}: {example}")

    return lines


def command_for(name):
    cls = Command.named(name)
    env = {"MERKELY_COMMAND": name}
    external = External(env=env)
    return cls(external)

