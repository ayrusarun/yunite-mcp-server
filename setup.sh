docker run -d -p 7000:7000 \
  -e API_BASE_URL=http://host.docker.internal:8000 \
  -e ADMIN_USERNAME=arjun_cs \
  -e ADMIN_PASSWORD=password123 \
  --name yunite-mcp \
  yunite-mcp-server