---
name: playwright-cli
description: Verify web flows in an isolated browser, inspect console and network activity, mock API responses, and reproduce failures with the project's Playwright tests.
version: 0.1.23
author: Microsoft
license: Apache-2.0
---

# Browser automation with Playwright CLI

Use the project-pinned Playwright runner for repeatable regressions. Use an installed Playwright CLI or Hermes browser tools for exploratory browser checks. Run against a local development server or an explicitly approved test target with synthetic accounts and data.

## Run a browser check

1. Inspect the project's test scripts and start its authorized development server. Confirm the URL and the expected visible outcome before interacting.
2. Use a distinct named, temporary browser session for each task. Use the browser installed for the workspace. If the launcher needs a path, point a local Playwright CLI config's `browser.launchOptions.executablePath` at the approved installed Chromium binary and pass `--config` on `open`.
3. Take a snapshot, interact using the latest element refs or a role locator, and verify the resulting UI and request outcome. Cover the happy path and the failure the feature is meant to handle. Inspect console and network evidence when the UI and API disagree.
4. Close only the named session you opened. Keep traces, screenshots and browser state local. Use sanitized test data and redact artifacts before sharing.

```bash
playwright-cli -s=feature-check open http://localhost:3000
playwright-cli -s=feature-check snapshot
playwright-cli -s=feature-check click "getByRole('button', { name: 'Save' })"
playwright-cli -s=feature-check console
playwright-cli -s=feature-check requests
playwright-cli -s=feature-check close
```

Use the same `-s=feature-check` prefix throughout a named session. Pick the application's actual URL and locators. Keep the default in-memory browser profile and use a dedicated debug session when attaching to a test runner.

### Emulation

```bash
playwright-cli set-color-scheme dark
playwright-cli clear-color-scheme
playwright-cli set-reduced-motion reduce
playwright-cli clear-reduced-motion
playwright-cli set-forced-colors active
playwright-cli clear-forced-colors
playwright-cli set-contrast more
playwright-cli clear-contrast
playwright-cli set-media print
playwright-cli clear-media
```

## Snapshots

After each command, playwright-cli provides a snapshot of the current browser state.

```bash
> playwright-cli goto https://example.com
### Page
- Page URL: http://localhost:3000/
- Page Title: Test application
### Snapshot
[Snapshot](.playwright-cli/page-2026-02-14T19-22-42-679Z.yml)
```

You can also take a snapshot on demand using `playwright-cli snapshot` command. All the options below can be combined as needed.

```bash
# default - save to a file with timestamp-based name
playwright-cli snapshot

# save to file, use when snapshot is a part of the workflow result
playwright-cli snapshot --filename=after-click.yaml

# snapshot an element instead of the whole page
playwright-cli snapshot "#main"

# limit snapshot depth for efficiency, take a partial snapshot afterwards
playwright-cli snapshot --depth=4
playwright-cli snapshot e34

# include each element's bounding box as [box=x,y,width,height]
playwright-cli snapshot --boxes

# search a large snapshot instead of capturing it all — returns matching nodes
# with 3 lines of context around each match (like grep -C)
playwright-cli find "Add to cart"
playwright-cli find --regex "\\$[0-9]+\\.[0-9]{2}"
```

## Targeting elements

By default, use refs from the snapshot to interact with page elements.

```bash
# get snapshot with refs
playwright-cli snapshot

# interact using a ref
playwright-cli click e15
```

You can also use css selectors or Playwright locators.

```bash
# css selector
playwright-cli click "#main > button.submit"

# role locator
playwright-cli click "getByRole('button', { name: 'Submit' })"

# test id
playwright-cli click "getByTestId('submit-button')"
```

## Repeatable tests and failure evidence

- Use [project tests](references/playwright-tests.md) to rerun a failure and debug the paused test session. Prefer stable role, label or test ID locators and assertions about user-visible outcomes.
- Use [request mocking](references/request-mocking.md) to reproduce empty, error and slow responses. Verify the real integration separately. Scope each mock to the approved test target and remove it afterward.
- Use [element attributes](references/element-attributes.md) when snapshots omit a property needed to understand a selector.
- Use `console`, `requests`, `request <id>`, `tracing-start`, and `tracing-stop` on synthetic flows when useful. Traces can retain page contents, request bodies and headers. Capture only the necessary steps and keep the output local.
