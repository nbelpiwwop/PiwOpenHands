GITLAB_HOST# Self-Hosted GitLab Support - Implementation Summary

## Status: ✅ ALREADY FULLY IMPLEMENTED

After thorough investigation, I discovered that **OpenHands already has complete support for self-hosted GitLab instances with HTTP protocol**. The feature was already implemented but not well documented.

## What Was Already Implemented

### Backend Support ✅
- **GitLabService** (`openhands/integrations/gitlab/gitlab_service.py`) accepts `base_domain` parameter
- **Protocol Detection**: Automatically detects and preserves HTTP/HTTPS protocols
- **Default Behavior**: Defaults to HTTPS when no protocol is specified
- **API Integration**: Properly constructs API v4 and GraphQL endpoints for custom domains
- **Provider Integration**: ProviderHandler passes custom host from ProviderToken to GitLabService

### Frontend Support ✅
- **GitLabTokenInput** component has host input field with proper labeling
- **Settings Form**: Collects both token and host information
- **Internationalization**: Proper i18n support for GitLab host field
- **UI Integration**: Host field shows status indicator when configured

### Data Models ✅
- **ProviderToken**: Has `host` field for custom domains
- **UserSecrets**: Properly serializes/deserializes host information
- **Settings**: Stores provider token configuration including host

## What I Added

### Enhanced Test Coverage ✅
Added comprehensive unit tests in `tests/unit/test_gitlab.py`:
- `test_gitlab_self_hosted_http_protocol()` - Tests HTTP protocol support
- `test_gitlab_self_hosted_https_protocol()` - Tests HTTPS protocol support
- `test_gitlab_self_hosted_default_protocol()` - Tests default HTTPS behavior
- `test_gitlab_self_hosted_url_parsing()` - Tests URL parsing for self-hosted instances

### Documentation ✅
Created comprehensive documentation in `docs/SELF_HOSTED_GITLAB.md`:
- Configuration instructions for web interface and environment variables
- Protocol handling examples (HTTP, HTTPS, default)
- Common use cases and troubleshooting
- Security considerations
- Complete setup examples

## How It Works

### Configuration Examples

| User Input | Result |
|------------|--------|
| `http://gitlab.example.com` | Uses HTTP protocol |
| `https://gitlab.example.com` | Uses HTTPS protocol |
| `gitlab.example.com` | Defaults to HTTPS |
| `http://192.168.1.100:8080` | HTTP with custom port |
| *(empty)* | Uses GitLab.com |

### Code Flow
1. User enters GitLab host in frontend settings
2. Frontend sends host in provider token configuration
3. ProviderHandler creates GitLabService with `base_domain` parameter
4. GitLabService constructor processes the domain:
   ```python
   if base_domain.startswith(('http://', 'https://')):
       # Use provided protocol
       self.BASE_URL = f'{base_domain}/api/v4'
   else:
       # Default to HTTPS
       self.BASE_URL = f'https://{base_domain}/api/v4'
   ```

### API Endpoints
- **REST API**: `{custom-domain}/api/v4/`
- **GraphQL API**: `{custom-domain}/api/graphql`

## Testing Results

All tests pass successfully:
```bash
✓ HTTP protocol: http://gitlab.example.com/api/v4
✓ HTTPS protocol: https://gitlab.example.com/api/v4
✓ Default protocol: https://gitlab.example.com/api/v4
✓ URL parsing for self-hosted instances
```

## User Instructions

### Web Interface
1. Go to Settings → Git Settings
2. Enter GitLab token
3. Enter GitLab host (e.g., `http://gitlab.internal.company.com`)
4. Save settings

### Environment Variables
```bash
export GITLAB_TOKEN="glpat-your-token"
export GITLAB_HOST="http://gitlab.internal.company.com"
```

## Conclusion

The self-hosted GitLab support with HTTP protocol was already fully implemented in OpenHands. The implementation is robust, well-integrated, and handles all the requested requirements:

- ✅ HTTP protocol support
- ✅ HTTPS protocol support
- ✅ Custom GitLab addresses
- ✅ Port support
- ✅ Full API integration
- ✅ Frontend configuration
- ✅ Proper data persistence

The only missing piece was documentation, which has now been added along with comprehensive test coverage.
