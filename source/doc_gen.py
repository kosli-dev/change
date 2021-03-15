from pathlib import Path
from commands import Command

# The Makefile volume-mounts docs.merkely.com/ to docs/
REFERENCE_DIR = '/docs/source/reference'


def auto_generate():
    ci_names = ['generic_docker', 'bitbucket_pipeline', 'github_actions']
    create_reference_rst_files(ci_names)
    create_reference_ci_rst_files(ci_names)
    create_reference_ci_dir(ci_names)


def create_reference_rst_files(ci_names):
    index = "\n".join([
        f".. This file was auto-generated from {__file__}",
        "",
    ])
    for ci_name in ci_names:
        index += index_ci_entry(ci_name)
    with open(f'{REFERENCE_DIR}/index.rst', 'wt') as file:
        file.write(index)


def index_ci_entry(ci_name):
    title = " ".join(list(s.capitalize() for s in ci_name.split('_')))
    return "\n".join([
        f".. This file was auto-generated from {__file__}",
        "",
        ".. toctree::",
        "   :maxdepth: 1",
        f"   :caption: {title}:",
        "",
        f"   {ci_name}",
        "",
    ])


def create_reference_ci_rst_files(ci_names):
    for ci_name in ci_names:
        title = " ".join(list(s.capitalize() for s in ci_name.split('_')))
        rst = "\n".join([
            f".. This file was auto-generated from {__file__}",
            "",
            title,
            "-" * len(title),
            "",
            ".. toctree::",
            "   :maxdepth: 1",
            "",
            f"   {ci_name}/index"
        ])
        with open(f'{REFERENCE_DIR}/{ci_name}.rst', 'wt') as file:
            file.write(rst)


def create_reference_ci_dir(ci_names):
    command_names = sorted(Command.names())
    command_names.remove('control_pull_request')  # Currently only github
    for ci_name in ci_names:
        dir = f"{REFERENCE_DIR}/{ci_name}"
        Path(dir).mkdir(exist_ok=True)
        index = "\n".join([
            f".. This file was auto-generated from {__file__}",
            "",
            ".. toctree::",
            "   :maxdepth: 1",
            "",
        ])
        index += "\n"
        for name in command_names:
            index += f"   {name}\n"
            create_reference_ci_command(ci_name, name)

        with open(f'{REFERENCE_DIR}/{ci_name}/index.rst', 'wt') as file:
            file.write(index)


def create_reference_ci_command(ci_name, command_name):
    title = " ".join(list(s.capitalize() for s in command_name.split('_')))
    if ci_name == 'generic_docker':
        short_ci_name = 'docker'
    elif ci_name == 'bitbucket_pipeline':
        short_ci_name = 'bitbucket'
    elif ci_name == 'github_actions':
        short_ci_name = 'github'
    rst = "\n".join([
        f".. This file was auto-generated from {__file__}",
        "",
        f"{title}",
        "=" * len(title),
        f".. describe_command:: {command_name} summary {short_ci_name}",
        "",
        "Invocation",
        "----------",
        f".. describe_command:: {command_name} invocation_full {short_ci_name}",
        "",
        "Parameters",
        "----------",
        f".. describe_command:: {command_name} parameters {short_ci_name}",
        "",
    ])
    with open(f'{REFERENCE_DIR}/{ci_name}/{command_name}.rst', 'wt') as file:
        file.write(rst)

