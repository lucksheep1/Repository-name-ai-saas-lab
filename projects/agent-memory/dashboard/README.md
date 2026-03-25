# Agent Memory Dashboard

A lightweight web dashboard for viewing and managing Agent Memory entries.

## Quick Start

```bash
cd dashboard
pip install flask
python app.py
```

Then open http://localhost:5000

## Features

- View all memory entries
- Search memories
- Filter by tags
- View TTL status
- Export to JSON

## API Endpoints

- `GET /api/memories` - List all memories
- `GET /api/memories/<id>` - Get single memory
- `GET /api/stats` - Get memory statistics