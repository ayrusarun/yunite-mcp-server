# Docker Deployment Guide

## Quick Start

### 1. Update Environment Variables
Edit `.env` file with your credentials:
```bash
API_BASE_URL=http://host.docker.internal:8000
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_password
SERVER_PORT=7000
```

### 2. Build and Run

#### Using docker-compose (Recommended):
```bash
# Start the container
docker-compose up -d

# View logs
docker-compose logs -f yunite-mcp-server

# Stop
docker-compose down
```

#### Using docker directly:
```bash
# Build image
docker build -t yunite-mcp-server .

# Run container
docker run -d \
  --name yunite-mcp-server \
  -p 7000:7000 \
  -e API_BASE_URL=http://host.docker.internal:8000 \
  -e ADMIN_USERNAME=your_username \
  -e ADMIN_PASSWORD=your_password \
  yunite-mcp-server

# View logs
docker logs -f yunite-mcp-server

# Stop
docker stop yunite-mcp-server
docker rm yunite-mcp-server
```

### 3. Configure Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

### 4. Verify

Test the server is running:
```bash
curl http://localhost:7000/health
```

Expected response:
```json
{"status": "healthy"}
```

## Troubleshooting

### Container won't start
Check logs:
```bash
docker-compose logs yunite-mcp-server
```

### Can't connect to host API
The Docker container uses `host.docker.internal:8000` to connect to your local API.
If this doesn't work, you can:

1. Find your host IP:
   ```bash
   ipconfig getifaddr en0  # macOS
   ```

2. Update `API_BASE_URL` in `.env`:
   ```
   API_BASE_URL=http://YOUR_IP:8000
   ```

3. Restart:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

### SSL Certificate Issues
If you get SSL errors, the Dockerfile already includes:
```dockerfile
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

## Useful Commands

```bash
# Rebuild image
docker-compose build

# Restart container
docker-compose restart

# View container stats
docker stats yunite-mcp-server

# Enter container shell
docker exec -it yunite-mcp-server sh

# Remove all
docker-compose down -v
docker rmi yunite-mcp-server
```
