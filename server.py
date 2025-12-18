#!/usr/bin/env python3
"""
Yunite MCP Server

MCP server with stdio transport for the Yunite platform.
Provides comprehensive read access to all API endpoints.
"""

import os
import json
import asyncio
from typing import Any, Optional

import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent
from dotenv import load_dotenv
from mcp.server.stdio import stdio_server
from tools_comprehensive import get_comprehensive_tools
from tool_handlers import handle_tool_call
from tools_write import get_write_tools
from tool_handlers_write import handle_write_tool_call

# Load environment variables
load_dotenv()

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")

# Initialize MCP server
app = Server("yunite-mcp-server")

# Cache for API token
_api_token_cache = {"token": None, "expires_at": 0}


async def get_api_token() -> str:
    """Get or refresh API token"""
    import time
    
    # Check if cached token is still valid (with 5 minute buffer)
    if _api_token_cache["token"] and _api_token_cache["expires_at"] > time.time() + 300:
        return _api_token_cache["token"]
    
    # Get new token
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/auth/login",
            json={
                "username": ADMIN_USERNAME,
                "password": ADMIN_PASSWORD
            }
        )
        response.raise_for_status()
        data = response.json()
        
        # Cache the token
        _api_token_cache["token"] = data["access_token"]
        
        # Decode JWT to get expiration (simple base64 decode)
        import base64
        import json as json_module
        try:
            payload = data["access_token"].split('.')[1]
            # Add padding if needed
            payload += '=' * (4 - len(payload) % 4)
            decoded = json_module.loads(base64.b64decode(payload))
            _api_token_cache["expires_at"] = decoded.get("exp", 0)
        except:
            # If decode fails, cache for 1 hour
            _api_token_cache["expires_at"] = time.time() + 3600
        
        return _api_token_cache["token"]


async def get_headers():
    """Get headers with authentication token"""
    token = await get_api_token()
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


async def make_api_request(
    method: str,
    endpoint: str,
    data: Optional[dict] = None,
    params: Optional[dict] = None
) -> dict:
    """Make an API request to the API"""
    url = f"{API_BASE_URL}{endpoint}"
    headers = await get_headers()
    
    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, params=params)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=data)
            elif method.upper() == "PUT":
                response = await client.put(url, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": True,
                "status_code": e.response.status_code,
                "message": str(e),
                "detail": e.response.text
            }
        except Exception as e:
            return {
                "error": True,
                "message": str(e)
            }


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools - comprehensive API coverage (74 read + 53 write = 127 tools)"""
    return get_comprehensive_tools() + get_write_tools()


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls - 74 read tools + 53 write tools"""
    
    try:
        # Try comprehensive READ handler first
        result = await handle_tool_call(name, arguments, make_api_request)
        
        # If not found in read tools, try WRITE tools
        # Check if result is a dict before using .get() method
        if isinstance(result, dict) and result.get("error") and result.get("message", "").startswith("Unknown tool"):
            result = await handle_write_tool_call(name, arguments, make_api_request)
        
        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]
        
    except Exception as e:
        return [
            TextContent(
                type="text",
                text=json.dumps({
                    "error": True,
                    "message": str(e)
                }, indent=2)
            )
        ]


async def main():
    """Main entry point for stdio transport"""
    import sys
    
    # Log startup to stderr (stdout is reserved for MCP protocol)
    print(f"🚀 Starting Yunite MCP Server (stdio transport)", file=sys.stderr)
    print(f"   API Base URL: {API_BASE_URL}", file=sys.stderr)
    print(f"   Admin User: {ADMIN_USERNAME}", file=sys.stderr)
    
    # Test token generation on startup
    try:
        token = await get_api_token()
        print(f"   ✅ Token generated successfully", file=sys.stderr)
    except Exception as e:
        print(f"   ❌ Failed to generate token: {e}", file=sys.stderr)
        print(f"   Please check your ADMIN_USERNAME and ADMIN_PASSWORD in .env", file=sys.stderr)
        sys.exit(1)
    
    # Run the server with stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
