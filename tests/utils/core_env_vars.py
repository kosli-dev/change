

def core_env_vars(command=None):
    if command is None:
        command = "declare_pipeline"
    return {
        "MERKELY_COMMAND": command,
        "MERKELY_API_TOKEN": "MY_SUPER_SECRET_API_TOKEN",
        "MERKELY_HOST": "https://app.compliancedb.com"
    }
