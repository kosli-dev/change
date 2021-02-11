
UNAPPROVED_REQUEST = {
	"approvals": [],
	"base_artifact": "084c799cd551dd1d8d5c5f9a5d593b2e931f5e36122ee5c793c1d08a19839cc1",
	"description": "Test approval for the approval project",
	"release_number": "1",
	"src_commit_list": [
		"e412ad6f7ea530ee9b83df964a0dde2b477be728",
		"e412ad6f7ea530ee9b83df964a0dde2b477be729"
	],
	"state": "UNAPPROVED",
	"target_artifact": "084c799cd551dd1d8d5c5f9a5d593b2e931f5e36122ee5c793c1d08a19839cc1"
}

APPROVED_REQUEST = {
	"approvals": [
		{
			"comment": "Looks pretty good, I ok this in my CI tool",
			"state": "APPROVED",
			"user": "external://meekrosoft-ci-user"
		}
	],
	"base_artifact": "084c799cd551dd1d8d5c5f9a5d593b2e931f5e36122ee5c793c1d08a19839cc1",
	"description": "Test approval for the approval project",
	"release_number": "2",
	"src_commit_list": [
		"e412ad6f7ea530ee9b83df964a0dde2b477be728",
		"e412ad6f7ea530ee9b83df964a0dde2b477be729"
	],
	"state": "APPROVED",
	"target_artifact": "084c799cd551dd1d8d5c5f9a5d593b2e931f5e36122ee5c793c1d08a19839cc1"
}


def control_deployment_approved(approvals):
	for approval in approvals:
		if approval["state"] == "APPROVED":
			return True
	return False

def test_returns_false_when_approvals_empty():
	is_approved = control_deployment_approved(approvals=[])
	assert is_approved == False

def test_returns_true_when_approved_approval():
	is_approved = control_deployment_approved(approvals=[APPROVED_REQUEST])
	assert is_approved == True

def test_returns_false_when_approvals_pending():
	is_approved = control_deployment_approved(approvals=[UNAPPROVED_REQUEST])
	assert is_approved == False

def test_returns_true_when_mixed_approval_states():
	is_approved = control_deployment_approved(approvals=[UNAPPROVED_REQUEST, APPROVED_REQUEST])
	assert is_approved == True

