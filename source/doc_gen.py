from pathlib import Path
from commands import Command

# The Makefile volume-mounts docs.merkely.com/ to docs/
REFERENCE_DIR = '/docs/source/reference'


def auto_generate():
    command_names = sorted(Command.names())
    command_names.remove('control_pull_request')  # Currently only github

    rst = reference_index_rst(command_names)
    with open(f'{REFERENCE_DIR}/index.rst', 'wt') as file:
        file.write(rst)

    for command_name in command_names:
        rst = reference_command_rst(command_name)
        with open(f'{REFERENCE_DIR}/{command_name}.rst', 'wt') as file:
            file.write(rst)


def reference_index_rst(command_names):
    index = "\n".join([
        f".. This file was auto-generated from {__file__}",
        "",
        ".. toctree::",
        "   :maxdepth: 1",
        "",
    ])
    for command_name in command_names:
        tab = " " * 3
        index += f"\n{tab}{command_name}"
    return index


def reference_command_rst(command_name):
    ci_names = ['bitbucket', 'github']
    tab = " " * 3
    title = " ".join(list(s.capitalize() for s in command_name.split('_')))
    rst = "\n".join([
        f".. This file was auto-generated from {__file__}",
        "",
        title,
        "-" * len(title),
        "",
        f".. describe_command:: {command_name} summary unused",
        "",
        ".. raw:: html",
        "",
        f'{tab}<ul class="nav nav-tabs">',
        f'{tab}{tab}<li class="active"><a data-toggle="tab" href="#docker">Docker</a></li>',
        "",
    ])

    for ci_name in ci_names:
        cap = ci_name.capitalize()
        rst += f'{tab}{tab}<li><a data-toggle="tab" href="#{ci_name}">{cap}</a></li>\n'

    rst += "\n".join([
        f"{tab}</ul>",
        f'{tab}<div class="tab-content">',
        "",
        f".. describe_command:: {command_name} invocation_full docker",
        "",
    ])

    for ci_name in ci_names:
        rst += f".. describe_command:: {command_name} invocation_full {ci_name}\n"

    rst += "\n".join([
        "",
        ".. raw:: html",
        "",
        f"{tab}</div>",
    ])

    return rst
