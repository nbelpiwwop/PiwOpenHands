import os
from pydantic import SecretStr

from openhands.core.logger import openhands_logger as logger
from openhands.integrations.bitbucket.bitbucket_service import BitBucketService
from openhands.integrations.github.github_service import GitHubService
from openhands.integrations.gitlab.gitlab_service import GitLabService
from openhands.integrations.provider import ProviderType
from openhands.integrations.service_types import RequestMethod


async def validate_provider_token(
    token: SecretStr, base_domain: str | None = None
) -> ProviderType | None:
    """
    Determine whether a token is for GitHub, GitLab, or Bitbucket by attempting to get user info
    from the services.

    Args:
        token: The token to check
        base_domain: Optional base domain for the service

    Returns:
        'github' if it's a GitHub token
        'gitlab' if it's a GitLab token
        'bitbucket' if it's a Bitbucket token
        None if the token is invalid for all services
    """
    # Skip validation for empty tokens
    if token is None:
        return None  # type: ignore[unreachable]

    # If no base_domain provided, check environment variables for each provider
    github_domain = base_domain or os.getenv('GITHUB_HOST')
    gitlab_domain = base_domain or os.getenv('GITLAB_HOST')
    bitbucket_domain = base_domain or os.getenv('BITBUCKET_HOST')

    # Try GitHub first
    github_error = None
    try:
        github_service = GitHubService(token=token, base_domain=github_domain)
        await github_service.verify_access()
        return ProviderType.GITHUB
    except Exception as e:
        github_error = e

    # Try GitLab next
    gitlab_error = None
    try:
        gitlab_service = GitLabService(token=token, base_domain=gitlab_domain)
        await gitlab_service.get_user()
        return ProviderType.GITLAB
    except Exception as e:
        gitlab_error = e
        # Log curl equivalent command for debugging GitLab token validation failures
        try:
            # Generate the curl command for the failed GitLab API call
            gitlab_headers = await gitlab_service._get_gitlab_headers()
            user_url = f'{gitlab_service.BASE_URL}/user'
            curl_command = gitlab_service._generate_curl_command(
                url=user_url,
                headers=gitlab_headers,
                method=RequestMethod.GET,
            )
            logger.info(f"GitLab token validation failed - curl equivalent: {curl_command}")
        except Exception as curl_error:
            logger.debug(f"Failed to generate curl command for GitLab validation: {curl_error}")

    # Try Bitbucket last
    bitbucket_error = None
    try:
        bitbucket_service = BitBucketService(token=token, base_domain=bitbucket_domain)
        await bitbucket_service.get_user()
        return ProviderType.BITBUCKET
    except Exception as e:
        bitbucket_error = e

    logger.debug(
        f'Failed to validate token: {github_error} \n {gitlab_error} \n {bitbucket_error}'
    )

    return None



