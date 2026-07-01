# The Price Is Right - AI Deal Hunter

A modular, Docker-based, multi-agent AI application that watches RSS feeds for products, estimates their true market price using an ensemble of AI models, and sends push notifications for great opportunities.

## Features

- **7 Collaborating AI Agents:** Scanner, Frontier (RAG), Specialist (Fine-tuned), Neural Network (DNN), Ensemble, Messaging, and Planning.
- **Gradio Dashboard:** Responsive mobile/desktop UI with dark/light theme toggle.
- **Live Settings:** Configure API keys, agent weights, and parameters on the fly.
- **Dockerized:** Fully containerized with deployment scripts for Linux and Windows.
- **Test Suite:** Comprehensive tests with timestamped Markdown reports.

## Quick Start

### Linux / macOS
```bash
chmod +x manage.sh
./manage.sh deploy
```

### Windows (PowerShell)
```powershell
.\manage.ps1 deploy
```

Access the dashboard at `http://localhost:7860`.

## Configuration

Update the following values in your `.env` file or via the Settings tab in the Dashboard:
- `OPENAI_API_KEY`: Required for Scanner and Frontier agents.
- `ANTHROPIC_API_KEY`: Required for Messaging agent.
- `PUSHOVER_USER` & `PUSHOVER_TOKEN`: Required for push notifications.

## Diagnostic / Testing

Run the test suite to verify all components:
```bash
./manage.sh test
```
Check the `tests/reports/` directory for the markdown output.

---

## Disclaimer
Lalit Nayyar | lalitnayyar@gmail.com | +971508320336 | +919595353336
