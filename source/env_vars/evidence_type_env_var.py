from env_vars import RequiredEnvVar


class EvidenceTypeEnvVar(RequiredEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_EVIDENCE_TYPE")

    def doc_example(self, ci_name, command_name):
        if ci_name == 'github':
            if command_name == 'log_evidence':
                return True, 'coverage'
            if command_name == 'log_test':
                return True, 'security'
        if ci_name == 'bitbucket':
            if command_name == 'log_evidence':
                return True, 'coverage'
            if command_name == 'log_test':
                return True, 'security'
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return "The evidence type."
