# The Price Is Right - AI Deal Hunter

A modular, Docker-based, multi-agent AI application that watches RSS feeds for products, estimates their true market price using an ensemble of AI models, and sends push notifications for great opportunities.

## Repository Structure

```
priceisrightcapstone/
├── app/
│   ├── agents/          # All 7 agent modules
│   ├── core/            # Data models, config, RAG DB
│   ├── models/          # PyTorch DNN definition
│   ├── ui/              # Gradio dashboard + settings
│   ├── api.py           # FastAPI REST API layer
│   └── main.py          # Entry point
├── tests/               # Test suite with markdown reports
├── scripts/             # Utility scripts
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── manage.sh            # Linux/macOS management script
└── manage.ps1           # Windows PowerShell management script
```

## Quick Start

### Linux / macOS
```bash
cd priceisrightcapstone
chmod +x manage.sh
./manage.sh deploy
```

### Windows (PowerShell)
```powershell
cd priceisrightcapstone
.\manage.ps1 deploy
```

Access the dashboard at `http://localhost:7860`.

## Management Commands

| Command | Description |
|---------|-------------|
| `deploy` | Pull latest from GitHub, build and start all containers |
| `update` | Pull latest from GitHub and rebuild/restart containers |
| `start` | Start all containers in background |
| `stop` | Stop all containers |
| `test` | Run unit tests and generate markdown report |
| `patch` | Apply a quick patch and restart services |
| `status` | Show container status |

## Configuration

Copy `.env.example` to `.env` and fill in your API keys:
- `OPENAI_API_KEY` — Required for Scanner and Frontier agents
- `ANTHROPIC_API_KEY` — Required for Messaging agent (Claude Sonnet)
- `PUSHOVER_USER` & `PUSHOVER_TOKEN` — Required for push notifications
- `MODAL_TOKEN_ID` & `MODAL_TOKEN_SECRET` — Optional for Specialist agent

---

## Disclaimer
Lalit Nayyar | lalitnayyar@gmail.com | +971508320336 | +919595353336
