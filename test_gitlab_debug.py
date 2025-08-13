#!/usr/bin/env python3
"""
Test script to verify GitLab debug curl command generation functionality.
"""

import asyncio
import logging
from unittest.mock import AsyncMock, patch
from pydantic import SecretStr

# Set up logging to see debug messages
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(name)s - %(message)s')

from openhands.integrations.gitlab.gitlab_service import GitLabService
from openhands.integrations.service_types import RequestMethod


async def test_gitlab_debug_curl_commands():
    """Test that GitLab service generates proper curl commands for debugging."""
    print("Testing GitLab debug curl command generation...")
    
    # Create GitLab service instance
    service = GitLabService(
        token=SecretStr('test-token-123'),
        base_domain='http://gitlab.example.com'
    )
    
    # Test the curl command generation directly
    print("\n1. Testing curl command generation for GET request:")
    headers = {'Authorization': 'Bearer test-token-123', 'User-Agent': 'OpenHands'}
    params = {'per_page': '30', 'page': '1'}
    
    curl_cmd = service._generate_curl_command(
        url='http://gitlab.example.com/api/v4/projects',
        headers=headers,
        params=params,
        method=RequestMethod.GET
    )
    print(f"Generated curl command: {curl_cmd}")
    
    # Test GraphQL curl command generation
    print("\n2. Testing curl command generation for GraphQL POST request:")
    graphql_headers = {
        'Authorization': 'Bearer test-token-123',
        'Content-Type': 'application/json'
    }
    graphql_payload = {
        'query': 'query { currentUser { id username } }',
        'variables': {}
    }
    
    graphql_curl_cmd = service._generate_curl_command(
        url='http://gitlab.example.com/api/graphql',
        headers=graphql_headers,
        method=RequestMethod.POST,
        json_data=graphql_payload
    )
    print(f"Generated GraphQL curl command: {graphql_curl_cmd}")
    
    # Test with actual request (mocked)
    print("\n3. Testing debug logging during actual request:")
    
    with patch('openhands.integrations.gitlab.gitlab_service.httpx.AsyncClient') as mock_client:
        # Mock the response
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'id': 1, 'username': 'test'}
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.raise_for_status.return_value = None
        
        mock_client_instance = AsyncMock()
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        # Mock execute_request method
        with patch.object(service, 'execute_request', return_value=mock_response):
            try:
                # This should generate debug log messages with curl commands
                result, headers = await service._make_request(
                    url='http://gitlab.example.com/api/v4/user',
                    params={'test': 'value'}
                )
                print("Request completed successfully!")
                print(f"Result: {result}")
            except Exception as e:
                print(f"Request failed: {e}")
    
    print("\n4. Testing GraphQL request debug logging:")
    
    with patch('openhands.integrations.gitlab.gitlab_service.httpx.AsyncClient') as mock_client:
        # Mock the GraphQL response
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': {'currentUser': {'id': '1', 'username': 'test'}}}
        mock_response.raise_for_status.return_value = None
        
        mock_client_instance = AsyncMock()
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        mock_client_instance.post.return_value = mock_response
        
        try:
            # This should generate debug log messages with GraphQL curl commands
            result = await service.execute_graphql_query(
                query='query { currentUser { id username } }',
                variables={}
            )
            print("GraphQL request completed successfully!")
            print(f"Result: {result}")
        except Exception as e:
            print(f"GraphQL request failed: {e}")
    
    print("\nTest completed!")


if __name__ == '__main__':
    asyncio.run(test_gitlab_debug_curl_commands())
