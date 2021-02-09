
def fingerprint_env_var_cls_for(protocol):
    # inline to break cyclic dependency
    from env_vars import DockerFingerprintEnvVar
    from env_vars import FileFingerprintEnvVar
    from env_vars import Sha256FingerprintEnvVar
    if protocol == 'docker://':
        return DockerFingerprintEnvVar
    elif protocol == 'file://':
        return FileFingerprintEnvVar
    elif protocol == 'sha256://':
        return Sha256FingerprintEnvVar
    else:
        return None
