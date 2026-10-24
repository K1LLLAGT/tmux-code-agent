from enum import StrEnum
class Capability(StrEnum):
 FS_READ='fs.read';FS_READ_SECRETS='fs.read.secrets';FS_WRITE='fs.write.workspace';FS_WRITE_HOME='fs.write.home';GIT_INTERNALS='git.internals';SHELL_EXEC='shell.execute';SHELL_INSTALL='shell.install';GIT_READ='git.read';GIT_WRITE='git.write';NETWORK_LOCAL='network.local';NETWORK_EXTERNAL='network.external';PROCESS_SIGNAL='process.signal'
class Decision(StrEnum):ALLOW='allow';APPROVE='approve';DENY='deny'
