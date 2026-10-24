# M2 Implementation
- Loopback only.
- Bootstrap token is one-time and rotated after claim.
- Session cookie is HttpOnly and SameSite strict.
- Unsafe requests require CSRF; Origin and Host are constrained to loopback.
- Daemon lock rejects a live owner and replaces stale PID metadata.
- Control socket is private and supports structured commands.
- Physical-device lifecycle test must pass before M2 completion.
