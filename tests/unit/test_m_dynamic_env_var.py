from errors import ChangeError
from env_vars import CIBuildNumberEnvVar
from pytest import raises


def test_name_as_set_in_ctor():
    ev = CIBuildNumberEnvVar({})
    with raises(ChangeError) as exc:
        ev.value

    assert str(exc.value) == \
        "Error: " \
        "MERKELY_CI_BUILD_NUMBER env-var is not set " \
        "and cannot be default-expanded as the CI system " \
        "cannot be determined (there are no BITBUCKET_ or GITHUB_ env-var)."


