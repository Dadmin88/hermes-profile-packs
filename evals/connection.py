"""Provider setup through Hermes's normal runtime API; never persist login secrets."""
from contextlib import redirect_stderr, redirect_stdout
import io
import os
from pathlib import Path
import sys

CODEX_URL = 'https://chatgpt.com/backend-api/codex'


def validate_login_settings(settings):
    if settings.get('provider') != 'openai-codex' or settings.get('base_url', '').rstrip('/') != CODEX_URL:
        raise ValueError('Hermes login mode is restricted to the official ChatGPT Codex endpoint')


def connect(settings):
    if settings.get('connection', 'api-key') == 'api-key':
        return {'api_key': os.environ.get('HERMES_EVAL_API_KEY'), 'api_mode': None}
    validate_login_settings(settings)
    # Only the trusted controller supplies this directory; browser requests cannot choose it.
    home = os.environ.get('HERMES_EVAL_LOGIN_HOME')
    if not home:
        raise RuntimeError('Hermes login home was not supplied by the controller')
    sys.path.insert(0, str(Path(settings['hermes_source']).resolve()))
    old = {key: os.environ.get(key) for key in ('HOME', 'HERMES_HOME', 'HERMES_PROFILE')}
    try:
        os.environ.update(HOME=home, HERMES_HOME=str(Path(home) / '.hermes'))
        os.environ.pop('HERMES_PROFILE', None)
        # Native credential use, not auth-file copying or parsing. Native code may refresh login.
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            from hermes_cli.runtime_provider import resolve_runtime_provider
            runtime = resolve_runtime_provider(requested='openai-codex', target_model=settings['model'])
        if (runtime.get('provider') != 'openai-codex' or runtime.get('api_mode') != 'codex_responses'
                or runtime.get('base_url', '').rstrip('/') != CODEX_URL or not runtime.get('api_key')):
            raise RuntimeError('Native connection does not match the supported Codex login route')
        return {'api_key': runtime['api_key'], 'api_mode': 'codex_responses'}
    except Exception as exc:
        # Provider exceptions can contain private connection details; report only the class.
        raise RuntimeError(f'Hermes login connection unavailable ({type(exc).__name__}); check Hermes sign-in') from None
    finally:
        for key, value in old.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
