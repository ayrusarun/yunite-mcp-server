#!/bin/bash

echo "🐳 Building Yunite MCP Server Docker Image..."
docker build -t yunite-mcp-server .

echo ""
echo "✅ Build complete!"
echo ""
echo "To run the container:"
echo "  docker-compose up -d"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop:"
echo "  docker-compose down"
