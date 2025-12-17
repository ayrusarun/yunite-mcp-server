#!/usr/bin/env python3
"""
Yunite MCP Server

Basic MCP server with HTTP transport for the Yunite platform.
Runs on port 7000 by default.
"""

import os
import json
import asyncio
from typing import Any, Optional

import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent
from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import Response
import uvicorn
from sse_starlette import EventSourceResponse
from mcp.server.stdio import stdio_server
import anyio

# Load environment variables
load_dotenv()

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
SERVER_PORT = int(os.getenv("SERVER_PORT", "7000"))

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
    """List available tools"""
    return [
        Tool(
            name="list_departments",
            description="List all departments in the college",
            inputSchema={
                "type": "object",
                "properties": {
                    "include_stats": {
                        "type": "boolean",
                        "description": "Include statistics about students and programs",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="list_programs",
            description="List academic programs",
            inputSchema={
                "type": "object",
                "properties": {
                    "department_id": {
                        "type": "integer",
                        "description": "Filter by department ID (optional)"
                    },
                    "include_stats": {
                        "type": "boolean",
                        "description": "Include statistics",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="list_cohorts",
            description="List cohorts (batches/year groups)",
            inputSchema={
                "type": "object",
                "properties": {
                    "program_id": {
                        "type": "integer",
                        "description": "Filter by program ID (optional)"
                    },
                    "admission_year": {
                        "type": "integer",
                        "description": "Filter by admission year (optional)"
                    },
                    "include_stats": {
                        "type": "boolean",
                        "description": "Include statistics",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="list_sections",
            description="List sections/classes",
            inputSchema={
                "type": "object",
                "properties": {
                    "cohort_id": {
                        "type": "integer",
                        "description": "Filter by cohort ID (optional)"
                    },
                    "program_id": {
                        "type": "integer",
                        "description": "Filter by program ID (optional)"
                    },
                    "include_stats": {
                        "type": "boolean",
                        "description": "Include statistics",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="get_user_profile",
            description="Get the current user's profile information",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="list_posts",
            description="List posts/announcements from the community",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of posts to retrieve",
                        "default": 20
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Offset for pagination",
                        "default": 0
                    }
                }
            }
        ),
        Tool(
            name="create_post",
            description="Create a new post/announcement",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Post content"
                    },
                    "title": {
                        "type": "string",
                        "description": "Post title (optional)"
                    }
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="get_user_groups",
            description="Get groups the user belongs to",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    
    try:
        if name == "list_departments":
            params = {}
            if arguments.get("include_stats"):
                params["include_stats"] = True
            result = await make_api_request("GET", "/departments/", params=params)
            
        elif name == "list_programs":
            params = {}
            if arguments.get("department_id"):
                params["department_id"] = arguments["department_id"]
            if arguments.get("include_stats"):
                params["include_stats"] = True
            result = await make_api_request("GET", "/academic/programs", params=params)
            
        elif name == "list_cohorts":
            params = {}
            if arguments.get("program_id"):
                params["program_id"] = arguments["program_id"]
            if arguments.get("admission_year"):
                params["admission_year"] = arguments["admission_year"]
            if arguments.get("include_stats"):
                params["include_stats"] = True
            result = await make_api_request("GET", "/academic/cohorts", params=params)
            
        elif name == "list_sections":
            params = {}
            if arguments.get("cohort_id"):
                params["cohort_id"] = arguments["cohort_id"]
            if arguments.get("program_id"):
                params["program_id"] = arguments["program_id"]
            if arguments.get("include_stats"):
                params["include_stats"] = True
            result = await make_api_request("GET", "/academic/classes", params=params)
            
        elif name == "get_user_profile":
            result = await make_api_request("GET", "/users/me")
            
        elif name == "list_posts":
            params = {
                "limit": arguments.get("limit", 20),
                "offset": arguments.get("offset", 0)
            }
            result = await make_api_request("GET", "/posts/", params=params)
            
        elif name == "create_post":
            data = {
                "content": arguments["content"],
                "title": arguments.get("title")
            }
            result = await make_api_request("POST", "/posts/", data=data)
            
        elif name == "get_user_groups":
            result = await make_api_request("GET", "/user-groups/my-groups")
            
        else:
            result = {"error": True, "message": f"Unknown tool: {name}"}
        
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


# HTTP/SSE endpoints for MCP
async def handle_sse(request):
    """Handle SSE connections for MCP"""
    from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream
    
    async def event_generator():
        # Create memory streams for communication
        read_stream_send, read_stream_receive = anyio.create_memory_object_stream(0)
        write_stream_send, write_stream_receive = anyio.create_memory_object_stream(0)
        
        async def run_server():
            async with read_stream_send, write_stream_receive:
                await app.run(
                    read_stream_receive,
                    write_stream_send,
                    app.create_initialization_options()
                )
        
        # Start server in background
        async with anyio.create_task_group() as tg:
            tg.start_soon(run_server)
            
            # Send events
            async with write_stream_receive:
                async for message in write_stream_receive:
                    yield {
                        "event": "message",
                        "data": message
                    }
    
    return EventSourceResponse(event_generator())


async def handle_messages(request):
    """Handle HTTP POST for messages"""
    return Response(content='{"status": "ok"}', media_type="application/json")


async def handle_health(request):
    """Health check endpoint"""
    return Response(content='{"status": "healthy"}', media_type="application/json")


# Create Starlette app
starlette_app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Route("/messages", endpoint=handle_messages, methods=["POST"]),
        Route("/health", endpoint=handle_health),
    ]
)


def main():
    """Start the HTTP server on port 7000"""
    print(f"🚀 Starting Yunite MCP Server on http://localhost:{SERVER_PORT}")
    print(f"   SSE endpoint: http://localhost:{SERVER_PORT}/sse")
    print(f"   API Base URL: {API_BASE_URL}")
    print(f"   Admin User: {ADMIN_USERNAME}")
    
    # Test token generation on startup
    import asyncio
    try:
        token = asyncio.run(get_api_token())
        print(f"   ✅ Token generated successfully")
    except Exception as e:
        print(f"   ❌ Failed to generate token: {e}")
        print(f"   Please check your ADMIN_USERNAME and ADMIN_PASSWORD in .env")
        return
    
    uvicorn.run(starlette_app, host="0.0.0.0", port=SERVER_PORT)


if __name__ == "__main__":
    main()
