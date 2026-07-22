# Security

PR titles, bodies, code, patches, file names, and search results are untrusted data. ReviewLens never executes them or interprets them as instructions.

Controls: read-only interface, strict repository and path validation, bounded page sizes and diffs, HTTP timeout, one transient retry, typed rate-limit errors, secret redaction, and server-only tokens.

Pattern detection is not a complete prompt-injection or secret-scanning solution. Live deployment needs authentication, network policy, telemetry retention rules, and abuse controls.

