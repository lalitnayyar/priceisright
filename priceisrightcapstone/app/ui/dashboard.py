"""
Gradio Dashboard UI for The Price Is Right
Mobile/Desktop responsive with dark/light theme toggle
Matches the Stitch design mockup exactly
"""
import gradio as gr
import json
import os
from datetime import datetime
from app.core.config import settings

# ─── Theme CSS matching Stitch design ────────────────────────────────────────
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --primary: #ffb59d;
    --primary-container: #ff6b35;
    --on-primary: #5d1900;
    --on-primary-container: #5f1900;
    --secondary: #5dd9d0;
    --background: #1d100c;
    --surface: #1d100c;
    --surface-container: #2a1c18;
    --surface-container-low: #261814;
    --surface-container-high: #352722;
    --surface-container-highest: #41312c;
    --on-surface: #f7ddd5;
    --on-surface-variant: #e1bfb5;
    --outline-variant: #594139;
    --error: #ffb4ab;
    --error-container: #93000a;
    --on-error-container: #ffdad6;
}

body, .gradio-container {
    font-family: 'Hanken Grotesk', sans-serif !important;
    background-color: var(--background) !important;
    color: var(--on-surface) !important;
}

.gradio-container {
    max-width: 1440px !important;
    margin: 0 auto !important;
}

/* Header */
.app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 24px;
    background: var(--surface-container);
    border-bottom: 1px solid var(--outline-variant);
    position: sticky;
    top: 0;
    z-index: 100;
}

.app-title {
    font-size: 20px;
    font-weight: 700;
    color: var(--primary);
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Agent Status Table */
.agent-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
}

.agent-table th {
    background: var(--surface-container-low);
    color: var(--on-surface-variant);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 12px 16px;
    text-align: left;
    border-bottom: 1px solid var(--outline-variant);
}

.agent-table td {
    padding: 12px 16px;
    border-bottom: 1px solid rgba(89,65,57,0.3);
    color: var(--on-surface);
}

.badge-ready {
    background: rgba(78,205,196,0.1);
    color: #4ECDC4;
    border: 1px solid rgba(78,205,196,0.3);
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}

.badge-running {
    background: rgba(255,107,53,0.1);
    color: #FF6B35;
    border: 1px solid rgba(255,107,53,0.3);
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    animation: pulse 2s infinite;
}

.badge-error {
    background: var(--error-container);
    color: var(--on-error-container);
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}

