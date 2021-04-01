from commands import Command, External, in_dry_run

API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"


def test_setting_in_dry_run_locally_using_MERKELY_DRY_RUN_env_var_is_TRUE():
    assert not in_dry_run(make_command(dry_run="FALSE"))
    assert in_dry_run(make_command(dry_run="TRUE"))


def test_setting_in_dry_run_globally_using_MERKELY_API_TOKEN_env_var_is_DRY_RUN():
    assert not in_dry_run(make_command(api_token=API_TOKEN))
    assert in_dry_run(make_command(api_token="DRY_RUN"))


def make_command(*, api_token=None, dry_run=None):
    if api_token is None:
        api_token = API_TOKEN
    if dry_run is None:
        dry_run = "FALSE"
    env = {
        'MERKELY_COMMAND': 'log_artifact',
        'MERKELY_API_TOKEN': api_token,
        'MERKELY_DRY_RUN': dry_run
    }
    return Command(External(env=env))
