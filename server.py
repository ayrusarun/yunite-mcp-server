#!/usr/bin/env python3
"""
Yunite MCP Server

MCP server with stdio transport for the Yunite platform.
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
        ),
        # Academic Admin Tools
        Tool(
            name="create_department",
            description="Create a new department in the college",
            inputSchema={
                "type": "object",
                "properties": {
                    "college_id": {
                        "type": "integer",
                        "description": "College ID"
                    },
                    "name": {
                        "type": "string",
                        "description": "Department name"
                    },
                    "code": {
                        "type": "string",
                        "description": "Department code (e.g., CS, EE, ME)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Department description (optional)"
                    },
                    "is_active": {
                        "type": "boolean",
                        "description": "Whether the department is active",
                        "default": True
                    }
                },
                "required": ["college_id", "name", "code"]
            }
        ),
        Tool(
            name="create_program",
            description="Create an academic program under a department",
            inputSchema={
                "type": "object",
                "properties": {
                    "college_id": {
                        "type": "integer",
                        "description": "College ID"
                    },
                    "department_id": {
                        "type": "integer",
                        "description": "Department ID"
                    },
                    "code": {
                        "type": "string",
                        "description": "Program code (e.g., BTECH-CS, MBA)"
                    },
                    "name": {
                        "type": "string",
                        "description": "Program name"
                    },
                    "short_name": {
                        "type": "string",
                        "description": "Short name (optional)"
                    },
                    "duration_years": {
                        "type": "integer",
                        "description": "Duration in years"
                    },
                    "description": {
                        "type": "string",
                        "description": "Program description (optional)"
                    },
                    "is_active": {
                        "type": "boolean",
                        "description": "Whether the program is active",
                        "default": True
                    }
                },
                "required": ["college_id", "department_id", "code", "name", "duration_years"]
            }
        ),
        Tool(
            name="create_cohort",
            description="Create a cohort (batch/year group) for a program",
            inputSchema={
                "type": "object",
                "properties": {
                    "college_id": {
                        "type": "integer",
                        "description": "College ID"
                    },
                    "program_id": {
                        "type": "integer",
                        "description": "Program ID"
                    },
                    "admission_year": {
                        "type": "integer",
                        "description": "Admission year (e.g., 2024)"
                    },
                    "code": {
                        "type": "string",
                        "description": "Cohort code (e.g., BTECH-CS-2024)"
                    },
                    "name": {
                        "type": "string",
                        "description": "Cohort name"
                    },
                    "expected_graduation_year": {
                        "type": "integer",
                        "description": "Expected graduation year (optional)"
                    },
                    "current_semester": {
                        "type": "integer",
                        "description": "Current semester",
                        "default": 1
                    },
                    "is_active": {
                        "type": "boolean",
                        "description": "Whether the cohort is active",
                        "default": True
                    }
                },
                "required": ["college_id", "program_id", "admission_year", "code", "name"]
            }
        ),
        Tool(
            name="create_section",
            description="Create a section/class for a cohort",
            inputSchema={
                "type": "object",
                "properties": {
                    "college_id": {
                        "type": "integer",
                        "description": "College ID"
                    },
                    "cohort_id": {
                        "type": "integer",
                        "description": "Cohort ID"
                    },
                    "program_id": {
                        "type": "integer",
                        "description": "Program ID"
                    },
                    "section_code": {
                        "type": "string",
                        "description": "Section code (e.g., A, B, C)"
                    },
                    "section_name": {
                        "type": "string",
                        "description": "Section name (optional)"
                    },
                    "capacity": {
                        "type": "integer",
                        "description": "Maximum capacity (optional)"
                    },
                    "is_active": {
                        "type": "boolean",
                        "description": "Whether the section is active",
                        "default": True
                    }
                },
                "required": ["college_id", "cohort_id", "program_id", "section_code"]
            }
        ),
        Tool(
            name="create_student",
            description="Create a new student user",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "Student username"
                    },
                    "email": {
                        "type": "string",
                        "description": "Student email"
                    },
                    "full_name": {
                        "type": "string",
                        "description": "Student full name"
                    },
                    "password": {
                        "type": "string",
                        "description": "Student password"
                    },
                    "college_id": {
                        "type": "integer",
                        "description": "College ID"
                    },
                    "department_id": {
                        "type": "integer",
                        "description": "Department ID"
                    },
                    "program_id": {
                        "type": "integer",
                        "description": "Program ID"
                    },
                    "cohort_id": {
                        "type": "integer",
                        "description": "Cohort ID"
                    },
                    "class_id": {
                        "type": "integer",
                        "description": "Section/Class ID"
                    },
                    "admission_year": {
                        "type": "integer",
                        "description": "Admission year"
                    }
                },
                "required": ["username", "email", "full_name", "password", "college_id", "department_id", "program_id", "cohort_id", "class_id", "admission_year"]
            }
        ),
        Tool(
            name="create_staff",
            description="Create a new staff/faculty user",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "Staff username"
                    },
                    "email": {
                        "type": "string",
                        "description": "Staff email"
                    },
                    "full_name": {
                        "type": "string",
                        "description": "Staff full name"
                    },
                    "password": {
                        "type": "string",
                        "description": "Staff password"
                    },
                    "college_id": {
                        "type": "integer",
                        "description": "College ID"
                    },
                    "department_id": {
                        "type": "integer",
                        "description": "Department ID (optional)"
                    },
                    "role": {
                        "type": "string",
                        "description": "Staff role (e.g., faculty, staff, admin)",
                        "default": "staff"
                    }
                },
                "required": ["username", "email", "full_name", "password", "college_id", "role"]
            }
        ),
        Tool(
            name="update_user_profile",
            description="Update a user's profile information",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "User ID to update"
                    },
                    "full_name": {
                        "type": "string",
                        "description": "Full name (optional)"
                    },
                    "email": {
                        "type": "string",
                        "description": "Email (optional)"
                    },
                    "bio": {
                        "type": "string",
                        "description": "Bio (optional)"
                    },
                    "profile_picture": {
                        "type": "string",
                        "description": "Profile picture URL (optional)"
                    }
                },
                "required": ["user_id"]
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
        
        # Academic Admin Tools
        elif name == "create_department":
            data = {
                "name": arguments["name"],
                "code": arguments["code"],
                "description": arguments.get("description"),
                "is_active": arguments.get("is_active", True)
            }
            result = await make_api_request("POST", "/departments/", data=data)
            
        elif name == "create_program":
            data = {
                "college_id": arguments["college_id"],
                "department_id": arguments["department_id"],
                "code": arguments["code"],
                "name": arguments["name"],
                "short_name": arguments.get("short_name"),
                "duration_years": arguments["duration_years"],
                "description": arguments.get("description"),
                "is_active": arguments.get("is_active", True)
            }
            result = await make_api_request("POST", "/academic/programs", data=data)
            
        elif name == "create_cohort":
            data = {
                "college_id": arguments["college_id"],
                "program_id": arguments["program_id"],
                "admission_year": arguments["admission_year"],
                "code": arguments["code"],
                "name": arguments["name"],
                "expected_graduation_year": arguments.get("expected_graduation_year"),
                "current_semester": arguments.get("current_semester", 1),
                "is_active": arguments.get("is_active", True)
            }
            result = await make_api_request("POST", "/academic/cohorts", data=data)
            
        elif name == "create_section":
            data = {
                "college_id": arguments["college_id"],
                "cohort_id": arguments["cohort_id"],
                "program_id": arguments["program_id"],
                "section_code": arguments["section_code"],
                "section_name": arguments.get("section_name"),
                "capacity": arguments.get("capacity"),
                "is_active": arguments.get("is_active", True)
            }
            result = await make_api_request("POST", "/academic/classes", data=data)
            
        elif name == "create_student":
            data = {
                "username": arguments["username"],
                "email": arguments["email"],
                "full_name": arguments["full_name"],
                "password": arguments["password"],
                "college_id": arguments["college_id"],
                "department_id": arguments["department_id"],
                "program_id": arguments["program_id"],
                "cohort_id": arguments["cohort_id"],
                "class_id": arguments["class_id"],
                "admission_year": arguments["admission_year"],
                "role": "student"
            }
            result = await make_api_request("POST", "/admin/users", data=data)
            
        elif name == "create_staff":
            data = {
                "username": arguments["username"],
                "email": arguments["email"],
                "full_name": arguments["full_name"],
                "password": arguments["password"],
                "college_id": arguments["college_id"],
                "role": arguments.get("role", "staff")
            }
            if arguments.get("department_id"):
                data["department_id"] = arguments["department_id"]
            result = await make_api_request("POST", "/admin/users", data=data)
            
        elif name == "update_user_profile":
            user_id = arguments["user_id"]
            data = {}
            if arguments.get("full_name"):
                data["full_name"] = arguments["full_name"]
            if arguments.get("email"):
                data["email"] = arguments["email"]
            if arguments.get("bio"):
                data["bio"] = arguments["bio"]
            if arguments.get("profile_picture"):
                data["profile_picture"] = arguments["profile_picture"]
            result = await make_api_request("PUT", f"/users/{user_id}", data=data)
            
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
