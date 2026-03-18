# Agent Memory - Docker Example

Simple Dockerfile to run agent-memory in a container.

## Quick Start

```bash
# Build
docker build -t agent-memory .

# Run
docker run -v $(pwd)/data:/app/data agent-memory

# Or with custom config
docker run -v $(pwd)/data:/app/data \
  -e STORAGE=sqlite \
  -e PATH=/app/data/memory.db \
  agent-memory
```

## Environment Variables

- `STORAGE` - Storage backend: json, sqlite (default: json)
- `PATH` - Path for memory file/db (default: ./memory.json)
- `TTL_DAYS` - Default TTL in days (optional)

## Docker Compose

```yaml
version: '3.8'
services:
  agent-memory:
    build: .
    volumes:
      - ./data:/app/data
    environment:
      - STORAGE=sqlite
      - PATH=/app/data/memory.db
    ports:
      - "8000:8000"
```

## Build & Run API Server

```bash
# Build
docker build -t agent-memory-api -f Dockerfile.api .

# Run API
docker run -v $(pwd)/data:/app/data -p 8000:8000 agent-memory-api
```
