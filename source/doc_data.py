import os
from commands import Command, External


def auto_generate():
    """
    Generates JSON files containing documentation source for each
    command (eg 'log_test') in each supported CI system (eg 'bitbucket')
    """
    command_names = [
        'declare_pipeline',
        'log_approval',
        'log_artifact',
        'log_deployment',
        'log_evidence',
        'log_test',
        'control_deployment',
    ]
    ci_names = [
        'docker',
        'github',
        'bitbucket'
    ]

    # The Makefile volume-mounts docs.merkely.com/ to docs/
    reference_dir = '/docs/build/reference'
    make_dir(reference_dir)
    make_dir(f"{reference_dir}/bitbucket")
    make_dir(f"{reference_dir}/docker")
    make_dir(f"{reference_dir}/github")
    make_dir(f"{reference_dir}/min")

    for ci_name in ci_names:
        for command_name in command_names:
            filename = f"{reference_dir}/{ci_name}/{command_name}.txt"
            lines = lines_for(ci_name, command_name)
            with open(filename, "wt") as file:
                file.writelines(line + "\n" for line in lines)

    for command_name in command_names:
        min_filename = f"{reference_dir}/min/{command_name}.txt"
        min_lines = min_lines_for(command_name)
        with open(min_filename, "wt") as file:
            file.writelines(line + "\n" for line in min_lines)


def make_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def lines_for(ci, name):
    # ci == ci name, eg 'bitbucket'
    # name == command name, eg 'log_test'
    command = command_for(name)
    tab = "    "
    yml_name_texts = {
        'declare_pipeline': 'Declare Merkely Pipeline',
        'log_approval': 'Log Approval in Merkely',
        'log_artifact': 'Log Docker Image in Merkely',
        'log_deployment': 'Log Deployment in Merkely',
        'log_evidence': 'Log Evidence in Merkely',
        'log_test': 'Log JUnit XML evidence in Merkely',
        'control_deployment': '...'
    }
    if name in yml_name_texts:
        yml_name_text = yml_name_texts[name]
    else:
        yml_name_text = '...'

    n, ci_yml = ci_yml_prefix(ci, yml_name_text)
    ci_indent = ' ' * n

    def lc(string):
        # bitbucket uses leading - to indicate start of a command
        # and a \ line continuation is not needed.
        if ci == 'bitbucket':
            line_continuation = ""
        else:
            line_continuation = "\\"
        return f"{ci_indent}{string} {line_continuation}"

    def env(var):
        if var.name == "MERKELY_COMMAND":
            value = var.value
        else:
            value = '"' + "${" + var.name + "}" + '"'
        return lc(f'{tab}--env {var.name}={value}')

    # CI .yml 'context'
    lines = ci_yml

    # The docker run command
    if ci == 'bitbucket':
        lines.append(f"  {ci_indent}- docker run")
    else:
        lines.append(lc("docker run"))

    # With each --env MERKELY_XXXX=...
    for var in command.merkely_env_vars:
        lines.append(env(var))

    # With each CI env-var used in a MERKELY_XXXX env-var default
    for name in command.ci_env_var_names(ci):
        lines.append(lc(f"{tab}--env {name}"))

    # The --rm docker run option
    lines.append(lc(f"{tab}--rm"))

    # The docker run volume-mount options, if any
    for mount in command.volume_mounts(ci):
        lines.append(lc(f"{tab}--volume {mount}"))

    # The merkely-pipe volume-mount is always required
    lines.append(lc(tab + "--volume ${YOUR_MERKELY_PIPE}:/data/Merkelypipe.json"))

    # The name of the docker image
    lines.append(f"{ci_indent}{tab}merkely/change")

    return lines


def min_lines_for(name):
    # name == command name, eg 'log_test'
    command = command_for(name)
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

    lines = [ lc("docker run") ]
    # With each --env MERKELY_XXXX=...
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


def ci_yml_prefix(ci, name_text):
    if ci == 'docker':
        return 0, []
    if ci == 'bitbucket':
        return 8, [
            "image: atlassian/default-image:2",
            "...",
            "pipelines:",
            "  default:",
            "    ...",
            "    - step:",
            "        name: {}".format(name_text),
            "        script:",
        ]
    if ci == 'github':
        return 8, [
            "...",
            "jobs:",
            "  build:",
            "    runs-on: ubuntu-20.04",
            "    steps:",
            "    ...",
            "    - name: {}".format(name_text),
            "      ...",
            "      run: |",
        ]


def command_for(name):
    cls = Command.named(name)
    env = {"MERKELY_COMMAND": name}
    external = External(env=env)
    return cls(external)
