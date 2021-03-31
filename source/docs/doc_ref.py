import requests
import subprocess

REF_FILES = {}

"""
change_makefile_url = 'https://github.com/merkely-development/change/blob/master/Makefile'
if ci_name == 'docker':
    ref = change_makefile_url
elif ci_name == 'bitbucket':
    ref = 'https://bitbucket.org/merkely/loan-calculator/src/master/bitbucket-pipelines.yml'
elif ci_name == 'github':
    workflow_url = 'https://github.com/merkely-development/loan-calculator/blob/master/.github/workflows'
    if command_name == 'control_deployment':
        ref = f'{workflow_url}/deploy_to_production.yml'
    else:
        ref = f'{workflow_url}/master_pipeline.yml'
"""


def curl_ref_files():
    """
    Called from docs.merkely.com/source/conf.py
    Loads files that are url ref targets for each command
    (eg 'log_test') in each supported CI system (eg 'bitbucket')
    """
    curlers = [
        github_loan_calculator_master_line_ref,
        github_loan_calculator_request_approval_line_ref,
        github_deploy_to_production_line_ref,
        bitbucket_loan_calculator_line_ref,
        docker_change_makefile_line_ref,
    ]
    for f in curlers:
        json = f('url_lines')
        REF_FILES[json["base_url"]] = json


def docker_change_makefile_line_ref(search_text):
    org = 'merkely-development'
    repo = 'change'
    branch = 'master'
    filename = 'Makefile'
    base_url = f'https://raw.githubusercontent.com/{org}/{repo}/{branch}/{filename}'
    if search_text == 'url_lines':
        lines = requests.get(base_url).text.splitlines()
        return {
            "base_url": base_url,
            "ref_url": f'https://github.com/{org}/{repo}/blob/{branch}/{filename}',
            "lines": lines
        }
    json = REF_FILES[base_url]
    lines = json["lines"]
    url = json['ref_url']
    indices = [i for i, line in enumerate(lines) if search_text == line.strip()]
    assert len(indices) == 1
    index = indices[0] + 1
    return f'{url}#L{index}'


def github_loan_calculator_master_line_ref(search_text):
    org = 'merkely-development'
    repo = 'loan-calculator'
    branch = 'master'
    dir = '.github/workflows'
    filename = 'master_pipeline.yml'
    base_url = f'https://raw.githubusercontent.com/{org}/{repo}/{branch}/{dir}/{filename}'
    if search_text == 'url_lines':
        lines = requests.get(base_url).text.splitlines()
        return {
            "base_url": base_url,
            "ref_url": f'https://github.com/{org}/{repo}/blob/{branch}/{dir}/{filename}',
            "lines": lines
        }
    json = REF_FILES[base_url]
    lines = json["lines"]
    url = json['ref_url']
    indices = [i for i, line in enumerate(lines) if search_text in line]
    index = indices[0] + 1
    return f'{url}#L{index}'


def github_loan_calculator_request_approval_line_ref(search_text):
    org = 'merkely-development'
    repo = 'loan-calculator'
    branch = 'master'
    dir = '.github/workflows'
    filename = 'request_approval.yml'
    base_url = f'https://raw.githubusercontent.com/{org}/{repo}/{branch}/{dir}/{filename}'
    if search_text == 'url_lines':
        lines = requests.get(base_url).text.splitlines()
        return {
            "base_url": base_url,
            "ref_url": f'https://github.com/{org}/{repo}/blob/{branch}/{dir}/{filename}',
            "lines": lines
        }
    json = REF_FILES[base_url]
    lines = json["lines"]
    url = json['ref_url']
    indices = [i for i, line in enumerate(lines) if search_text in line]
    index = indices[0] + 1
    return f'{url}#L{index}'


def github_deploy_to_production_line_ref(search_text):
    org = 'merkely-development'
    repo = 'loan-calculator'
    branch = 'master'
    dir = '.github/workflows'
    filename = 'deploy_to_production.yml'
    base_url = f'https://raw.githubusercontent.com/{org}/{repo}/{branch}/{dir}/{filename}'
    if search_text == 'url_lines':
        lines = requests.get(base_url).text.splitlines()
        return {
            "base_url": base_url,
            "ref_url": f'https://github.com/{org}/{repo}/blob/{branch}/{dir}/{filename}',
            "lines": lines
        }
    json = REF_FILES[base_url]
    lines = json["lines"]
    url = json['ref_url']
    indices = [i for i, line in enumerate(lines) if search_text in line]
    index = indices[0] + 1
    return f'{url}#L{index}'


def bitbucket_loan_calculator_line_ref(search_text):
    org = 'merkely'
    repo = 'loan-calculator'
    base_url = f"https://bitbucket.org/{org}/{repo}"
    filename = 'bitbucket-pipelines.yml'
    if search_text == 'url_lines':
        bytes = subprocess.check_output(['git', 'ls-remote', f"{base_url}/src/master"])
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
    json = REF_FILES[base_url]
    lines = json["lines"]
    url = json["ref_url"]
    indices = [i for i, line in enumerate(lines) if search_text in line]
    index = indices[0] + 1
    return f"{url}#lines-{index}"
