from docutils import nodes
from docutils.parsers.rst import Directive
from commands import Command, External


class DescribeCommand(Directive):

    has_content = True

    def run(self):
        args = self.content[0].split()
        name = args[0]
        description_type = args[1]
        ci = args[2]
        if description_type == "summary":
            return summary(name, ci)
        if description_type == "invocation_full":
            return invocation(name, 'full', ci)
        if description_type == "invocation_minimum":
            return invocation(name, 'minimum', ci)
        if description_type == "parameters":
            return parameters(name, ci)
        return []


def summary(name, ci):
    return [nodes.paragraph(text=command_for(name).summary(ci))]


def invocation(name, kind, ci):
    return [nodes.literal_block(text=docker_run_string(name, kind, ci))]


def docker_run_string(name, kind, ci):
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

    def lcnl(string):
        # bitbucket uses leading - to indicate start of a command
        # and a \ line continuation is not needed.
        if ci == 'bitbucket':
            line_continuation = ""
        else:
            line_continuation = "\\"
        newline = "\n"
        return f"{ci_indent}{string} {line_continuation}{newline}"

    def env(var):
        if var.name == "MERKELY_COMMAND":
            value = var.value
        else:
            value = '"' + "${" + var.name + "}" + '"'
        return lcnl(f'{tab}--env {var.name}={value}')

    # CI .yml 'context'
    drs = ci_yml

    # The docker run command
    if ci == 'bitbucket':
        drs += "docker run\n"
    else:
        drs += lcnl("docker run")

    # With each --env MERKELY_XXXX=...
    for var in command.merkely_env_vars:
        if kind == 'full':
            drs += env(var)
        if kind == 'minimum' and var.is_required:
            drs += env(var)

    # With each CI env-var used in a MERKELY_XXXX env-var default
    for name in command.ci_env_var_names(ci):
        drs += lcnl(f"{tab}--env {name}")

    # The --rm docker run option
    drs += lcnl(f"{tab}--rm")

    # The docker run volume-mount options, if any
    for mount in command.volume_mounts(ci):
        drs += lcnl(f"{tab}--volume {mount}")

    # The merkely-pipe volume-mount is always required
    drs += lcnl(tab + "--volume ${YOUR_MERKELY_PIPE}:/data/Merkelypipe.json")

    # The name of the docker image
    drs += f"{ci_indent}{tab}merkely/change"

    return drs


def ci_yml_prefix(ci, name_text):
    if ci == 'docker':
        return 0, ""
    if ci == 'bitbucket':
        return 8, "\n".join([
            "image: atlassian/default-image:2",
            "...",
            "pipelines:",
            "  default:",
            "    ...",
            "    - step:",
            "        name: {}".format(name_text),
            "        script:",
            "          - ",
        ])
    if ci == 'github':
        return 8, "\n".join([
            "...",
            "jobs:",
            "  build:",
            "    runs-on: ubuntu-20.04",
            "    steps:",
            "    ...",
            "    - name: {}".format(name_text),
            "      ...",
            "      run: |",
            "",
        ])


def parameters(name, ci):
    return [env_vars_to_table(command_for(name).merkely_env_vars, ci)]


def command_for(name):
    cls = Command.named(name)
    env = {"MERKELY_COMMAND": name}
    external = External(env=env)
    return cls(external)


def env_vars_to_table(env_vars, ci):
    table = nodes.table()
    tgroup = nodes.tgroup(cols=3)
    table += tgroup

    colspec = nodes.colspec()
    tgroup += colspec
    tgroup += colspec
    tgroup += colspec

    thead = nodes.thead()
    tgroup += thead
    row = nodes.row()
    row += nodes.entry("", nodes.paragraph(text="NAME"))
    row += nodes.entry("", nodes.paragraph(text="Required?"))
    row += nodes.entry("", nodes.paragraph(text="Notes"))
    thead += row

    tbody = nodes.tbody()
    for env_var in env_vars:
        row = nodes.row()
        row += nodes.entry("", nodes.paragraph(text=env_var.name))
        if env_var.is_required(ci):
            required = 'yes'
        else:
            required = 'no'
        row += nodes.entry("", nodes.paragraph(text=required))
        notes = env_var.notes(ci)
        if notes == "<FINGERPRINT_LINK>":
            ref = "../../fingerprints/docker_fingerprint.html"
            para = nodes.paragraph(text="")
            para += nodes.reference('', 'Fingerprint', internal=False, refuri=ref)
            row += nodes.entry("", para)
        else:
            row += nodes.entry("", nodes.paragraph(text=notes))
        tbody += row
    tgroup += tbody
    return table


def setup(app):
    app.add_directive("describe_command", DescribeCommand)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }