# Self-Hosted GitLab Support

OpenHands fully supports self-hosted GitLab instances with both HTTP and HTTPS protocols. This guide explains how to configure and use self-hosted GitLab with OpenHands.

## Features

- ✅ **HTTP Protocol Support**: Connect to GitLab instances using HTTP (e.g., `http://gitlab.internal.company.com`)
- ✅ **HTTPS Protocol Support**: Connect to GitLab instances using HTTPS (e.g., `https://gitlab.secure.company.com`)
- ✅ **Custom Domains**: Support for any custom domain or IP address
- ✅ **Port Support**: Support for custom ports (e.g., `http://gitlab.example.com:8080`)
- ✅ **API Integration**: Full GitLab API v4 and GraphQL support
- ✅ **Repository Management**: Browse, search, and manage repositories
- ✅ **Merge Requests**: Create and manage merge requests
- ✅ **Issue Tracking**: Access and manage GitLab issues

## Configuration

### 1. Using the Web Interface

1. Navigate to **Settings** → **Git Settings** in the OpenHands web interface
2. In the **GitLab** section:
   - **GitLab Token**: Enter your GitLab personal access token
   - **GitLab Host (optional)**: Enter your self-hosted GitLab URL

#### Examples:

| GitLab Host Field | Result |
|-------------------|--------|
| `http://gitlab.example.com` | Uses HTTP protocol |
| `https://gitlab.example.com` | Uses HTTPS protocol |
| `gitlab.example.com` | Defaults to HTTPS |
| `http://192.168.1.100:8080` | HTTP with custom port |
| *(empty)* | Uses GitLab.com |

### 2. Using Environment Variables

You can also configure self-hosted GitLab using environment variables:

```bash
# Set your GitLab token
export GITLAB_TOKEN="glpat-your-token-here"

# For HTTP protocol
export GITLAB_HOST="http://gitlab.internal.company.com"

# For HTTPS protocol  
export GITLAB_HOST="https://gitlab.secure.company.com"

# For custom port
export GITLAB_HOST="http://gitlab.example.com:8080"
```

### 3. Creating a GitLab Personal Access Token

1. Log in to your self-hosted GitLab instance
2. Go to **User Settings** → **Access Tokens**
3. Create a new token with the following scopes:
   - `api` - Full API access
   - `read_user` - Read user information
   - `read_repository` - Read repository information
   - `write_repository` - Write repository information (for merge requests)

## Protocol Handling

OpenHands automatically handles different protocol configurations:

### HTTP Protocol
```
Input: http://gitlab.example.com
API Base URL: http://gitlab.example.com/api/v4
GraphQL URL: http://gitlab.example.com/api/graphql
```

### HTTPS Protocol
```
Input: https://gitlab.example.com
API Base URL: https://gitlab.example.com/api/v4
GraphQL URL: https://gitlab.example.com/api/graphql
```

### Default Protocol (HTTPS)
```
Input: gitlab.example.com
API Base URL: https://gitlab.example.com/api/v4
GraphQL URL: https://gitlab.example.com/api/graphql
```

## Common Use Cases

### Corporate Self-Hosted GitLab

Many organizations run GitLab on internal networks:

```
GitLab Host: http://gitlab.internal.company.com
Token: glpat-xxxxxxxxxxxxxxxxxxxx
```

### GitLab with Custom SSL

For GitLab instances with custom SSL certificates:

```
GitLab Host: https://gitlab.secure.company.com
Token: glpat-xxxxxxxxxxxxxxxxxxxx
```

### Development Environment

For local development GitLab instances:

```
GitLab Host: http://localhost:8080
Token: glpat-xxxxxxxxxxxxxxxxxxxx
```

## Troubleshooting

### Connection Issues

1. **SSL Certificate Errors**: If using HTTPS with self-signed certificates, ensure your system trusts the certificate or use HTTP if appropriate for your environment.

2. **Network Access**: Ensure OpenHands can reach your GitLab instance. Check firewalls and network policies.

3. **Token Permissions**: Verify your personal access token has the required scopes (`api`, `read_user`, `read_repository`, `write_repository`).

### Testing Your Configuration

You can test your GitLab configuration by:

1. Going to **Settings** → **Git Settings**
2. Entering your token and host
3. Saving the configuration
4. Trying to browse repositories or create a new conversation with a GitLab repository

### API Endpoints

OpenHands uses these GitLab API endpoints:

- **REST API**: `{your-gitlab-host}/api/v4/`
- **GraphQL API**: `{your-gitlab-host}/api/graphql`

Ensure these endpoints are accessible from where OpenHands is running.

## Security Considerations

### HTTP vs HTTPS

- **HTTPS**: Recommended for production environments. Provides encryption for API calls and token transmission.
- **HTTP**: Suitable for internal networks or development environments where HTTPS is not available.

### Token Security

- Store tokens securely and rotate them regularly
- Use tokens with minimal required permissions
- Consider using GitLab's token expiration features

### Network Security

- Ensure proper firewall rules are in place
- Consider using VPN or private networks for sensitive GitLab instances
- Monitor API access logs for unusual activity

## Examples

### Complete Configuration Example

```bash
# Environment variables
export GITLAB_TOKEN="glpat-your-personal-access-token"
export GITLAB_HOST="http://gitlab.internal.company.com"

# Start OpenHands
openhands
```

### Repository URL Formats

OpenHands supports these GitLab repository URL formats:

- `http://gitlab.example.com/group/repo`
- `https://gitlab.example.com/group/subgroup/repo`
- `http://gitlab.internal.company.com:8080/namespace/project`

## Support

If you encounter issues with self-hosted GitLab integration:

1. Check the OpenHands logs for error messages
2. Verify your GitLab instance is accessible
3. Test your token permissions using GitLab's API directly
4. Ensure your GitLab version is supported (GitLab 13.0+ recommended)

For additional help, please refer to the main OpenHands documentation or open an issue on the OpenHands GitHub repository.