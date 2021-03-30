from docutils import nodes
from docutils.parsers.rst import Directive
from commands import Command, External
import requests
import subprocess


class DescribeCommand(Directive):

    has_content = True

    def run(self):
        args = self.content[0].split()
        command_name = args[0]
        description_type = args[1]
        ci_name = args[2]
        if description_type == "summary":
            return summary(command_name, ci_name)
        if description_type == "invocation_full":
            return invocation_full(command_name, ci_name)
        if description_type == "invocation_minimum":
            return invocation_minimum(command_name)
        if description_type == "parameters":
            return parameters(command_name, ci_name)
        return []


def summary(command_name, ci_name):
    return [nodes.paragraph(text=command_for(command_name).doc_summary(ci_name))]


# The Makefile volume-mounts docs.merkely.com/ to docs/
REFERENCE_DIR = '/docs/build/reference'


def invocation_full(command_name, ci_name):
    filename = f"{REFERENCE_DIR}/{ci_name}/{command_name}.txt"
    with open(filename, "rt") as file:
        text = file.read()

    div = nodes.container()
    div += literal_block_link(command_name, ci_name)
    div += nodes.literal_block(text=text)
    div += parameters(command_name, ci_name)

    # Add bootstrap "tab-pane" to connect to
    #    <ul class="nav nav-tabs">...</ul>
    # inside each command's .rst file

    div_classes = [ci_name, "tab-pane"]
    if ci_name == "docker":
        div_classes.append("active")
    div.update_basic_atts({
        "ids": [ci_name],
        "classes": div_classes
    })
    return [div]


def invocation_minimum(command_name):
    filename = f"{REFERENCE_DIR}/min/{command_name}.txt"
    with open(filename, "rt") as file:
        text = file.read()
    return [nodes.literal_block(text=text)]


def parameters(command_name, ci_name):
    command = command_for(command_name)
    env_vars = command.merkely_env_vars
    return [env_vars_to_table(env_vars, ci_name, command_name)]


def command_for(name):
    cls = Command.named(name)
    env = {"MERKELY_COMMAND": name}
    external = External(env=env)
    return cls(external)


def env_vars_to_table(env_vars, ci_name, command_name):
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
    row += nodes.entry("", nodes.paragraph(text="ENV_VAR_NAME"))
    row += nodes.entry("", nodes.paragraph(text="Required?"))
    row += nodes.entry("", nodes.paragraph(text="Notes"))
    thead += row

    tbody = nodes.tbody()
    for env_var in env_vars:
        row = nodes.row()
        row += nodes.entry("", nodes.paragraph(text=env_var.name))
        if env_var.is_required(ci_name):
            required = 'yes'
        else:
            required = 'no'
        row += nodes.entry("", nodes.paragraph(text=required))
        note = env_var.doc_note(ci_name, command_name)
        if note == "<FINGERPRINT_LINK>":
            ref = "../../fingerprints/docker_fingerprint.html"
            para = nodes.paragraph(text="")
            para += nodes.reference('', 'Fingerprint', internal=False, refuri=ref)
            row += nodes.entry("", para)
        else:
            row += nodes.entry("", nodes.paragraph(text=note))
        tbody += row
    tgroup += tbody
    return table


def literal_block_link(command_name, ci_name):
    change_makefile_url = 'https://github.com/merkely-development/change/blob/master/Makefile'
    if command_name == 'approve_deployment':
        # Currently only one 'docker' use
        ref = change_makefile_url
    elif ci_name == 'docker':
        ref = change_makefile_url
    elif ci_name == 'bitbucket':
        ref = 'https://bitbucket.org/merkely/loan-calculator/src/master/bitbucket-pipelines.yml'
    elif ci_name == 'github':
        workflow_url = 'https://github.com/merkely-development/loan-calculator/blob/master/.github/workflows'
        if command_name == 'request_approval':
            url = f'{workflow_url}/request_approval.yml'
            #ref = github_request_approval_line_url('MERKELY_COMMAND: request_approval')
            #ref = bitbucket_request_approval_line_url('MERKELY_COMMAND: request_approval')
            ref = url
        elif command_name == 'control_deployment':
            ref = f'{workflow_url}/deploy_to_production.yml'
        else:
            ref = f'{workflow_url}/master_pipeline.yml'
    para = nodes.paragraph(text="")
    para += nodes.reference('', 'See an example of use in a git repo.', internal=False, refuri=ref)
    para.update_basic_atts({
        "classes": ['literal-block-link']
    })
    return para


# Working towards URL's that target individual lines...
def github_request_approval_line_url(search_text):
    org = 'merkely-development'
    repo = 'loan-calculator'
    raw_url = f'https://raw.githubusercontent.com/{org}/{repo}/master/.github/workflows/request_approval.yml'
    url = f'https://github.com/{org}/{repo}/blob/master/.github/workflows/request_approval.yml'
    lines = requests.get(raw_url).text.splitlines()
    indices = [i for i, line in enumerate(lines) if search_text in line]
    index = indices[0] + 1
    return f'{url}#L{index}'


def bitbucket_request_approval_line_url(search_text):
    org = 'merkely'
    repo = 'loan-calculator'
    base_url = f"https://bitbucket.org/{org}/{repo}"
    bytes = subprocess.check_output(['git', 'ls-remote', f"{base_url}/src/master"])
    stdout = bytes.decode('utf-8')
    long_sha = stdout.split()[0]  # eg 1d513d611f297e61a97bf766388f0c9df6ff13d4
    short_sha = long_sha[:7]      # eg 1d513d6
    raw_url = f"{base_url}/raw/{short_sha}/bitbucket-pipelines.yml"
    lines = requests.get(raw_url).text.splitlines()
    indices = [i for i, line in enumerate(lines) if search_text in line]
    index = indices[0] + 1
    return f"{base_url}/src/{short_sha}/bitbucket-pipelines.yml#lines-{index}"


def setup(app):
    app.add_directive("describe_command", DescribeCommand)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }