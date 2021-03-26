from errors import ChangeError
from env_vars import CIBuildNumberEnvVar
from pytest import raises


def test_doc_note_is_passed_ci_name_and_command_name_for_customisability():
    expected = "The ci build number."
    assert CIBuildNumberEnvVar({}).doc_note('docker', 'log_artifact') == expected


def test_value_expands_when_non_abiguous_expansion():
    gh = {"GITHUB_RUN_ID": "23"}
    assert CIBuildNumberEnvVar(gh).value == "23"
    bb = {"BITBUCKET_BUILD_NUMBER": "134"}
    assert CIBuildNumberEnvVar(bb).value == "134"


def test_value_raises_when_no_default_expansion():
    ev = CIBuildNumberEnvVar({})
    with raises(ChangeError) as exc:
        ev.value

    assert str(exc.value) == \
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
       "MERKELY_CI_BUILD_NUMBER env-var is not set " \
       "and cannot be default-expanded as the CI system " \
       "cannot be determined (there are BITBUCKET_ and GITHUB_ env-vars)."



