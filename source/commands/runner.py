from errors import ChangeError
from commands import Command
from lib.http import *
import json


def run(external):
    stdout = external.stdout
    name = external.env.get("MERKELY_COMMAND", None)
    if name is None:
        raise ChangeError("MERKELY_COMMAND environment-variable is not set.")

    stdout.print(f"MERKELY_COMMAND={name}")
    klass = Command.named(name)
    command = klass(external)
    for env_var in command.merkely_env_vars:
        env_var.value  # check required env-vars are set

    method, url, payload, callback = command()

    dry_run = in_dry_run(command)
    api_token = command.api_token.value

    if method == 'GET':
        stdout.print("Getting json:")
        stdout.print("From this url: " + url)
        if dry_run:
            stdout.print("DRY RUN: Get not performed")
            response = None
        else:
            response = Http(stdout).get_json(url, api_token)

    if method == 'PUT':
        stdout.print("Putting this payload:")
        stdout.print(pretty_json(payload))
        stdout.print("To this url: " + url)
        if dry_run:
            stdout.print("DRY RUN: Put not sent")
            response = None
        else:
            response = Http(stdout).put_payload(url, payload, api_token)

    if method == 'POST':
        stdout.print("Posting this payload:")
        stdout.print(pretty_json(payload))
        stdout.print("To this url: " + url)
        if dry_run:
            stdout.print("DRY RUN: Post not sent")
            response = None
        else:
            response = Http(stdout).post_payload(url, payload, api_token)

    if response is not None:
        raise_unless_success(response)
        stdout.print(response.text)

    if not dry_run and callback is not None:
        return callback(response)
    else:
        return method, url, payload


def in_dry_run(command):
    global_off = command.api_token.value == 'DRY_RUN'
    local_off = command.dry_run.value == "TRUE"
    return global_off or local_off


def raise_unless_success(response):
    # Eg https://github.com/merkely-development/change/runs/1961998055?check_suite_focus=true
    status_code = response.status_code
    if status_code not in [200, 201]:
        message = f"HTTP status=={status_code}\n{response.text}"
        raise ChangeError(message)


def pretty_json(payload):
    return json.dumps(payload, sort_keys=True, indent=4)


def main(external):
    try:
        run(external)
        print('Success')
        return 0
    except ChangeError as exc:
        print(f"Error: {str(exc)}")
        return 144


