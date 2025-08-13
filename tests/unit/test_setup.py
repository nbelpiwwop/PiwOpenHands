"""Unit tests for the setup script functionality."""

import os
from unittest.mock import MagicMock, patch

from pydantic import SecretStr

from openhands.events.action import CmdRunAction, FileReadAction
from openhands.events.event import EventSource
from openhands.events.observation import ErrorObservation, FileReadObservation
from openhands.integrations.service_types import ProviderType
from openhands.runtime.base import Runtime


def test_maybe_run_setup_script_executes_action():
    """Test that maybe_run_setup_script executes the action after adding it to the event stream."""
    # Create mock runtime
    runtime = MagicMock(spec=Runtime)
    runtime.read.return_value = FileReadObservation(
        content="#!/bin/bash\necho 'test'", path='.openhands/setup.sh'
    )

    # Mock the event stream
    runtime.event_stream = MagicMock()

    # Add required attributes
    runtime.status_callback = None

    # Call the actual implementation
    with patch.object(
        Runtime, 'maybe_run_setup_script', Runtime.maybe_run_setup_script
    ):
        Runtime.maybe_run_setup_script(runtime)

    # Verify that read was called with the correct action
    runtime.read.assert_called_once_with(FileReadAction(path='.openhands/setup.sh'))

    # Verify that add_event was called with the correct action and source
    runtime.event_stream.add_event.assert_called_once()
    args, kwargs = runtime.event_stream.add_event.call_args
    action, source = args
    assert isinstance(action, CmdRunAction)
    assert source == EventSource.ENVIRONMENT

    # Verify that run_action was called with the correct action
    runtime.run_action.assert_called_once()
    args, kwargs = runtime.run_action.call_args
    action = args[0]
    assert isinstance(action, CmdRunAction)
    assert (
        action.command == 'chmod +x .openhands/setup.sh && source .openhands/setup.sh'
    )


def test_maybe_run_setup_script_skips_when_file_not_found():
    """Test that maybe_run_setup_script skips execution when the setup script is not found."""
    # Create mock runtime
    runtime = MagicMock(spec=Runtime)
    runtime.read.return_value = ErrorObservation(content='File not found', error_id='')

    # Mock the event stream
    runtime.event_stream = MagicMock()

    # Call the actual implementation
    with patch.object(
        Runtime, 'maybe_run_setup_script', Runtime.maybe_run_setup_script
    ):
        Runtime.maybe_run_setup_script(runtime)

    # Verify that read was called with the correct action
    runtime.read.assert_called_once_with(FileReadAction(path='.openhands/setup.sh'))

    # Verify that add_event was not called
    runtime.event_stream.add_event.assert_not_called()

    # Verify that run_action was not called
    runtime.run_action.assert_not_called()


def test_get_provider_tokens_gitlab_with_host():
    """Test that get_provider_tokens correctly reads GITLAB_TOKEN and GITLAB_HOST."""
    from openhands.core.setup import get_provider_tokens

    with patch.dict(
        os.environ,
        {
            'GITLAB_TOKEN': 'glpat-test-token',
            'GITLAB_HOST': 'http://gitlab.internal.company.com',
        },
        clear=True,
    ):
        provider_tokens = get_provider_tokens()

        assert provider_tokens is not None
        assert ProviderType.GITLAB in provider_tokens

        gitlab_token = provider_tokens[ProviderType.GITLAB]
        assert gitlab_token.token == SecretStr('glpat-test-token')
        assert gitlab_token.host == 'http://gitlab.internal.company.com'


def test_get_provider_tokens_gitlab_token_only():
    """Test that get_provider_tokens works with only GITLAB_TOKEN (no host)."""
    from openhands.core.setup import get_provider_tokens

    with patch.dict(
        os.environ,
        {
            'GITLAB_TOKEN': 'glpat-test-token-only',
        },
        clear=True,
    ):
        provider_tokens = get_provider_tokens()

        assert provider_tokens is not None
        assert ProviderType.GITLAB in provider_tokens

        gitlab_token = provider_tokens[ProviderType.GITLAB]
        assert gitlab_token.token == SecretStr('glpat-test-token-only')
        assert gitlab_token.host is None


def test_get_provider_tokens_github_with_host():
    """Test that get_provider_tokens correctly reads GITHUB_TOKEN and GITHUB_HOST."""
    from openhands.core.setup import get_provider_tokens

    with patch.dict(
        os.environ,
        {
            'GITHUB_TOKEN': 'ghp_test_token',
            'GITHUB_HOST': 'https://github.enterprise.com',
        },
        clear=True,
    ):
        provider_tokens = get_provider_tokens()

        assert provider_tokens is not None
        assert ProviderType.GITHUB in provider_tokens

        github_token = provider_tokens[ProviderType.GITHUB]
        assert github_token.token == SecretStr('ghp_test_token')
        assert github_token.host == 'https://github.enterprise.com'


def test_get_provider_tokens_bitbucket_with_host():
    """Test that get_provider_tokens correctly reads BITBUCKET_TOKEN and BITBUCKET_HOST."""
    from openhands.core.setup import get_provider_tokens

    with patch.dict(
        os.environ,
        {
            'BITBUCKET_TOKEN': 'bb_test_token',
            'BITBUCKET_HOST': 'https://bitbucket.internal.com',
        },
        clear=True,
    ):
        provider_tokens = get_provider_tokens()

        assert provider_tokens is not None
        assert ProviderType.BITBUCKET in provider_tokens

        bitbucket_token = provider_tokens[ProviderType.BITBUCKET]
        assert bitbucket_token.token == SecretStr('bb_test_token')
        assert bitbucket_token.host == 'https://bitbucket.internal.com'


def test_get_provider_tokens_multiple_providers():
    """Test that get_provider_tokens handles multiple providers with hosts."""
    from openhands.core.setup import get_provider_tokens

    with patch.dict(
        os.environ,
        {
            'GITHUB_TOKEN': 'ghp_test_token',
            'GITHUB_HOST': 'https://github.enterprise.com',
            'GITLAB_TOKEN': 'glpat-test-token',
            'GITLAB_HOST': 'http://gitlab.internal.company.com',
            'BITBUCKET_TOKEN': 'bb_test_token',
            'BITBUCKET_HOST': 'https://bitbucket.internal.com',
        },
        clear=True,
    ):
        provider_tokens = get_provider_tokens()

        assert provider_tokens is not None
        assert len(provider_tokens) == 3

        # Check GitHub
        github_token = provider_tokens[ProviderType.GITHUB]
        assert github_token.token == SecretStr('ghp_test_token')
        assert github_token.host == 'https://github.enterprise.com'

        # Check GitLab
        gitlab_token = provider_tokens[ProviderType.GITLAB]
        assert gitlab_token.token == SecretStr('glpat-test-token')
        assert gitlab_token.host == 'http://gitlab.internal.company.com'

        # Check Bitbucket
        bitbucket_token = provider_tokens[ProviderType.BITBUCKET]
        assert bitbucket_token.token == SecretStr('bb_test_token')
        assert bitbucket_token.host == 'https://bitbucket.internal.com'


def test_get_provider_tokens_no_env_vars():
    """Test that get_provider_tokens returns None when no environment variables are set."""
    from openhands.core.setup import get_provider_tokens

    with patch.dict(os.environ, {}, clear=True):
        provider_tokens = get_provider_tokens()
        assert provider_tokens is None
