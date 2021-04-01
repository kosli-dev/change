from errors import ChangeError
from commands import Command
from lib.http import *
import json


def run(external):
    name = external.env.get("MERKELY_COMMAND", None)
    if name is None:
        raise ChangeError("MERKELY_COMMAND environment-variable is not set.")
    print(f"MERKELY_COMMAND={name}")
    klass = Command.named(name)
    command = klass(external)
    for env_var in command.merkely_env_vars:
        env_var.value  # check required env-vars are set

    method, url, payload, callback = command()
    api_token = command.api_token.value
    dry_run = command.in_dry_run
    if method == 'GET':
        print("Getting json:")
        print("From this url: " + url)
        if dry_run:
            print("DRY RUN: Get not performed")
            response = None
        else:
            response = http_get_json(url, api_token)
    if method == 'PUT':
        print("Putting this payload:")
        print(pretty_json(payload))
        print("To this url: " + url)
        if dry_run:
            print("DRY RUN: Put not sent")
            response = None
        else:
            response = http_put_payload(url, payload, api_token)
    if method == 'POST':
        print("Posting this payload:")
        print(pretty_json(payload))
        print("To this url: " + url)
        if dry_run:
            print("DRY RUN: Post not sent")
            response = None
        else:
            response = http_post_payload(url, payload, api_token)

    if not dry_run and callback is not None:
        raise_unless_success(response)
        return callback(response)
    else:
        return method, url, payload


def raise_unless_success(response):
    # Eg https://github.com/merkely-development/change/runs/1961998055?check_suite_focus=true
    status_code = response.status_code
    if status_code in [200, 201]:
        print(response.text)
    else:
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


