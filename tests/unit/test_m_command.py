from commands import Command


def test_Command_names():
    assert "log_test" in Command.names()
    names = sorted(Command.names())
    assert "control_deployment"   == names[0]
    assert "control_pull_request" == names[1]
    assert "declare_pipeline"     == names[2]
