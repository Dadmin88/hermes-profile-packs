---
name: code-example-validation
description: Validate documentation code examples by executing them against the documented version, checking dependencies, setup, security, output, cleanup, platform assumptions, and consistency with current APIs.
---
# Code Example Validation

Use when documentation includes code or commands readers are expected to copy, adapt, or trust.

## Procedure
1. Identify the language, runtime, dependency versions, product or API version, environment, and prerequisites the example claims to support.
2. Start from a clean or representative workspace and follow setup exactly as a reader would.
3. Run the example without undocumented files, environment variables, credentials, global packages, or local services.
4. Verify output, side effects, error handling, cleanup, and whether the example demonstrates the behavior the surrounding prose claims.
5. Check imports, types, deprecated APIs, configuration, permissions, platform-specific syntax, and dependency pinning or installation instructions.
6. Replace real secrets, personal data, destructive commands, and unsafe defaults with explicit placeholders or safe examples.
7. Test important variants or failures only where the documentation promises they work; keep the primary example minimal.
8. Record the validated environment and update or remove examples that cannot be maintained reliably.

## Decision rules
- Copyable code should actually run.
- Hidden author setup is a documentation defect.
- Examples should teach the supported interface, not a deprecated shortcut.
- Safe placeholders must be obviously non-secret and explained where replacement is required.

## Quality gate
The example is validated when a reader can reproduce it from documented prerequisites on a supported environment, the observed result matches the text, current APIs and dependencies are used, security or cleanup surprises are absent, and hidden local assumptions have been eliminated.