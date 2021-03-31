from errors import ChangeError
from commands import Command
from lib.http import *
import os


def run(external):
    name = external.env.get("MERKELY_COMMAND", None)
    if name is None:
        raise ChangeError("MERKELY_COMMAND environment-variable is not set.")
    print(f"MERKELY_COMMAND={name}")
    klass = Command.named(name)
    command = klass(external)
    for env_var in command.merkely_env_vars:
        env_var.value

    method, url, payload, callback = command()
    api_token = command.api_token.value
    dry_run = in_dry_run(external.env)
    if method == 'GET':
        print("Getting json:")
        print("From this url: " + url)
        response = http_get_json(url=url, api_token=api_token, dry_run=dry_run)
    if method == 'PUT':
        print("Putting this payload:")
        print(pretty_json(payload))
        print("To this url: " + url)
        response = http_put_payload(url=url, payload=payload, api_token=api_token, dry_run=dry_run)
    if method == 'POST':
        print("Posting this payload:")
        print(pretty_json(payload))
        print("To this url: " + url)
        response = http_post_payload(url=url, payload=payload, api_token=api_token, dry_run=dry_run)

    if not dry_run and callback is not None:
        return callback(response)
    else:
        return method, url, payload


def in_dry_run(env):
    return env.get('MERKELY_DRY_RUN', 'FALSE') == "TRUE"


def main(external):
    try:
        run(external)
        print('Success')
        return 0
    except ChangeError as exc:
        print(f"Error: {str(exc)}")
        return 144


