from gitsafe.worktree import should_offer
def test_dirty_offers_worktree():assert should_offer(True) and not should_offer(False)
