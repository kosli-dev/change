

def core_env_vars(command):
    return {
        "MERKELY_COMMAND": command,
        "MERKELY_API_TOKEN": "MY_SUPER_SECRET_API_TOKEN",
        "MERKELY_HOST": "https://app.merkely.com",
        "MERKELY_OWNER": "acme",
        "MERKELY_PIPELINE": "lib-controls-test-pipeline",
    }
