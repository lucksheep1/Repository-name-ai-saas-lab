# 🚀 Agent Memory Web Dashboard

A lightweight Flask-based web dashboard for viewing and managing your Agent Memory entries.

![Dashboard Preview](https://lucksheep1.github.io/Repository-name-ai-saas-lab/demo.html)

## Quick Start

```bash
# Install dependencies
cd dashboard
pip install -r requirements.txt

# Install agent-memory (from parent)
cd ..
pip install -e .

# Run dashboard
cd dashboard
python app.py
```

Then open http://localhost:5000

## Features

- 📊 **Dashboard View** - See all memory entries at a glance
- 🔍 **Search** - Full-text search across all memories
- 🏷️ **Tags** - Filter and view tags
- ⏰ **TTL Status** - See expiration time for each memory
- 📤 **Export** - Export all memories as JSON

## Screenshots

```
┌─────────────────────────────────────────┐
│  🧠 Agent Memory Dashboard              │
│  ┌──────────┐  ┌──────────┐            │
│  │ 42 Total  │  │  8 Tags  │            │
│  │ Memories  │  │          │            │
│  └──────────┘  └──────────┘            │
├─────────────────────────────────────────┤
│ [Search...              ] [Search] [Export] │
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │
│ │ #a1b2c3d4  ⏰ 2h left               │ │
│ │ User prefers dark mode              │ │
│ │ 2026-03-25 12:00  [preference]     │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard |
| `/api/memories` | GET | List all memories (JSON) |
| `/api/stats` | GET | Get statistics |
| `/api/export` | GET | Export all memories |

## Docker (Optional)

```dockerfile
FROM python:3.10
WORKDIR /app
COPY dashboard/ .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

## Next Steps

- [ ] Add memory creation UI
- [ ] Add TTL editing
- [ ] Add memory deletion
- [ ] Add dark/light theme toggle

---
*Added: 2026-03-25 (Cycle 32)*