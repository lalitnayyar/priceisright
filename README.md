# 📊 The Price Is Right — AI Deal Hunter

**The Price Is Right** is a modular, Docker-based, multi-agent AI application designed to autonomously hunt for online product deals. It watches RSS feeds, estimates the true market price of products using an ensemble of 7 specialized AI models, and sends push notifications when it discovers significant arbitrage opportunities.

---

## 📸 Application Screenshots

### 🖥️ Dashboard View
The main dashboard provides a real-time view of the agent framework, recently discovered deals, live terminal logs, and the RAG vector store capacity.

![Dashboard](docs/screenshots/dashboard_mobile.png)

### ⚙️ Settings View
The live settings page allows you to configure API keys, agent parameters, ensemble weights, and RSS feeds on the fly without restarting the application.

![Settings](docs/screenshots/settings_mobile.png)

---

## 🧠 7-Agent AI Framework

The core of the application is a pipeline orchestrated by 7 distinct AI agents working in harmony:

![Agent Pipeline](docs/screenshots/agent_pipeline.png)

1. **Scanner Agent (GPT-4o-mini):** Parses RSS feeds, extracts product listings, and identifies the best deal candidates using structured JSON outputs.
2. **Frontier Agent (GPT-4o + RAG):** Queries the local ChromaDB vector store for similar historical products and uses the retrieved context to estimate the true market price.
3. **Specialist Agent (Llama-3.2-3B):** Calls a fine-tuned model hosted on Modal GPU, trained specifically on product price prediction to "bust the frontier."
4. **Neural Network Agent (PyTorch):** Runs the product features through a fast, local 5-layer residual Deep Neural Network (DNN) for an offline price estimate.
5. **Ensemble Agent:** Aggregates the estimates from the Frontier, Specialist, and DNN agents using configurable weights to determine the final true value and calculate the discount percentage.
6. **Messaging Agent (Claude 3.5 Sonnet):** Crafts a compelling, concise push notification message and sends it via the Pushover API to your device.
7. **Planning Agent (Orchestrator):** Coordinates the entire pipeline, handles parallel execution, logs every step, and saves results to the local memory store.

---

## 🏗️ Architecture & Docker Services

The application is fully containerized and consists of four main Docker services:

![Docker Architecture](docs/screenshots/docker_services.png)

- **`chromadb`:** The persistent vector database storing product embeddings.
- **`rag-init`:** A one-off initialization script that populates ChromaDB with sample data.
- **`api`:** The FastAPI REST API layer handling background tasks and state management.
- **`app`:** The Gradio-based web UI providing the dashboard and settings interface.

---

## 🚀 User Guide & Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git installed
- API Keys: OpenAI (Required), Anthropic (Required), Pushover (Required for notifications)

### Installation

Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/lalitnayyar/priceisright.git
cd priceisright/priceisrightcapstone
```

### Configuration

Copy the example environment file and fill in your API keys:
```bash
cp .env.example .env
```

Open `.env` and add your keys:
```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
PUSHOVER_USER=...
PUSHOVER_TOKEN=...
```

### Deployment

We provide unified management scripts for both Linux/macOS and Windows.

**Linux / macOS:**
```bash
chmod +x manage.sh
./manage.sh deploy
```

**Windows (PowerShell):**
```powershell
.\manage.ps1 deploy
```

Once deployed, access the dashboard at **[http://localhost:7860](http://localhost:7860)**.

---

## 🛠️ Management Commands

Use the `manage.sh` (Linux) or `manage.ps1` (Windows) scripts to control the application:

| Command | Description |
|---------|-------------|
| `deploy` | Pull latest code, build images, and start all containers |
| `update` | Pull latest code and restart containers |
| `start` | Start all containers in the background |
| `stop` | Stop all running containers |
| `test` | Run the 118-test suite and generate a Markdown report |
| `patch` | Apply a quick code patch and restart the API/App services |
| `status` | Show the current status of all Docker containers |

---

## 🧪 Testing

The project includes a comprehensive test suite (118 tests) that validates agent logic, data models, and API endpoints.

To run the tests:
```bash
./manage.sh test
```

Test results are automatically exported as timestamped Markdown files in the `tests/reports/` directory.

---

## 📝 Disclaimer
Lalit Nayyar | lalitnayyar@gmail.com | +971508320336 | +919595353336
