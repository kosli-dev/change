def control_deployment_approved(approvals):
    for approval in approvals:
        if approval["state"] == "APPROVED":
            return True
    return False
