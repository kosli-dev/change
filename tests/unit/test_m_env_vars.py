from commands import LogEvidenceCommand, Context


def test_env_vars():
    domain = "app.compliancedb.com"
    build_url = "https://gitlab/build/1956"
    protocol = "docker://"
    image_name = "acme/widget:4.67"
    api_token = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"
    env = {
        "MERKELY_API_TOKEN": api_token,
        "MERKELY_CI_BUILD_URL": build_url,
        "MERKELY_COMMAND": "log_evidence",
        "MERKELY_DESCRIPTION": "branch coverage",
        "MERKELY_EVIDENCE_TYPE": "unit_test",
        "MERKELY_FINGERPRINT": f"{protocol}/{image_name}",
        "MERKELY_HOST": f"https://{domain}",
        "MERKELY_IS_COMPLIANT": "TRUE",
    }
    context = Context(env)
    command = LogEvidenceCommand(context)
    env_vars = command.env_vars

    assert env_vars.api_token.value == api_token
    assert env_vars.ci_build_url.value == build_url
    assert env_vars.description.value == "branch coverage"
    assert env_vars.evidence_type.value == "unit_test"
    assert env_vars.fingerprint.value == f"{protocol}/{image_name}"
    assert env_vars.host.value == f"https://{domain}"
    assert env_vars.is_compliant.value == 'TRUE'

