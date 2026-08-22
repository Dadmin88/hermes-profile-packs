# Security Policy

Profile packs are source distributions and must never contain runtime credentials or private user state.

## Never commit

- API keys, access tokens, refresh tokens, passwords, cookies, private keys, or OAuth credentials
- `.env` files or authentication databases
- personal home-directory paths, private mount paths, or machine-specific service endpoints
- user conversations, memory databases, logs, cache snapshots, or session dumps

## Reporting

If you discover a credential, private user artifact, unsafe distribution behavior, or a profile instruction that could materially enable harm, report it privately to the repository maintainer rather than opening a public issue containing the sensitive data.

If a secret is ever committed, treat it as compromised even after history is rewritten: revoke or rotate it first, then remove it from history.
