from policy.hard_deny import command_denied
def test_git_hard_denies():assert command_denied(['git','reset','--hard']) and command_denied(['git','push','--force']) and not command_denied(['git','status'])
