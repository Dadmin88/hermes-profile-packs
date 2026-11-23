import contextlib
import io
import os
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from evals.connection import CODEX_URL, connect, validate_login_settings


class ConnectionTests(unittest.TestCase):
    def setUp(self):
        self.settings = {'connection':'hermes-login', 'hermes_source':'/tmp/runtime', 'model':'test-model',
                         'provider':'openai-codex', 'base_url':CODEX_URL}
        original = list(sys.path)
        self.addCleanup(lambda: sys.path.__setitem__(slice(None), original))

    def test_login_cannot_be_redirected_to_another_host(self):
        for url in ('https://evil.invalid', CODEX_URL + '.evil.invalid', CODEX_URL + '?key=x'):
            with self.assertRaises(ValueError): validate_login_settings(dict(self.settings, base_url=url))

    def test_native_login_uses_resolver_and_restores_isolated_home(self):
        resolver = Mock(return_value={'provider':'openai-codex','base_url':CODEX_URL,'api_mode':'codex_responses','api_key':'test-only-secret'})
        output = io.StringIO()
        with patch.dict(sys.modules, {'hermes_cli.runtime_provider':SimpleNamespace(resolve_runtime_provider=resolver)}), \
             patch.dict(os.environ, {'HOME':'/tmp/isolated', 'HERMES_HOME':'/tmp/isolated/profile', 'HERMES_EVAL_LOGIN_HOME':'/tmp/login-test'}), \
             contextlib.redirect_stdout(output):
            connection = connect(self.settings)
            self.assertEqual(os.environ['HOME'], '/tmp/isolated')
            self.assertEqual(os.environ['HERMES_HOME'], '/tmp/isolated/profile')
        resolver.assert_called_once_with(requested='openai-codex', target_model='test-model')
        self.assertEqual(connection['api_key'], 'test-only-secret')
        self.assertNotIn('test-only-secret', output.getvalue())

    def test_provider_errors_do_not_expose_secrets(self):
        resolver = Mock(side_effect=ValueError('test-only-secret'))
        with patch.dict(sys.modules, {'hermes_cli.runtime_provider':SimpleNamespace(resolve_runtime_provider=resolver)}), \
             patch.dict(os.environ, {'HERMES_EVAL_LOGIN_HOME':'/tmp/login-test'}):
            with self.assertRaises(RuntimeError) as caught: connect(self.settings)
        self.assertNotIn('test-only-secret', str(caught.exception))

    def test_unexpected_native_route_is_rejected(self):
        for field, value in [('provider','custom'),('base_url','https://evil.invalid'),('api_mode','codex_app_server')]:
            runtime={'provider':'openai-codex','base_url':CODEX_URL,'api_mode':'codex_responses','api_key':'test-only-secret',field:value}
            resolver=Mock(return_value=runtime)
            with patch.dict(sys.modules, {'hermes_cli.runtime_provider':SimpleNamespace(resolve_runtime_provider=resolver)}), \
                 patch.dict(os.environ, {'HERMES_EVAL_LOGIN_HOME':'/tmp/login-test'}):
                with self.assertRaises(RuntimeError): connect(self.settings)

    def test_explicit_key_mode_does_not_use_login(self):
        with patch.dict(os.environ, {'HERMES_EVAL_API_KEY':'test-only-key'}):
            self.assertEqual(connect({'connection':'api-key'})['api_key'], 'test-only-key')
