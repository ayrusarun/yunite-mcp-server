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

#### Option A: Run Directly
```bash
python3 server.py
```

#### Option B: Run with Docker
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

The server will start on `http://localhost:7000`

## Available Tools

### View/List Tools
- `list_departments` - List all departments
- `list_programs` - List academic programs
- `list_cohorts` - List cohorts (batches)
- `list_sections` - List sections/classes
- `get_user_profile` - Get current user profile
- `list_posts` - List community posts
- `get_user_groups` - Get user's groups

### Create Tools (Academic Admin)
- `create_department` - Create a new department
- `create_program` - Create an academic program
- `create_cohort` - Create a cohort (batch/year group)
- `create_section` - Create a section/class
- `create_student` - Create a new student user
- `create_staff` - Create a new staff/faculty user
- `create_post` - Create a new post

### Update Tools
- `update_user_profile` - Update user profile information

## Connect from Claude Desktop

### For Direct Run
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

### For Docker Run
Use the same configuration (see `claude_config_docker.json`):

```json
{
  "mcpServers": {
    "yunite-docker": {
      "url": "http://localhost:7000/sse",
      "transport": "sse"
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
