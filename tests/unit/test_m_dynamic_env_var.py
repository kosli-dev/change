from errors import ChangeError
from env_vars import CIBuildNumberEnvVar
from pytest import raises


def test_value_raises_when_no_default_expansion():
    ev = CIBuildNumberEnvVar({})
    with raises(ChangeError) as exc:
        ev.value

    assert str(exc.value) == \
        "Error: " \
        "MERKELY_CI_BUILD_NUMBER env-var is not set " \
        "and cannot be default-expanded as the CI system " \
        "cannot be determined (there are no BITBUCKET_ or GITHUB_ env-vars)."


def test_value_raises_when_ambiguous_default_expansion():
    os_env = {
        "BITBUCKET_BUILD_NUMBER": "this is set",
        "GITHUB_RUN_ID": "this is also set",
    }
    ev = CIBuildNumberEnvVar(os_env)
    with raises(ChangeError) as exc:
        ev.value

    assert str(exc.value) == \
        "Error: " \
        "MERKELY_CI_BUILD_NUMBER env-var is not set " \
        "and cannot be default-expanded as the CI system " \
        "cannot be determined (there are BITBUCKET_ and GITHUB_ env-vars)."