from policy.capabilities import Capability as C,Decision as D
from policy.profiles import decision
def test_profile_matrix_core():
 assert decision('READ_ONLY',C.FS_READ)==D.ALLOW;assert decision('READ_ONLY',C.FS_WRITE)==D.DENY;assert decision('SAFE',C.FS_WRITE)==D.APPROVE;assert decision('NORMAL',C.FS_WRITE)==D.ALLOW;assert decision('NORMAL',C.GIT_INTERNALS)==D.DENY
