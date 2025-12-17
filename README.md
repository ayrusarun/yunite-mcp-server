# Yunite MCP Server

HTTP/SSE-based MCP server for the Yunite platform running on port 7000.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update your credentials:

```bash
cp .env.example .env
# Edit .env and add your ADMIN_USERNAME and ADMIN_PASSWORD
```

### 3. Start the Server

```bash
python3 server.py
```

The server will start on `http://localhost:7000`

## Available Tools

- `list_departments` - List all departments
- `list_programs` - List academic programs
- `list_cohorts` - List cohorts (batches)
- `list_sections` - List sections/classes
- `get_user_profile` - Get current user profile
- `list_posts` - List community posts
- `create_post` - Create a new post
- `get_user_groups` - Get user's groups

## Connect from Claude Desktop

Add to your `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "yunite": {
      "url": "http://localhost:7000/sse"
    }
  }
}
```

## Testing

Test the server is running:

```bash
curl http://localhost:7000/sse
```
# yunite-mcp-server
