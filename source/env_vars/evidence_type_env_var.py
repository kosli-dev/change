from env_vars import RequiredEnvVar


class EvidenceTypeEnvVar(RequiredEnvVar):

    def __init__(self, env):
        notes = "The evidence type."
        super().__init__(env, "MERKELY_EVIDENCE_TYPE", notes)

    def ci_doc_example(self, ci_name, command_name):
        if ci_name == 'github':
            if command_name == 'log_evidence':
                return True, 'coverage'
            if command_name == 'log_test':
                return True, 'security'
        return False, ""
