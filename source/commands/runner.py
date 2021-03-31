from errors import ChangeError
from commands import Command
from lib.http import *


def run(external):
    name = external.env.get("MERKELY_COMMAND", None)
    if name is None:
        raise ChangeError("MERKELY_COMMAND environment-variable is not set.")
    print(f"MERKELY_COMMAND={name}")
    klass = Command.named(name)
    command = klass(external)
    for env_var in command.merkely_env_vars:
        env_var.value

    api_token = command.api_token.value
    method, url, payload, callback = command()
    if method == 'GET':
        print("Getting json:")
        print("From this url: " + url)
        response = http_get_json(url, api_token)
    if method == 'PUT':
        print("Putting this payload:")
        print(pretty_json(payload))
        print("To this url: " + url)
        response = http_put_payload(url, payload, api_token)
    if method == 'POST':
        print("Posting this payload:")
        print(pretty_json(payload))
        print("To this url: " + url)
        response = http_post_payload(url, payload, api_token)

    if callback is not None:
        return callback(response)
    else:
        return method, url, payload


def main(external):
    try:
        run(external)
        print('Success')
        return 0
    except ChangeError as exc:
        print(f"Error: {str(exc)}")
        return 144


