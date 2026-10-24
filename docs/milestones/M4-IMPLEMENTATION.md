# M4 Implementation
SSH is transport, not a privilege boundary. Channel B uses an exec key forced into `tca-runner`; PTY uses a separate restricted key. Child stdout/stderr are logged separately. Commands execute in their own process group. The request carries exact argv/cwd/env/limits rather than a shell command string. LocalTransport uses the same runner protocol as a degraded fallback.
