from agent.completion import verify_claims
def test_claim_verification():
 assert verify_claims([{'kind':'tests_pass'}],{'tests_after_last_edit':True})[0]['verified'];assert not verify_claims([{'kind':'tests_pass'}],{'tests_after_last_edit':False})[0]['verified']
