# Yunite MCP Server - stdio Transport Setup

This MCP server now uses **stdio transport** instead of SSE/HTTP, which is more reliable and simpler.

## Architecture

```
Claude Desktop <--stdio--> Docker Container <--HTTP--> Yunite API Server
```

## Setup Instructions

### 1. Configure Environment Variables

Edit `.env` file:
```bash
API_BASE_URL=http://172.17.0.1:8000
ADMIN_USERNAME=arjun_cs
ADMIN_PASSWORD=password123
```

### 2. Build and Start the Docker Container

```bash
# Build the image
docker-compose build

# Start the container (it will stay running)
docker-compose up -d

# Check logs
docker-compose logs -f
```

### 3. Configure Claude Desktop

Copy the config to your Claude Desktop settings:

**For macOS/Linux:**
```bash
cp claude_config_docker.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**For Windows:**
```bash
copy claude_config_docker.json %APPDATA%\Claude\claude_desktop_config.json
```

Or manually copy this config:

```json
{
  "mcpServers": {
    "yunite": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "yunite-mcp-server",
        "python3",
        "server.py"
      ]
    }
  }
}
```

### 4. Restart Claude Desktop

Completely quit and restart Claude Desktop for the changes to take effect.

## Verification

1. **Check container is running:**
   ```bash
   docker ps | grep yunite-mcp-server
   ```

2. **Check API connectivity:**
   ```bash
   docker exec yunite-mcp-server curl -s http://172.17.0.1:8000/health
   ```

3. **Test the MCP server directly:**
   ```bash
   docker exec -i yunite-mcp-server python3 server.py
   # Should show startup messages and wait for input
   # Press Ctrl+C to exit
   ```

4. **In Claude Desktop:**
   - Look for the 🔌 icon in the bottom right
   - Click it to see connected MCP servers
   - "yunite" should be listed

## Troubleshooting

### Container not starting
```bash
docker-compose logs
```

### Authentication errors
```bash
# Check if credentials work
docker exec yunite-mcp-server python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
print(f'API_BASE_URL: {os.getenv(\"API_BASE_URL\")}')
print(f'ADMIN_USERNAME: {os.getenv(\"ADMIN_USERNAME\")}')
"
```

### Claude Desktop not connecting
1. Ensure Docker is running
2. Ensure container is running: `docker ps | grep yunite-mcp-server`
3. Check Claude Desktop logs (usually in ~/Library/Logs/Claude/)
4. Try restarting both Docker and Claude Desktop

## How It Works

1. Claude Desktop runs `docker exec -i yunite-mcp-server python3 server.py`
2. This creates an interactive session with stdin/stdout
3. Claude communicates with the MCP server via stdio protocol
4. The MCP server makes HTTP requests to your Yunite API
5. Results are returned to Claude via stdout

## Benefits of stdio Transport

- ✅ No port management needed
- ✅ No authentication between Claude and MCP server
- ✅ More reliable connection
- ✅ Standard MCP protocol
- ✅ Works seamlessly with Docker
