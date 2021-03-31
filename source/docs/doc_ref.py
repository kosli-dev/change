import requests
import subprocess

CURL_COMMAND = 'curl_ref_lines'
REF_FILES = {}


def curl_ref_files():
    """
    Called from docs.merkely.com/source/conf.py
    Loads files that are url ref targets for each command
    (eg 'log_test') in each supported CI system (eg 'bitbucket').
    See Command.doc_ref()
    """
    curlers = [
        github_loan_calculator_master_pipeline_line_ref,
        github_loan_calculator_request_approval_line_ref,
        github_loan_calculator_deploy_to_production_line_ref,
        bitbucket_loan_calculator_line_ref,
        docker_change_makefile_line_ref,
    ]
    for f in curlers:
        json = f(CURL_COMMAND)
        REF_FILES[json["base_url"]] = json

"""
Custom functions that return the URL <a ref=""> targets which appear
above the live-documentation fragment for a command being used in
a file in a public git repo. Target specific line numbers. 
Note that loan-calculator's Github Action pipeline is split into three files
because Github Actions does not yet support manual approval steps.
"""


def docker_change_makefile_line_ref(search_text):
    return github_loan_calculator_line_ref(search_text, 'Makefile')


def github_loan_calculator_master_pipeline_line_ref(search_text):
    return github_loan_calculator_line_ref(search_text, 'master_pipeline.yml')


def github_loan_calculator_request_approval_line_ref(search_text):
    return github_loan_calculator_line_ref(search_text, 'request_approval.yml')


def github_loan_calculator_deploy_to_production_line_ref(search_text):
    return github_loan_calculator_line_ref(search_text, 'deploy_to_production.yml')


def github_loan_calculator_line_ref(search_text, filename):
    org = 'merkely-development'
    if filename == 'Makefile':
        repo = 'change'
        dir = ''
    else:
        repo = 'loan-calculator'
        dir = '.github/workflows/'
    branch = 'master'
    base_url = f'https://raw.githubusercontent.com/{org}/{repo}/{branch}/{dir}{filename}'
    if search_text == CURL_COMMAND:
        lines = requests.get(base_url).text.splitlines()
        return {
            "base_url": base_url,
            "ref_url": f'https://github.com/{org}/{repo}/blob/{branch}/{dir}{filename}',
            "lines": lines
        }
    url, n = line_number(search_text, base_url)
    return f"{url}#L{n}"


def bitbucket_loan_calculator_line_ref(search_text):
    org = 'merkely'
    repo = 'loan-calculator'
    branch = 'master'
    base_url = f"https://bitbucket.org/{org}/{repo}"
    filename = 'bitbucket-pipelines.yml'
    if search_text == CURL_COMMAND:
        # On bitbucket, raw_url needs a commit sha on master
        bytes = subprocess.check_output(['git', 'ls-remote', f"{base_url}/src/{branch}"])
        stdout = bytes.decode('utf-8')
        long_sha = stdout.split()[0]  # eg 1d513d611f297e61a97bf766388f0c9df6ff13d4
        short_sha = long_sha[:7]      # eg 1d513d6
        raw_url = f"{base_url}/raw/{short_sha}/{filename}"
        lines = requests.get(raw_url).text.splitlines()
        return {
            "base_url": base_url,
            "ref_url": f"{base_url}/src/{short_sha}/{filename}",
            "lines": lines
        }
    url, n = line_number(search_text, base_url)
    return f"{url}#lines-{n}"


def line_number(search_text, base_url):
    json = REF_FILES[base_url]
    lines = json["lines"]
    url = json["ref_url"]
    indices = [i for i, line in enumerate(lines) if search_text == line.strip()]
    assert len(indices) > 0
    return url, indices[0] + 1  # Human counting is 1-based
