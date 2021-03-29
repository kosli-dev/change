from env_vars import ArtifactGitUrlEnvVar


def test_is_required__is_true_for_raw_docker():
    assert ArtifactGitUrlEnvVar({}).is_required('docker')


def test_is_required__is_false_for_genuine_ci():
    assert not ArtifactGitUrlEnvVar({}).is_required('bitbucket')

