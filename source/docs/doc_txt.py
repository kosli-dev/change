import os
from commands import Command, External

# The Makefile volume-mounts docs.merkely.com/ to docs/
REFERENCE_DIR = '/docs/build/reference'


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
    docs = {}
    command_names = sorted(Command.names())
    command_names.remove('control_pull_request')  # Currently only github

    for command_name in command_names:
        filename = f"{REFERENCE_DIR}/min/{command_name}.txt"
        lines = min_lines_for(command_name)
        docs[filename] = lines
    ci_names = [
        'docker',
        'bitbucket',
        'github',
    ]
    for ci_name in ci_names:
        for command_name in command_names:
            filename = f"{REFERENCE_DIR}/{ci_name}/{command_name}.txt"
            lines = lines_for(ci_name, command_name)
            docs[filename] = lines
    return docs


def lines_for(ci, command_name):
    if ci == 'docker':
        return lines_for_docker(command_name)
    if ci == 'bitbucket':
        return lines_for_bitbucket(command_name)
    if ci == 'github':
        return lines_for_github(command_name)


def min_lines_for(command_name):
    command = command_for(command_name)
    tab = "    "

    def lc(string):
        line_continuation = "\\"
        return f"{string} {line_continuation}"

    def env(var):
        if var.name == "MERKELY_COMMAND":
            value = var.value
        elif var.name == 'MERKELY_FINGERPRINT':
            value = 'docker://acme/road-runner:2.3'
        else:
            value = '"' + "${" + var.name + "}" + '"'
        return lc(f'{tab}--env {var.name}={value}')

    lines = [lc("docker run")]

    for var in command.merkely_env_vars:
        if var.name == "MERKELY_PIPE_PATH":
            continue
        if var.name == "MERKELY_HOST":
            continue
        if var.is_required:
            lines.append(env(var))

    lines.append(lc(f"{tab}--rm"))
    for mount in command.doc_volume_mounts('docker'):
        lines.append(lc(f"{tab}--volume {mount}"))

    # The merkely-pipe volume-mount is always required
    if command_name == 'declare_pipeline':
        lines.append(lc(tab + "--volume ${YOUR_MERKELY_PIPE}:/data/Merkelypipe.json"))

    # The name of the docker image
    lines.append(f"{tab}merkely/change")

    return lines


yml_name_texts = {
    'declare_pipeline': 'Declare Merkely Pipeline',
    'log_artifact': 'Log Docker image in Merkely',
    'log_deployment': 'Log deployment in Merkely',
    'log_evidence': 'Log evidence in Merkely',
    'log_test': 'Log unit test results in Merkely',
    'request_approval': 'Request approval in Merkely',
    'approve_deployment': 'Approve a deployment',
    'control_deployment': 'Fail the pipeline unless approved for deployment in Merkely'
}


def lines_for_docker(command_name):
    def lc(string):
        line_continuation = "\\"
        return f"{string} {line_continuation}"

    tab = " " * 4
    def env(var):
        if var.name == "MERKELY_COMMAND":
            value = var.value
        else:
            value = '"' + "${" + var.name + "}" + '"'
        return lc(f'{tab}--env {var.name}={value}')

    command = command_for(command_name)
    lines = [lc("docker run")]
    for var in command.merkely_env_vars:
        lines.append(env(var))
    lines.append(lc(f"{tab}--rm"))
    for mount in command.doc_volume_mounts('docker'):
        lines.append(lc(f"{tab}--volume {mount}"))
    if command_name == 'declare_pipeline':
        lines.append(lc(tab + "--volume ${YOUR_MERKELY_PIPE}:/data/Merkelypipe.json"))
    lines.append(f"{tab}merkely/change")
    return lines


def lines_for_github(command_name):
    command = command_for(command_name)
    lines = [
        "    - name: {}".format(yml_name_texts[command_name]),
        "      uses: docker://merkely/change:latest",
        "      env:",
    ]
    tab = " " * 8
    for var in command.merkely_env_vars:
        show, example = var.doc_example('github', command_name)
        if show:
            lines.append(f'{tab}{var.name}: {example}')
    return lines


def lines_for_bitbucket(command_name):
    command = command_for(command_name)
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
        "          - pipe: docker://merkely/change:latest",
        "            variables:",
    ]
    tab = " " * 14
    for var in command.merkely_env_vars:
        show, example = var.doc_example('bitbucket', command_name)
        if show:
            lines.append(f'{tab}{var.name}: {example}')
    return lines


def command_for(name):
    cls = Command.named(name)
    env = {"MERKELY_COMMAND": name}
    external = External(env=env)
    return cls(external)