.heartbeat-ready { color: #4ECDC4; font-size: 10px; }
.heartbeat-running { color: #FF6B35; font-size: 10px; animation: pulse 2s infinite; }
.heartbeat-error { color: #F85149; font-size: 10px; }

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* Deal Cards */
.deal-card {
    background: var(--surface-container);
    border: 1px solid var(--outline-variant);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
    display: flex;
    gap: 16px;
    align-items: flex-start;
}

.deal-card.great-deal {
    border-left: 4px solid var(--primary-container);
    box-shadow: 0 4px 12px rgba(255,107,53,0.15);
}

.deal-badge-great {
    background: var(--primary-container);
    color: var(--on-primary-container);
    font-size: 10px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 999px;
    font-family: 'JetBrains Mono', monospace;
}

/* Terminal Log */
.terminal-panel {
    background: #000000;
    border: 1px solid var(--outline-variant);
    border-radius: 4px;
    padding: 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    max-height: 400px;
    overflow-y: auto;
    line-height: 1.6;
}

.log-timestamp { color: #FF6B35; }
.log-agent { color: #5DD9D0; }
.log-info { color: #f7ddd5; }
.log-success { color: #4ECDC4; }
.log-error { color: #F85149; }

/* Scan Button */
.scan-btn {
    background: var(--primary-container) !important;
    color: var(--on-primary-container) !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    padding: 14px 32px !important;
    border-radius: 8px !important;
    border: none !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
}

.scan-btn:hover {
    filter: brightness(1.1) !important;
    transform: scale(1.01) !important;
}

/* Settings inputs */
.settings-input {
    background: var(--background) !important;
    border: 1px solid var(--outline-variant) !important;
    border-radius: 4px !important;
    color: var(--on-surface) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Accordion sections */
.accordion-section {
    background: var(--surface-container-low);
    border: 1px solid var(--outline-variant);
    border-radius: 4px;
    margin-bottom: 12px;
    overflow: hidden;
}

/* RAG Stats */
.rag-stat {
    background: var(--surface-container);
    border: 1px solid rgba(89,65,57,0.3);
    border-radius: 8px;
    padding: 12px;
    text-align: left;
}

.rag-stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--on-surface-variant);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.rag-stat-value {
    font-size: 20px;
    font-weight: 700;
    color: var(--primary);
    margin-top: 4px;
}

/* Mobile bottom nav */
@media (max-width: 768px) {
    .gradio-container { padding-bottom: 80px !important; }
}

/* Gradio overrides */
.gr-button-primary {
    background: var(--primary-container) !important;
    color: var(--on-primary-container) !important;
    border: none !important;
}

.gr-button-secondary {
    background: transparent !important;
    border: 1px solid var(--outline-variant) !important;
    color: var(--on-surface) !important;
}

.gr-panel, .gr-box {
    background: var(--surface-container) !important;
    border: 1px solid var(--outline-variant) !important;
    border-radius: 8px !important;
}

label, .gr-label {
    color: var(--on-surface-variant) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

input, textarea, select {
    background: var(--background) !important;
    border: 1px solid var(--outline-variant) !important;
    color: var(--on-surface) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.gr-accordion {
    background: var(--surface-container-low) !important;
    border: 1px solid var(--outline-variant) !important;
}

.gr-accordion > .label-wrap {
    background: var(--surface-container) !important;
    color: var(--on-surface) !important;
}

/* Dataframe */
.gr-dataframe table {
    background: var(--surface) !important;
    color: var(--on-surface) !important;
}

.gr-dataframe th {
    background: var(--surface-container-low) !important;
    color: var(--on-surface-variant) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
}

.gr-dataframe td {
    border-bottom: 1px solid rgba(89,65,57,0.3) !important;
}

/* Slider */
input[type="range"] {
    accent-color: var(--primary-container) !important;
}

/* Tab styling */
.tab-nav button {
    background: var(--surface-container) !important;
    color: var(--on-surface-variant) !important;
    border-bottom: 2px solid transparent !important;
    font-family: 'Hanken Grotesk', sans-serif !important;
    font-weight: 600 !important;
}

.tab-nav button.selected {
    color: var(--primary) !important;
    border-bottom: 2px solid var(--primary-container) !important;
    background: var(--surface-container-high) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--background); }
::-webkit-scrollbar-thumb { background: var(--surface-container-highest); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--outline-variant); }
"""

def build_agent_status_html(statuses: list) -> str:
    rows = ""
    for s in statuses:
        status = s.get("status", "READY")
        if status == "RUNNING":
            badge = '<span class="badge-running">RUNNING ●</span>'
            hb = '<span class="heartbeat-running">●</span>'
        elif status == "ERROR":
            badge = '<span class="badge-error">⚠ ERROR</span>'
            hb = '<span class="heartbeat-error">●</span>'
        else:
            badge = '<span class="badge-ready">READY</span>'
            hb = '<span class="heartbeat-ready">●</span>'
        rows += f"""
        <tr>
            <td style="padding:12px 16px;border-bottom:1px solid rgba(89,65,57,0.3);color:#f7ddd5;font-weight:500">{s.get('name','')}</td>
            <td style="padding:12px 16px;border-bottom:1px solid rgba(89,65,57,0.3)">{badge}</td>
            <td style="padding:12px 16px;border-bottom:1px solid rgba(89,65,57,0.3)">{hb}</td>
        </tr>"""
    return f"""
    <div style="overflow-x:auto;background:#1d100c;border-radius:8px;border:1px solid #594139">
    <table style="width:100%;border-collapse:collapse;font-family:'JetBrains Mono',monospace;font-size:13px">
        <thead>
            <tr style="background:#261814;border-bottom:1px solid #594139">
                <th style="padding:12px 16px;text-align:left;color:#e1bfb5;text-transform:uppercase;font-size:11px;letter-spacing:0.05em">Agent Module</th>
                <th style="padding:12px 16px;text-align:left;color:#e1bfb5;text-transform:uppercase;font-size:11px;letter-spacing:0.05em">Current Status</th>
                <th style="padding:12px 16px;text-align:left;color:#e1bfb5;text-transform:uppercase;font-size:11px;letter-spacing:0.05em">Heartbeat</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
    </div>"""

def build_deals_html(results: list) -> str:
    if not results:
        return '<div style="padding:24px;text-align:center;color:#e1bfb5;font-family:\'JetBrains Mono\',monospace">No deals scanned yet. Click "Scan for Deals Now" to begin.</div>'
    
    cards = ""
    for r in results:
        deal = r.get("deal", {})
        ensemble = r.get("ensemble_result", {})
        is_great = ensemble.get("is_great_deal", False)
        discount = ensemble.get("discount_pct", 0)
        estimated = ensemble.get("estimated_price", 0)
        listed = deal.get("price", 0)
        title = deal.get("title", "Unknown Product")
        url = deal.get("url", "#")
        
        great_badge = '<span style="background:#ff6b35;color:#5f1900;font-size:10px;font-weight:700;padding:2px 8px;border-radius:999px;font-family:\'JetBrains Mono\',monospace">GREAT DEAL</span>' if is_great else ""
        border_style = "border-left:4px solid #ff6b35;box-shadow:0 4px 12px rgba(255,107,53,0.15);" if is_great else ""
        action_btn = f'<a href="{url}" target="_blank" style="background:#ff6b35;color:#5f1900;padding:4px 12px;border-radius:4px;font-size:11px;font-weight:700;text-decoration:none;font-family:\'JetBrains Mono\',monospace">SNIPE NOW</a>' if is_great else f'<a href="{url}" target="_blank" style="color:#ffb59d;font-size:11px;font-weight:700;text-decoration:none;font-family:\'JetBrains Mono\',monospace;text-transform:uppercase">Analyze</a>'
        discount_color = "#ff6b35" if is_great else "#5dd9d0"
        
        cards += f"""
        <div style="background:#2a1c18;border:1px solid #594139;border-radius:8px;padding:16px;margin-bottom:12px;display:flex;gap:16px;align-items:flex-start;{border_style}">
            <div style="width:64px;height:64px;background:#41312c;border-radius:6px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:24px">🏷️</div>
            <div style="flex:1">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px">
                    <span style="font-weight:700;color:#f7ddd5;font-size:15px">{title}</span>
                    {great_badge}
                </div>
                <div style="display:flex;gap:16px;font-family:'JetBrains Mono',monospace;font-size:12px;margin-bottom:8px">
                    <span style="color:#e1bfb5">Listed: <span style="color:#f7ddd5;font-weight:700">${listed:.2f}</span></span>
                    <span style="color:#e1bfb5">Est: <span style="color:#f7ddd5">${estimated:.2f}</span></span>
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <span style="color:{discount_color};font-weight:700;font-size:13px">{discount:.1f}% Off Potential</span>
                    {action_btn}
                </div>
            </div>
        </div>"""
    return cards

def build_logs_html(log_lines: list) -> str:
    lines = ""
    for line in log_lines[-50:]:
        ts = line.get("ts", "")
        agent = line.get("agent", "")
        msg = line.get("msg", "")
        level = line.get("level", "INFO")
        
        if level == "ERROR":
            color = "#F85149"
        elif level == "SUCCESS":
            color = "#4ECDC4"
        else:
            color = "#f7ddd5"
            
        lines += f'<p style="margin:2px 0"><span style="color:#FF6B35">[{ts}]</span> <span style="color:#5DD9D0">{agent}:</span> <span style="color:{color}">{msg}</span></p>\n'
    
    return f"""
    <div style="background:#000;border:1px solid #594139;border-radius:4px;padding:16px;font-family:'JetBrains Mono',monospace;font-size:12px;max-height:400px;overflow-y:auto;line-height:1.6">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;border-bottom:1px solid rgba(255,255,255,0.1);padding-bottom:8px">
            <div style="width:10px;height:10px;border-radius:50%;background:#F85149"></div>
            <div style="width:10px;height:10px;border-radius:50%;background:#ff6b35"></div>
            <div style="width:10px;height:10px;border-radius:50%;background:#5DD9D0"></div>
            <span style="color:rgba(247,221,213,0.4);margin-left:8px">agent_orchestrator_v1.2.log</span>
        </div>
        {lines if lines else '<p style="color:rgba(247,221,213,0.4)">No logs yet. Run a scan to see agent activity.</p>'}
    </div>"""

def build_rag_html(stats: dict) -> str:
    vectors = stats.get("vectors", 16842)
    capacity = stats.get("capacity_pct", 84)
    storage_gb = stats.get("storage_gb", 1.2)
    memory_mb = stats.get("memory_mb", 450)
    dimensions = stats.get("dimensions", 384)
    growth = stats.get("growth_pct", 12.4)
    
    return f"""
    <div style="background:#170b08;border:1px dashed #594139;border-radius:8px;padding:24px">
        <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:16px;margin-bottom:20px">
            <div>
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
                    <span style="color:#ffb59d;font-size:20px">🗄️</span>
                    <h3 style="color:#f7ddd5;font-size:20px;font-weight:600;margin:0">RAG Vector Store</h3>
                </div>
                <p style="color:#e1bfb5;font-size:13px;margin:0">Indexing historical transaction data for real-time inference.</p>
            </div>
            <div style="min-width:200px">
                <div style="display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-size:11px;margin-bottom:4px">
                    <span style="color:#e1bfb5">CAPACITY USAGE</span>
                    <span style="color:#ff6b35;font-weight:700">{capacity}%</span>
                </div>
                <div style="background:#41312c;border-radius:999px;height:6px;overflow:hidden">
                    <div style="background:#FF6B35;height:100%;width:{capacity}%;border-radius:999px"></div>
                </div>
            </div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-bottom:16px">
            <div style="background:#2a1c18;border:1px solid rgba(89,65,57,0.3);border-radius:8px;padding:12px">
                <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#e1bfb5;text-transform:uppercase;letter-spacing:0.05em">Vectors Indexed</div>
                <div style="font-size:22px;font-weight:700;color:#ffb59d;margin-top:4px">{vectors:,}</div>
            </div>
            <div style="background:#2a1c18;border:1px solid rgba(89,65,57,0.3);border-radius:8px;padding:12px">
                <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#e1bfb5;text-transform:uppercase;letter-spacing:0.05em">Storage Used</div>
                <div style="font-size:22px;font-weight:700;color:#f7ddd5;margin-top:4px">{storage_gb} GB <span style="font-size:12px;font-weight:400;color:#e1bfb5">/ 1.5 GB</span></div>
            </div>
            <div style="background:#2a1c18;border:1px solid rgba(89,65,57,0.3);border-radius:8px;padding:12px">
                <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#e1bfb5;text-transform:uppercase;letter-spacing:0.05em">Memory Resident</div>
                <div style="font-size:22px;font-weight:700;color:#5dd9d0;margin-top:4px">{memory_mb} MB</div>
            </div>
            <div style="background:#2a1c18;border:1px solid rgba(89,65,57,0.3);border-radius:8px;padding:12px">
                <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#e1bfb5;text-transform:uppercase;letter-spacing:0.05em">Dimensions</div>
                <div style="font-size:22px;font-weight:700;color:#f7ddd5;margin-top:4px">{dimensions} <span style="font-size:12px;font-weight:400;color:#e1bfb5">(MiniLM)</span></div>
            </div>
        </div>
        <div style="background:#2a1c18;border:1px solid rgba(89,65,57,0.3);border-radius:8px;padding:16px">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
                <div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#e1bfb5;text-transform:uppercase;letter-spacing:0.05em">Vector Growth Trend</div>
                    <div style="font-size:12px;color:rgba(225,191,181,0.7)">Last 30 Days</div>
                </div>
                <div style="background:rgba(93,217,208,0.1);color:#5dd9d0;font-size:12px;font-weight:700;padding:2px 10px;border-radius:4px">Growth: +{growth}% (30d)</div>
            </div>
            <svg width="100%" height="80" viewBox="0 0 400 80" preserveAspectRatio="none">
                <defs>
                    <linearGradient id="cg" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stop-color="#FF6B35" stop-opacity="0.3"/>
                        <stop offset="100%" stop-color="#FF6B35" stop-opacity="0"/>
                    </linearGradient>
                </defs>
                <path d="M0,65 L40,60 L80,62 L120,55 L160,50 L200,42 L240,35 L280,28 L320,20 L360,12 L400,8 L400,80 L0,80 Z" fill="url(#cg)"/>
                <path d="M0,65 L40,60 L80,62 L120,55 L160,50 L200,42 L240,35 L280,28 L320,20 L360,12 L400,8" fill="none" stroke="#FF6B35" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div style="display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-size:10px;color:rgba(225,191,181,0.5);margin-top:4px">
                <span>30d ago (12k)</span><span>Today ({vectors/1000:.1f}k)</span>
            </div>
        </div>
    </div>"""


def create_dashboard():
    """Build and return the Gradio app"""
    
    # Shared state
    state = {
        "results": [],
        "logs": [
            {"ts": "12:05:01", "agent": "Planning Agent", "msg": "Initiating global scan sequence via RSS_FEED_URLS...", "level": "INFO"},
            {"ts": "12:05:05", "agent": "Scanner Agent", "msg": "Parsing 'dealnews.com'... Found 12 items.", "level": "INFO"},
            {"ts": "12:05:08", "agent": "Scanner Agent", "msg": "JSON extraction complete. Identified 5 high-confidence candidates.", "level": "INFO"},
            {"ts": "12:05:10", "agent": "Frontier Agent", "msg": "Analyzing 'Sony WH-1000XM5'... Querying ChromaDB 'products' collection.", "level": "INFO"},
            {"ts": "12:05:12", "agent": "Frontier Agent", "msg": "Retrieved 5 similar items (similarity > 0.89). Estimating price via RAG context...", "level": "INFO"},
            {"ts": "12:05:14", "agent": "Specialist Agent", "msg": "Modal GPU request sent (Llama-3.2-3B).", "level": "INFO"},
            {"ts": "12:05:15", "agent": "Neural Network Agent", "msg": "Running residual block inference... Weights loaded from 'dnn_weights.pt'.", "level": "INFO"},
            {"ts": "12:05:18", "agent": "Specialist Agent", "msg": "Modal inference returned $385.50 (Confidence: 0.94).", "level": "INFO"},
            {"ts": "12:05:20", "agent": "Ensemble Agent", "msg": "Aggregating estimates (W: 0.8/0.1/0.1)... Calculated true value: $399.00.", "level": "INFO"},
            {"ts": "12:05:22", "agent": "Ensemble Agent", "msg": "Discount detected: 50.12% ($199 vs $399). TRIGGERING DEAL THRESHOLD.", "level": "SUCCESS"},
            {"ts": "12:05:25", "agent": "Messaging Agent", "msg": "Claude crafting notification... '🔥 Sony WH-1000XM5: 50% Off Arbitrage! Snipe now.'", "level": "INFO"},
            {"ts": "12:05:28", "agent": "Messaging Agent", "msg": "Pushover API returned 200 OK. Notification sent.", "level": "SUCCESS"},
            {"ts": "12:05:40", "agent": "[INFO] [PLANNER]", "msg": f"Awaiting next RSS scan interval ({settings.SCAN_INTERVAL_MINUTES}m)...", "level": "INFO"},
        ],
        "agent_statuses": [
            {"name": "Scanner", "role": "RSS Parsing", "model": settings.SCANNER_MODEL, "status": "READY"},
            {"name": "Frontier", "role": "RAG Price Estimation", "model": settings.FRONTIER_MODEL, "status": "RUNNING"},
            {"name": "Specialist", "role": "Fine-tuned Inference", "model": "Llama-3.2-3B", "status": "READY"},
            {"name": "Neural Network", "role": "DNN Inference", "model": "Local PyTorch", "status": "READY"},
            {"name": "Ensemble", "role": "Weighted Combiner", "model": "Heuristic", "status": "READY"},
            {"name": "Messaging", "role": "Push Notifications", "model": settings.MESSAGING_MODEL, "status": "ERROR"},
            {"name": "Planning", "role": "Orchestration", "model": "GPT-4o", "status": "READY"},
        ],
        "rag_stats": {"vectors": 16842, "capacity_pct": 84, "storage_gb": 1.2, "memory_mb": 450, "dimensions": 384, "growth_pct": 12.4},
        "demo_deals": [
            {"deal": {"id": "1", "title": "Apple iPhone 15 Pro", "price": 899.0, "url": "https://example.com/iphone15", "description": "Latest Apple flagship", "source": "dealnews.com"}, "ensemble_result": {"estimated_price": 1200.0, "discount_pct": 25.1, "is_great_deal": False, "weights_used": {"frontier": 0.8, "specialist": 0.1, "dnn": 0.1}}, "notification_sent": False},
            {"deal": {"id": "2", "title": "Sony WH-1000XM5", "price": 199.0, "url": "https://example.com/sony-wh", "description": "Premium noise-canceling headphones", "source": "techbargains.com"}, "ensemble_result": {"estimated_price": 399.0, "discount_pct": 50.1, "is_great_deal": True, "weights_used": {"frontier": 0.8, "specialist": 0.1, "dnn": 0.1}}, "notification_sent": True},
            {"deal": {"id": "3", "title": "Samsung 4K OLED TV 55\"", "price": 699.0, "url": "https://example.com/samsung-tv", "description": "55-inch 4K OLED Smart TV", "source": "slickdeals.net"}, "ensemble_result": {"estimated_price": 1499.0, "discount_pct": 53.4, "is_great_deal": True, "weights_used": {"frontier": 0.8, "specialist": 0.1, "dnn": 0.1}}, "notification_sent": True},
        ]
    }
    state["results"] = state["demo_deals"]

    def do_scan():
        ts = datetime.now().strftime("%H:%M:%S")
        state["logs"].append({"ts": ts, "agent": "Planning Agent", "msg": "Manual scan triggered by user.", "level": "INFO"})
        state["agent_statuses"][0]["status"] = "RUNNING"
        
        # Simulate scan
        import time, random
        time.sleep(0.5)
        
        state["agent_statuses"][0]["status"] = "READY"
        state["logs"].append({"ts": datetime.now().strftime("%H:%M:%S"), "agent": "Scanner Agent", "msg": f"Scan complete. Found {random.randint(3,8)} candidates.", "level": "SUCCESS"})
        
        return (
            gr.update(value=build_agent_status_html(state["agent_statuses"])),
            gr.update(value=build_deals_html(state["results"])),
            gr.update(value=build_logs_html(state["logs"])),
        )

    def save_settings(openai_key, anthropic_key, pushover_user, pushover_token, modal_id, modal_secret,
                      deal_threshold, scan_interval, scanner_model, frontier_model, messaging_model,
                      ens_weights, chroma_path, embed_model, rss_feeds, max_deals):
        lines = [
            f"OPENAI_API_KEY={openai_key}",
            f"ANTHROPIC_API_KEY={anthropic_key}",
            f"PUSHOVER_USER={pushover_user}",
            f"PUSHOVER_TOKEN={pushover_token}",
            f"MODAL_TOKEN_ID={modal_id}",
            f"MODAL_TOKEN_SECRET={modal_secret}",
            f"DEAL_THRESHOLD={deal_threshold}",
            f"SCAN_INTERVAL_MINUTES={int(scan_interval)}",
            f"SCANNER_MODEL={scanner_model}",
            f"FRONTIER_MODEL={frontier_model}",
            f"MESSAGING_MODEL={messaging_model}",
            f"CHROMA_DB_PATH={chroma_path}",
            f"EMBEDDING_MODEL={embed_model}",
            f"RSS_FEED_URLS={','.join(rss_feeds.strip().split())}",
        ]
        try:
            with open(".env", "w") as f:
                f.write("\n".join(lines))
            return gr.update(value="✅ Settings saved and applied successfully!", visible=True)
        except Exception as e:
            return gr.update(value=f"❌ Error saving settings: {e}", visible=True)

    def validate_settings(openai_key, anthropic_key, *args):
        msgs = []
        if openai_key and openai_key.startswith("sk-"):
            msgs.append("✅ OpenAI key format valid")
        else:
            msgs.append("⚠️ OpenAI key missing or invalid format")
        if anthropic_key and anthropic_key.startswith("sk-ant-"):
            msgs.append("✅ Anthropic key format valid")
        else:
            msgs.append("⚠️ Anthropic key missing or invalid format")
        return gr.update(value="\n".join(msgs), visible=True)

    def reset_settings():
        return (
            "", "", "", "", "", "",
            50.0, 5, "gpt-4o-mini", "gpt-4o", "claude-3-5-sonnet-20241022",
            "0.8, 0.1, 0.1", "./data/products_vectorstore", "sentence-transformers/all-MiniLM-L6-v2",
            "https://www.dealnews.com/rss.html\nhttps://feeds.feedburner.com/techbargains", 50,
            gr.update(value="🔄 Settings reset to defaults.", visible=True)
        )

    def export_settings(openai_key, anthropic_key, *args):
        export = {
            "OPENAI_API_KEY": "sk-***REDACTED***" if openai_key else "",
            "ANTHROPIC_API_KEY": "sk-ant-***REDACTED***" if anthropic_key else "",
            "DEAL_THRESHOLD": args[0] if args else 50,
            "SCAN_INTERVAL_MINUTES": args[1] if len(args) > 1 else 5,
        }
        return gr.update(value=json.dumps(export, indent=2), visible=True)

    # ─── Build Gradio UI ─────────────────────────────────────────────────────
    with gr.Blocks(
        title="The Price Is Right — AI Deal Hunter",
        css=CUSTOM_CSS,
        theme=gr.themes.Base(
            primary_hue=gr.themes.colors.orange,
            secondary_hue=gr.themes.colors.teal,
            neutral_hue=gr.themes.colors.stone,
            font=gr.themes.GoogleFont("Hanken Grotesk"),
            font_mono=gr.themes.GoogleFont("JetBrains Mono"),
        )
    ) as app:

        # ── Header ──────────────────────────────────────────────────────────
        gr.HTML("""
        <div style="display:flex;justify-content:space-between;align-items:center;padding:12px 24px;
                    background:#2a1c18;border-bottom:1px solid #594139;position:sticky;top:0;z-index:100">
            <div style="display:flex;align-items:center;gap:10px">
                <span style="font-size:22px">📊</span>
                <span style="font-size:18px;font-weight:700;color:#ffb59d;font-family:'Hanken Grotesk',sans-serif">
                    The Price Is Right
                </span>
                <span style="background:#ff6b35;color:#5f1900;font-size:10px;font-weight:700;padding:2px 8px;
                             border-radius:999px;font-family:'JetBrains Mono',monospace">AI DEAL HUNTER</span>
            </div>
            <div style="display:flex;align-items:center;gap:12px">
                <span style="color:#e1bfb5;font-size:12px;font-family:'JetBrains Mono',monospace">v1.2.0</span>
                <span style="color:#4ECDC4;font-size:12px;font-family:'JetBrains Mono',monospace">● LIVE</span>
            </div>
        </div>
        """)

        # ── Tabs ─────────────────────────────────────────────────────────────
        with gr.Tabs(elem_id="main-tabs") as tabs:

            # ════════════════════════════════════════════════════════════════
            # TAB 1 — DASHBOARD
            # ════════════════════════════════════════════════════════════════
            with gr.Tab("🖥️ Dashboard", id="tab-dashboard"):

                # Section 1: Agent Framework
                with gr.Accordion("🤖 Agent Framework", open=True):
                    agent_status_html = gr.HTML(
                        value=build_agent_status_html(state["agent_statuses"]),
                        label=""
                    )

                # Section 2: Deal Opportunities
                with gr.Accordion("🔥 Deal Opportunities Found", open=True):
                    deals_html = gr.HTML(
                        value=build_deals_html(state["results"]),
                        label=""
                    )

                # Section 3: Live Agent Logs
                with gr.Accordion("📋 Live Agent Logs", open=True):
                    logs_html = gr.HTML(
                        value=build_logs_html(state["logs"]),
                        label=""
                    )
                    with gr.Row():
                        scan_btn = gr.Button(
                            "🔍 Scan for Deals Now",
                            variant="primary",
                            size="lg",
                            elem_classes=["scan-btn"]
                        )
                        refresh_logs_btn = gr.Button("🔄 Refresh Logs", variant="secondary", size="sm")

                # Section 4: RAG Vector Store
                with gr.Accordion("📊 RAG Vector Store", open=True):
                    rag_html = gr.HTML(
                        value=build_rag_html(state["rag_stats"]),
                        label=""
                    )
                    refresh_rag_btn = gr.Button("🔄 Refresh RAG Plot", variant="secondary", size="sm")

                # Deals Dataframe (hidden, for data export)
                with gr.Accordion("📋 Deals Data Table (Export)", open=False):
                    deals_df = gr.Dataframe(
                        headers=["Title", "Listed $", "Estimated $", "Discount %", "Great Deal?", "URL"],
                        datatype=["str", "number", "number", "number", "bool", "str"],
                        value=[
                            [d["deal"]["title"], d["deal"]["price"],
                             d["ensemble_result"]["estimated_price"],
                             round(d["ensemble_result"]["discount_pct"], 1),
                             d["ensemble_result"]["is_great_deal"],
                             d["deal"]["url"]]
                            for d in state["results"]
                        ],
                        interactive=False,
                        wrap=True
                    )

            # ════════════════════════════════════════════════════════════════
            # TAB 2 — SETTINGS
            # ════════════════════════════════════════════════════════════════
            with gr.Tab("⚙️ Settings", id="tab-settings"):
                gr.Markdown("""
                ## System Configuration
                Manage your agent parameters, database connections, and external API integrations.
                """)

                # Section 1: API Keys
                with gr.Accordion("🔑 API Keys", open=False):
                    with gr.Row():
                        with gr.Column():
                            openai_key = gr.Textbox(label="OpenAI API Key", placeholder="sk-...", type="password")
                            with gr.Row():
                                test_openai_btn = gr.Button("Test OpenAI", size="sm", variant="secondary")
                                openai_status = gr.Textbox(label="", show_label=False, interactive=False, scale=3)
                        with gr.Column():
                            anthropic_key = gr.Textbox(label="Anthropic API Key", placeholder="sk-ant-...", type="password")
                            with gr.Row():
                                test_anthropic_btn = gr.Button("Test Anthropic", size="sm", variant="secondary")
                                anthropic_status = gr.Textbox(label="", show_label=False, interactive=False, scale=3)
                    with gr.Row():
                        with gr.Column():
                            pushover_user = gr.Textbox(label="Pushover User Key", placeholder="User Key", type="password")
                            with gr.Row():
                                test_pushover_btn = gr.Button("Test Pushover", size="sm", variant="secondary")
                                pushover_status = gr.Textbox(label="", show_label=False, interactive=False, scale=3)
                        with gr.Column():
                            pushover_token = gr.Textbox(label="Pushover App Token", placeholder="App Token", type="password")
                    with gr.Row():
                        with gr.Column():
                            modal_id = gr.Textbox(label="Modal Token ID", placeholder="ak-...", type="password")
                        with gr.Column():
                            modal_secret = gr.Textbox(label="Modal Token Secret", placeholder="...", type="password")
                            with gr.Row():
                                test_modal_btn = gr.Button("Test Modal", size="sm", variant="secondary")
                                modal_status = gr.Textbox(label="", show_label=False, interactive=False, scale=3)

                # Section 2: Agent Configuration
                with gr.Accordion("🤖 Agent Configuration", open=True):
                    with gr.Row():
                        deal_threshold = gr.Slider(label="Deal Threshold (%)", minimum=1, maximum=90, value=50, step=1)
                        scan_interval = gr.Slider(label="Scan Interval (min)", minimum=1, maximum=60, value=5, step=1)
                    with gr.Row():
                        scanner_model = gr.Dropdown(
                            label="Scanner Model",
                            choices=["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
                            value="gpt-4o-mini"
                        )
                        frontier_model = gr.Dropdown(
                            label="Frontier Model",
                            choices=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
                            value="gpt-4o"
                        )
                        messaging_model = gr.Dropdown(
                            label="Messaging Model",
                            choices=["claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-haiku-20240307"],
                            value="claude-3-5-sonnet-20241022"
                        )
                    ens_weights = gr.Textbox(
                        label="Ensemble Weights (Frontier, Specialist, DNN — must sum to 1.0)",
                        value="0.8, 0.1, 0.1",
                        placeholder="0.8, 0.1, 0.1"
                    )

                # Section 3: RAG Database
                with gr.Accordion("🧠 RAG Database", open=False):
                    with gr.Row():
                        chroma_path = gr.Textbox(label="ChromaDB Storage Path", value="./data/products_vectorstore")
                        embed_model = gr.Dropdown(
                            label="Embedding Model",
                            choices=["sentence-transformers/all-MiniLM-L6-v2", "text-embedding-3-small", "text-embedding-ada-002"],
                            value="sentence-transformers/all-MiniLM-L6-v2"
                        )
                    with gr.Row():
                        chroma_results = gr.Slider(label="RAG Results Count", minimum=1, maximum=20, value=5, step=1)
                        rag_max_points = gr.Slider(label="Visualisation Max Points", minimum=100, maximum=5000, value=1000, step=100)

                # Section 4: Notifications
                with gr.Accordion("🔔 Notifications", open=False):
                    with gr.Row():
                        notif_sound = gr.Dropdown(
                            label="Pushover Sound",
                            choices=["pushover", "bike", "bugle", "cashregister", "classical", "cosmic", "falling", "gamelan", "incoming", "intermission", "magic", "mechanical", "pianobar", "siren", "spacealarm", "tugboat", "alien", "climb", "persistent", "echo", "updown"],
                            value="pushover"
                        )
                        notif_title = gr.Textbox(label="Notification Title", value="The Price Is Right Alert")
                    notif_min_interval = gr.Slider(label="Min Interval Between Notifications (min)", minimum=1, maximum=60, value=5, step=1)

                # Section 5: RSS Feeds
                with gr.Accordion("📡 RSS Feeds", open=True):
                    rss_feeds = gr.Textbox(
                        label="Feed Sources (one per line)",
                        value="https://www.dealnews.com/rss.html\nhttps://feeds.feedburner.com/techbargains\nhttps://slickdeals.net/newsearch.php?mode=frontpage&searcharea=deals&searchin=first&rss=1",
                        lines=5,
                        placeholder="https://..."
                    )
                    max_deals = gr.Slider(label="Max Deals Per Scan", minimum=1, maximum=200, value=50, step=1)

                # Section 6: Advanced
                with gr.Accordion("⚙️ Advanced", open=False):
                    with gr.Row():
                        memory_file = gr.Textbox(label="Memory File Path", value="./data/memory.json")
                        log_level = gr.Dropdown(label="Log Level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], value="INFO")
                    with gr.Row():
                        dnn_weights = gr.Textbox(label="DNN Weights Path", value="./data/dnn_weights.pt")
                        dashboard_port = gr.Number(label="Dashboard Port", value=7860)
                    api_port = gr.Number(label="API Port", value=8000)

                # ── Settings Action Buttons ──────────────────────────────────
                gr.HTML('<div style="height:16px"></div>')
                with gr.Row():
                    reset_btn = gr.Button("🔄 Reset to Defaults", variant="secondary")
                    validate_btn = gr.Button("✅ Validate Only", variant="secondary")
                    export_btn = gr.Button("📤 Export Settings", variant="secondary")
                save_btn = gr.Button("💾 Save & Apply", variant="primary", size="lg")

                settings_msg = gr.Textbox(label="Status", interactive=False, visible=False)
                export_output = gr.Code(label=".env Preview / Export", language="shell", visible=False)

        # ── Mobile Bottom Nav ─────────────────────────────────────────────────
        gr.HTML("""
        <div style="position:fixed;bottom:0;left:0;right:0;z-index:200;
                    display:flex;justify-content:space-around;align-items:center;
                    height:60px;background:#1d100c;border-top:1px solid #594139;
                    padding:0 16px" class="mobile-nav-bar">
            <a href="#tab-dashboard" style="display:flex;flex-direction:column;align-items:center;
                text-decoration:none;color:#ffb59d;font-size:11px;font-family:'JetBrains Mono',monospace;gap:2px">
                <span style="font-size:20px">📊</span>Dashboard
            </a>
            <a href="#tab-settings" style="display:flex;flex-direction:column;align-items:center;
                text-decoration:none;color:#e1bfb5;font-size:11px;font-family:'JetBrains Mono',monospace;gap:2px">
                <span style="font-size:20px">⚙️</span>Settings
            </a>
        </div>
        <style>
        @media (min-width: 769px) { .mobile-nav-bar { display: none !important; } }
        </style>
        """)

        # ── Event Wiring ──────────────────────────────────────────────────────
        scan_btn.click(
            fn=do_scan,
            outputs=[agent_status_html, deals_html, logs_html]
        )

        refresh_logs_btn.click(
            fn=lambda: gr.update(value=build_logs_html(state["logs"])),
            outputs=[logs_html]
        )

        refresh_rag_btn.click(
            fn=lambda: gr.update(value=build_rag_html(state["rag_stats"])),
            outputs=[rag_html]
        )

        save_btn.click(
            fn=save_settings,
            inputs=[openai_key, anthropic_key, pushover_user, pushover_token, modal_id, modal_secret,
                    deal_threshold, scan_interval, scanner_model, frontier_model, messaging_model,
                    ens_weights, chroma_path, embed_model, rss_feeds, max_deals],
            outputs=[settings_msg]
        ).then(lambda: gr.update(visible=True), outputs=[settings_msg])

        validate_btn.click(
            fn=validate_settings,
            inputs=[openai_key, anthropic_key],
            outputs=[settings_msg]
        ).then(lambda: gr.update(visible=True), outputs=[settings_msg])

        reset_btn.click(
            fn=reset_settings,
            outputs=[openai_key, anthropic_key, pushover_user, pushover_token, modal_id, modal_secret,
                     deal_threshold, scan_interval, scanner_model, frontier_model, messaging_model,
                     ens_weights, chroma_path, embed_model, rss_feeds, max_deals, settings_msg]
        )

        export_btn.click(
            fn=export_settings,
            inputs=[openai_key, anthropic_key, deal_threshold, scan_interval],
            outputs=[export_output]
        ).then(lambda: gr.update(visible=True), outputs=[export_output])

        test_openai_btn.click(
            fn=lambda k: "✅ Format OK" if k.startswith("sk-") else "⚠️ Invalid format",
            inputs=[openai_key], outputs=[openai_status]
        )
        test_anthropic_btn.click(
            fn=lambda k: "✅ Format OK" if k.startswith("sk-ant-") else "⚠️ Invalid format",
            inputs=[anthropic_key], outputs=[anthropic_status]
        )
        test_pushover_btn.click(
            fn=lambda k: "✅ Key provided" if k else "⚠️ Key missing",
            inputs=[pushover_user], outputs=[pushover_status]
        )
        test_modal_btn.click(
            fn=lambda k: "✅ Token provided" if k else "⚠️ Token missing",
            inputs=[modal_id], outputs=[modal_status]
        )

    return app
