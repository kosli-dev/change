import os
from commands import Command, External

# The Makefile volume-mounts docs.merkely.com/ to docs/
REFERENCE_DIR = '/docs/build/reference'


def auto_generate():
    """
    Generates text files containing documentation source for each
    command (eg 'log_test') in each supported CI system (eg 'bitbucket')
    """
    make_dir(REFERENCE_DIR)
    make_dir(f"{REFERENCE_DIR}/min")
    command_names = [
        'declare_pipeline',
        'log_approval',
        'log_artifact',
        'log_deployment',
        'log_evidence',
        'log_test',
        'control_deployment',
    ]
    for command_name in command_names:
        min_filename = f"{REFERENCE_DIR}/min/{command_name}.txt"
        min_lines = min_lines_for(command_name)
        with open(min_filename, "wt") as file:
            file.writelines(line + "\n" for line in min_lines)

    ci_names = [
        'bitbucket',
        'docker',
        'github',
    ]
    for ci_name in ci_names:
        make_dir(f"{REFERENCE_DIR}/{ci_name}")
        for command_name in command_names:
            filename = f"{REFERENCE_DIR}/{ci_name}/{command_name}.txt"
            lines = lines_for(ci_name, command_name)
            with open(filename, "wt") as file:
                file.writelines(line + "\n" for line in lines)


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
    for mount in command.volume_mounts('docker'):
        lines.append(lc(f"{tab}--volume {mount}"))

    # The merkely-pipe volume-mount is always required
    lines.append(lc(tab + "--volume ${YOUR_MERKELY_PIPE}:/data/Merkelypipe.json"))

    # The name of the docker image
    lines.append(f"{tab}merkely/change")

    return lines


yml_name_texts = {
    'declare_pipeline': 'Declare Merkely Pipeline',
    'log_approval': 'Log Approval in Merkely',
    'log_artifact': 'Log Docker Image in Merkely',
    'log_deployment': 'Log Deployment in Merkely',
    'log_evidence': 'Log Evidence in Merkely',
    'log_test': 'Log JUnit XML evidence in Merkely',
    'control_deployment': '...'
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
    for mount in command.volume_mounts('docker'):
        lines.append(lc(f"{tab}--volume {mount}"))
    lines.append(lc(tab + "--volume ${YOUR_MERKELY_PIPE}:/data/Merkelypipe.json"))
    lines.append(f"{tab}merkely/change")
    return lines


def lines_for_github(command_name):
    ci_indent = " " * 8
    def lc(string):
        line_continuation = "\\"
        return f"{ci_indent}{string} {line_continuation}"

    tab = " " * 4
    def env(var):
        if var.name == "MERKELY_COMMAND":
            value = var.value
        else:
            value = '"' + "${" + var.name + "}" + '"'
        return lc(f'{tab}--env {var.name}={value}')

    command = command_for(command_name)
    lines = [
        "...",
        "jobs:",
        "  build:",
        "    runs-on: ubuntu-20.04",
        "    steps:",
        "    ...",
        "    - name: {}".format(yml_name_texts[command_name]),
        "      ...",
        "      run: |",
        lc("docker run"),
    ]
    for var in command.merkely_env_vars:
        lines.append(env(var))
    # Add each CI env-var used in a MERKELY_XXXX env-var default
    # eg GITHUB_REPOSITORY
    for name in command.ci_env_var_names('github'):
        lines.append(lc(f"{tab}--env {name}"))
    lines.append(lc(f"{tab}--rm"))
    for mount in command.volume_mounts('github'):
        lines.append(lc(f"{tab}--volume {mount}"))
    lines.append(lc(tab + "--volume ${YOUR_MERKELY_PIPE}:/data/Merkelypipe.json"))
    lines.append(f"{ci_indent}{tab}merkely/change")
    return lines


def lines_for_bitbucket(command_name):
    ci_indent = " " * 8
    def lc(string):
        # bitbucket uses leading - to indicate start of a command
        # and a \ line continuation is not needed.
        return f"{ci_indent}{string} "
    tab = " " * 4
    def env(var):
        if var.name == "MERKELY_COMMAND":
            value = var.value
        else:
            value = '"' + "${" + var.name + "}" + '"'
        return lc(f'{tab}--env {var.name}={value}')

    command = command_for(command_name)
    lines = [
        "image: atlassian/default-image:2",
        "...",
        "pipelines:",
        "  default:",
        "    ...",
        "    - step:",
        "        name: {}".format(yml_name_texts[command_name]),
        "        script:",
        f"  {ci_indent}- docker run",
    ]
    for var in command.merkely_env_vars:
        lines.append(env(var))
    # Add each CI env-var used in a MERKELY_XXXX env-var default
    # eg BITBUCKET_BITBUCKET_REPO_SLUG
    for name in command.ci_env_var_names('bitbucket'):
        lines.append(lc(f"{tab}--env {name}"))
    lines.append(lc(f"{tab}--rm"))
    for mount in command.volume_mounts('bitbucket'):
        lines.append(lc(f"{tab}--volume {mount}"))
    lines.append(lc(tab + "--volume ${YOUR_MERKELY_PIPE}:/data/Merkelypipe.json"))
    lines.append(f"{ci_indent}{tab}merkely/change")
    return lines


def command_for(name):
    cls = Command.named(name)
    env = {"MERKELY_COMMAND": name}
    external = External(env=env)
    return cls(external)


def make_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

