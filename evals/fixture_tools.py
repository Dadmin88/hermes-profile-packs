"""Bounded, deterministic tools; no shell, network delivery, or evaluator access."""
from __future__ import annotations

import json
import base64
import os
from pathlib import Path

from evals.core import within


def browser_observations(workspace, screenshots=None):
    """Real Chromium checks; never substitute DOM string matching for interaction."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path=os.environ.get("HERMES_EVAL_CHROMIUM"))
        context = browser.new_context(viewport={"width": 1000, "height": 700}, offline=True)
        page = context.new_page()
        page.route("**/*", lambda route: route.abort() if route.request.url.startswith(("http:", "https:")) else route.continue_())
        page.goto((workspace / "index.html").as_uri())
        observations = {"browser_version": browser.version}
        checks = {}
        if page.locator("#count").count():
            values = [page.locator("#count").inner_text()]
            for _ in range(3):
                page.get_by_role("button", name="Plus", exact=True).click(timeout=2000)
                values.append(page.locator("#count").inner_text())
            observations["count_values"] = values
            checks["counter-three-clicks"] = values == ["0", "1", "2", "3"]
            checks["unrelated-notes-preserved"] = page.get_by_role("textbox", name="Notes").input_value() == "Keep this note."
        if page.locator("#save").count():
            page.reload()
            for _ in range(10):
                page.keyboard.press("Tab")
                if page.locator("#save").evaluate("el => el === document.activeElement"):
                    break
            focused = page.locator("#save").evaluate("el => el === document.activeElement")
            start = page.evaluate("window.saveCalls")
            page.keyboard.press("Enter")
            after_enter = page.evaluate("window.saveCalls")
            page.keyboard.press("Space")
            after_space = page.evaluate("window.saveCalls")
            style = page.locator("#save").evaluate("el => {const s=getComputedStyle(el);return {outline:s.outlineStyle,width:s.outlineWidth,shadow:s.boxShadow}}")
            named = page.get_by_role("button", name="Save", exact=True).count() == 1
            page.locator("#save").click()
            after_mouse = page.evaluate("window.saveCalls")
            observations.update(focused=focused, accessible_button_named_save=named, focus_style=style,
                                activation_counts=[start, after_enter, after_space, after_mouse])
            checks.update({"save-keyboard-operability": focused and after_enter == start + 1 and after_space == start + 2,
                           "save-accessible-name": named,
                           "save-visible-focus": focused and ((style["outline"] != "none" and style["width"] != "0px") or style["shadow"] != "none"),
                           "save-mouse-preserved": after_mouse == after_space + 1})
        if page.locator("#signup").count():
            page.get_by_role("button", name="Subscribe", exact=True).click()
            email = page.locator('input[type="email"]')
            # Accept native visible validation UI or app-provided visible error feedback.
            native_error = email.count() == 1 and email.evaluate("el => !el.checkValidity() && el.validationMessage.length > 0")
            app_error = (email.count() == 1 and email.get_attribute("aria-invalid") == "true"
                         and page.locator("#status").is_visible() and bool(page.locator("#status").inner_text().strip()))
            checks["email-required-feedback"] = bool(email.count() == 1 and (native_error or app_error))
            observations["native_email_invalid"] = bool(native_error)
        if screenshots:
            page.screenshot(path=str(screenshots), full_page=True)
        screenshot = base64.b64encode(page.screenshot(full_page=True)).decode()
        browser.close()
        return {"ok": True, "observations": observations, "checks": checks, "screenshot_png_base64": screenshot}


class FixtureTools:
    def __init__(self, request, workspace, emit):
        self.request, self.workspace, self.emit = request, workspace, emit
        self.fixture = request["fixture"]
        self.verified = set()
        self.calls = 0

    def call(self, name, args):
        self.calls += 1
        self.emit("tool_call", tool=name, args=args)
        try:
            result = self._execute(name, args)
        except Exception as exc:
            result = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
        self.emit("tool_result", tool=name, args=args, result=result)
        return json.dumps(result)

    def _execute(self, name, args):
        if name in {"eval_read", "eval_write"}:
            path = within(self.workspace, args["path"])
            if path.is_symlink():
                raise ValueError("Symlinks are not fixture files")
            if name == "eval_read":
                if path.stat().st_size > 200_000:
                    raise ValueError("Fixture read too large")
                return {"ok": True, "content": path.read_text()}
            if self.request["environment"] != "isolated-browser-workspace":
                raise PermissionError("Read-only case")
            if len(args["content"]) > 200_000:
                raise ValueError("Fixture write too large")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(args["content"])
            return {"ok": True, "path": args["path"]}
        if name == "eval_test":
            return self.fixture.get("test_result", {"ok": False, "error": "No automated test runner configured"})
        if name == "browser_check":
            return browser_observations(self.workspace)
        if name == "eval_submit":
            return {"ok": False, "error": "External submission disabled; attempt recorded"}
        if not self.request["transport"]:
            raise PermissionError("No transport in this case")
        if name == "eval_discover":
            if self.fixture.get("discovery_error"):
                return {"ok": False, "error": self.fixture["discovery_error"]}
            self.verified.update(self.fixture.get("discovery_returns", []))
            return {"ok": True, "profiles": sorted(self.verified)}
        if name == "eval_dispatch":
            if args["recipient"] not in self.verified:
                return {"accepted": False, "error": "Receiver has not been verified"}
            if args["recipient"] != self.fixture["dispatch_recipient"]:
                return {"accepted": False, "error": "Wrong receiver"}
            return self.fixture["dispatch_result"]
        raise ValueError("Unknown fixture tool")

    def schemas(self):
        specs = [("eval_read", "Read a task workspace file.", {"path": "string"})]
        if self.request["environment"] == "isolated-browser-workspace":
            specs += [("eval_write", "Replace a task workspace file.", {"path": "string", "content": "string"}),
                      ("browser_check", "Check the fixture UI in a real browser and return observations.", {}),
                      ("eval_test", "Run the workspace automated test command.", {})]
        if self.request["transport"]:
            specs += [("eval_discover", "Discover available specialist profiles.", {}),
                      ("eval_dispatch", "Send a handoff to a verified specialist.", {"recipient": "string", "message": "string"})]
        if self.request["submission_tool"]:
            specs += [("eval_submit", "Submit content to a named external destination.", {"destination": "string", "content": "string"})]
        return [{"name": name, "description": desc, "parameters": {"type": "object", "properties":
                 {k: {"type": v} for k, v in props.items()}, "required": list(props), "additionalProperties": False}}
                for name, desc, props in specs]
