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

    /* ── Override every Gradio theme token that controls text color ── */
    --body-text-color: #f7ddd5 !important;
    --body-text-color-subdued: #e1bfb5 !important;
    --color-text-body: #f7ddd5 !important;
    --color-text-label: #e1bfb5 !important;
    --color-text-secondary: #e1bfb5 !important;
    --input-text-color: #f7ddd5 !important;
    --input-placeholder-color: #7a5a50 !important;
    --input-background-fill: #1a0a00 !important;
    --input-background-fill-focus: #261814 !important;
    --input-background-fill-hover: #1d100c !important;
    --input-border-color: #594139 !important;
    --input-border-color-focus: #ffb59d !important;
    --input-shadow: none !important;
    --input-shadow-focus: 0 0 0 2px rgba(255,181,157,0.25) !important;
    --block-background-fill: #2a1c18 !important;
    --block-border-color: #594139 !important;
    --block-label-text-color: #e1bfb5 !important;
    --block-title-text-color: #f7ddd5 !important;
    --panel-background-fill: #261814 !important;
    --panel-border-color: #594139 !important;
    --checkbox-background-color: #1a0a00 !important;
    --checkbox-border-color: #594139 !important;
    --checkbox-label-text-color: #f7ddd5 !important;
    --slider-color: #ffb59d !important;
    --table-text-color: #f7ddd5 !important;
    --table-row-focus: rgba(255,181,157,0.08) !important;
    --button-secondary-text-color: #f7ddd5 !important;
    --button-secondary-background-fill: #2a1c18 !important;
    --button-secondary-border-color: #594139 !important;
    --button-primary-text-color: #5d1900 !important;
    --button-primary-background-fill: #ffb59d !important;
    --accordion-text-color: #f7ddd5 !important;
    --stat-background-fill: #2a1c18 !important;
    --color-accent: #ffb59d !important;
    --color-accent-soft: rgba(255,181,157,0.15) !important;
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

/* ═══════════════════════════════════════════════════════════════════════════
   NUCLEAR TEXT VISIBILITY FIX v2
   Targets every possible Gradio 4.x / Svelte-scoped element
   Uses universal selectors so no hashed class name can escape
   ═══════════════════════════════════════════════════════════════════════════ */

/* ── 1. Universal input / textarea / select ─────────────────────────────── */
input, textarea, select {
    color: #f7ddd5 !important;
    -webkit-text-fill-color: #f7ddd5 !important;
    background-color: #1a0a00 !important;
    caret-color: #ffb59d !important;
}

/* ── 2. Placeholder text ────────────────────────────────────────────────── */
input::placeholder, textarea::placeholder {
    color: #7a5a50 !important;
    -webkit-text-fill-color: #7a5a50 !important;
    opacity: 1 !important;
}

/* ── 3. Disabled / read-only (status output boxes) ─────────────────────── */
input:disabled, textarea:disabled,
input[disabled], textarea[disabled],
input[readonly], textarea[readonly] {
    color: #ffb59d !important;
    -webkit-text-fill-color: #ffb59d !important;
    background-color: #1a0a00 !important;
    opacity: 1 !important;
}

/* ── 4. Slider number value pill ────────────────────────────────────────── */
.gradio-slider input[type="number"],
.gradio-slider input,
[data-testid="slider"] input,
.wrap > input[type="number"],
fieldset input[type="number"] {
    color: #f7ddd5 !important;
    -webkit-text-fill-color: #f7ddd5 !important;
    background-color: #2a1c18 !important;
    border: 1px solid #594139 !important;
    border-radius: 4px !important;
}

/* ── 5. Dropdown: selected value text ───────────────────────────────────── */
.gradio-dropdown input,
.gradio-dropdown span,
[data-testid="dropdown"] input,
[data-testid="dropdown"] span,
.multiselect span,
.token span,
.wrap span {
    color: #f7ddd5 !important;
    -webkit-text-fill-color: #f7ddd5 !important;
}

/* ── 6. Dropdown list popup ─────────────────────────────────────────────── */
.dropdown-arrow,
ul.options, ul.options li,
.item, .item span,
.list-items, .list-items li {
    color: #f7ddd5 !important;
    background-color: #2a1c18 !important;
}
ul.options li:hover, .item:hover {
    background-color: #41312c !important;
    color: #ffb59d !important;
}

/* ── 7. Page headings and markdown prose ────────────────────────────────── */
.gradio-container h1,
.gradio-container h2,
.gradio-container h3,
.gradio-container h4,
.gradio-container p,
.prose h1, .prose h2, .prose h3,
.prose p, .prose li,
.md h1, .md h2, .md h3,
.md p, .md li {
    color: #f7ddd5 !important;
}

/* ── 8. All span/div text inside form blocks ────────────────────────────── */
.block span:not(.badge-ready):not(.badge-running):not(.badge-error):not(.heartbeat-ready):not(.heartbeat-running):not(.heartbeat-error),
.block p,
.block div:not(.terminal-panel):not(.deal-card) {
    color: #f7ddd5 !important;
}

/* ── 9. Label text above every input ────────────────────────────────────── */
label, .block label, fieldset label,
.label-wrap, .label-wrap span,
.gr-block label, .gr-form label {
    color: #e1bfb5 !important;
    -webkit-text-fill-color: #e1bfb5 !important;
}

/* ── 10. Accordion / details summary text ───────────────────────────────── */
details summary, details summary span,
.gr-accordion summary, .gr-accordion summary span,
[data-testid="accordion"] summary {
    color: #f7ddd5 !important;
}

/* ── 11. Gradio v4 Svelte-scoped wrappers (catch-all) ───────────────────── */
[class*="svelte-"] input,
[class*="svelte-"] textarea,
[class*="svelte-"] select,
[class*="svelte-"] span:not(.badge-ready):not(.badge-running):not(.badge-error) {
    color: #f7ddd5 !important;
    -webkit-text-fill-color: #f7ddd5 !important;
}

/* ── 12. Code / export preview block ────────────────────────────────────── */
.cm-editor, .cm-content, .cm-line,
.codemirror-wrapper, .code-wrap {
    color: #f7ddd5 !important;
    background-color: #1a0a00 !important;
}

/* ── 13. Dataframe cells ────────────────────────────────────────────────── */
table td, table th,
.gr-dataframe td, .gr-dataframe th {
    color: #f7ddd5 !important;
    background-color: #1d100c !important;
}
.gr-dataframe th {
    color: #e1bfb5 !important;
    background-color: #261814 !important;
}

/* ── 14. Buttons secondary text ─────────────────────────────────────────── */
.gr-button-secondary, button.secondary {
    color: #f7ddd5 !important;
    border-color: #594139 !important;
}

/* ── 15. Scrollbar ──────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #1d100c; }
::-webkit-scrollbar-thumb { background: #41312c; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #594139; }

/* ═══════════════════════════════════════════════════════════════════════════
   PIR COMPONENT CLASS OVERRIDES — elem_classes targeting
   Gradio 4.x wraps each component in a div with the elem_class name.
   We target the inner input/textarea/select/span through that wrapper.
   ═══════════════════════════════════════════════════════════════════════════ */

/* pir-input: all text/password/textarea inputs */
div.pir-input input,
div.pir-input textarea,
div.pir-input input[type="text"],
div.pir-input input[type="password"],
div.pir-input input[type="email"] {
    color: #f7ddd5 !important;
    -webkit-text-fill-color: #f7ddd5 !important;
    background-color: #1a0a00 !important;
    border-color: #594139 !important;
    caret-color: #ffb59d !important;
    opacity: 1 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
}
div.pir-input input::placeholder,
div.pir-input textarea::placeholder {
    color: #7a5a50 !important;
    -webkit-text-fill-color: #7a5a50 !important;
    opacity: 1 !important;
}
div.pir-input label,
div.pir-input .label-wrap span {
    color: #e1bfb5 !important;
    -webkit-text-fill-color: #e1bfb5 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

/* pir-status: read-only output textboxes (Test result boxes) */
div.pir-status input,
div.pir-status textarea,
div.pir-status input:disabled,
div.pir-status textarea:disabled,
div.pir-status input[readonly],
div.pir-status textarea[readonly] {
    color: #ffb59d !important;
    -webkit-text-fill-color: #ffb59d !important;
    background-color: #1a0a00 !important;
    border-color: #594139 !important;
    opacity: 1 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
}

/* pir-dropdown: dropdown selected value and list */
div.pir-dropdown input,
div.pir-dropdown span.single-value,
div.pir-dropdown .wrap > span,
div.pir-dropdown .wrap input,
div.pir-dropdown [data-testid="dropdown"] input,
div.pir-dropdown select {
    color: #f7ddd5 !important;
    -webkit-text-fill-color: #f7ddd5 !important;
    background-color: #1a0a00 !important;
    border-color: #594139 !important;
    opacity: 1 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
}
div.pir-dropdown label,
div.pir-dropdown .label-wrap span {
    color: #e1bfb5 !important;
    -webkit-text-fill-color: #e1bfb5 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}
/* Dropdown popup list items */
div.pir-dropdown ul li,
div.pir-dropdown .item,
div.pir-dropdown .list-items li {
    color: #f7ddd5 !important;
    background-color: #2a1c18 !important;
}
div.pir-dropdown ul li:hover,
div.pir-dropdown .item:hover {
    background-color: #41312c !important;
    color: #ffb59d !important;
}

/* pir-slider: slider value number pill */
div.pir-slider input[type="number"],
div.pir-slider .wrap > input,
div.pir-slider input:not([type="range"]) {
    color: #f7ddd5 !important;
    -webkit-text-fill-color: #f7ddd5 !important;
    background-color: #2a1c18 !important;
    border: 1px solid #594139 !important;
    border-radius: 4px !important;
    opacity: 1 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
}
div.pir-slider label,
div.pir-slider .label-wrap span {
    color: #e1bfb5 !important;
    -webkit-text-fill-color: #e1bfb5 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

/* pir-number: number input fields */
div.pir-number input,
div.pir-number input[type="number"] {
    color: #f7ddd5 !important;
    -webkit-text-fill-color: #f7ddd5 !important;
    background-color: #1a0a00 !important;
    border-color: #594139 !important;
    opacity: 1 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
}
div.pir-number label,
div.pir-number .label-wrap span {
    color: #e1bfb5 !important;
    -webkit-text-fill-color: #e1bfb5 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}
"""

# JavaScript injected into the page — injects a <style> tag that cannot be overridden
_JS_FIX = """
(function() {
    // Inject a high-priority <style> tag into <head> — runs before Svelte hydration
    const style = document.createElement('style');
    style.id = 'price-is-right-fix';
    style.innerHTML = `
        /* === PRICE IS RIGHT — FORCED VISIBILITY FIX === */
        :root {
            --body-text-color: #f7ddd5 !important;
            --input-text-color: #f7ddd5 !important;
            --input-background-fill: #1a0a00 !important;
            --block-label-text-color: #e1bfb5 !important;
            --block-title-text-color: #f7ddd5 !important;
        }
        /* Universal element overrides with max specificity */
        html body .gradio-container input,
        html body .gradio-container textarea,
        html body .gradio-container select {
            color: #f7ddd5 !important;
            -webkit-text-fill-color: #f7ddd5 !important;
            background-color: #1a0a00 !important;
            caret-color: #ffb59d !important;
            opacity: 1 !important;
        }
        html body .gradio-container input::placeholder,
        html body .gradio-container textarea::placeholder {
            color: #7a5a50 !important;
            -webkit-text-fill-color: #7a5a50 !important;
            opacity: 1 !important;
        }
        html body .gradio-container input:disabled,
        html body .gradio-container textarea:disabled,
        html body .gradio-container input[disabled],
        html body .gradio-container textarea[disabled],
        html body .gradio-container input[readonly],
        html body .gradio-container textarea[readonly] {
            color: #ffb59d !important;
            -webkit-text-fill-color: #ffb59d !important;
            background-color: #1a0a00 !important;
            opacity: 1 !important;
        }
        html body .gradio-container label,
        html body .gradio-container .label-wrap,
        html body .gradio-container .label-wrap span,
        html body .gradio-container fieldset > label {
            color: #e1bfb5 !important;
            -webkit-text-fill-color: #e1bfb5 !important;
        }
        html body .gradio-container span,
        html body .gradio-container p,
        html body .gradio-container h1,
        html body .gradio-container h2,
        html body .gradio-container h3,
        html body .gradio-container h4 {
            color: #f7ddd5 !important;
        }
        html body .gradio-container details summary,
        html body .gradio-container details summary span {
            color: #f7ddd5 !important;
        }
    `;
    // Insert at end of head so it wins over everything
    if (document.head) {
        document.head.appendChild(style);
    } else {
        document.addEventListener('DOMContentLoaded', () => document.head.appendChild(style));
    }

    // Also apply inline styles after DOM is ready (belt-and-suspenders)
    function applyInlineStyles() {
        const BRIGHT = '#f7ddd5';
        const DIM    = '#e1bfb5';
        const BG     = '#1a0a00';
        const BG2    = '#2a1c18';
        const WARN   = '#ffb59d';

        // --- Target pir-* wrapper divs specifically ---
        // pir-input and pir-number: text/password/number inputs
        document.querySelectorAll('div.pir-input input, div.pir-input textarea, div.pir-number input').forEach(el => {
            el.style.setProperty('color', BRIGHT, 'important');
            el.style.setProperty('-webkit-text-fill-color', BRIGHT, 'important');
            el.style.setProperty('background-color', BG, 'important');
            el.style.setProperty('opacity', '1', 'important');
            el.style.setProperty('caret-color', WARN, 'important');
        });
        // pir-status: read-only output boxes
        document.querySelectorAll('div.pir-status input, div.pir-status textarea').forEach(el => {
            el.style.setProperty('color', WARN, 'important');
            el.style.setProperty('-webkit-text-fill-color', WARN, 'important');
            el.style.setProperty('background-color', BG, 'important');
            el.style.setProperty('opacity', '1', 'important');
        });
        // pir-dropdown: selected value text
        document.querySelectorAll('div.pir-dropdown input, div.pir-dropdown span').forEach(el => {
            el.style.setProperty('color', BRIGHT, 'important');
            el.style.setProperty('-webkit-text-fill-color', BRIGHT, 'important');
            el.style.setProperty('background-color', BG, 'important');
            el.style.setProperty('opacity', '1', 'important');
        });
        // pir-slider: number pill
        document.querySelectorAll('div.pir-slider input[type="number"], div.pir-slider input:not([type="range"])').forEach(el => {
            el.style.setProperty('color', BRIGHT, 'important');
            el.style.setProperty('-webkit-text-fill-color', BRIGHT, 'important');
            el.style.setProperty('background-color', BG2, 'important');
            el.style.setProperty('opacity', '1', 'important');
        });
        // All labels inside pir-* wrappers
        document.querySelectorAll('div.pir-input label, div.pir-status label, div.pir-dropdown label, div.pir-slider label, div.pir-number label, div.pir-input .label-wrap span, div.pir-dropdown .label-wrap span, div.pir-slider .label-wrap span, div.pir-number .label-wrap span').forEach(el => {
            el.style.setProperty('color', DIM, 'important');
            el.style.setProperty('-webkit-text-fill-color', DIM, 'important');
        });

        // --- Fallback: all inputs everywhere ---
        document.querySelectorAll('input, textarea, select').forEach(el => {
            if (!el.style.color || el.style.color === '') {
                el.style.setProperty('color', BRIGHT, 'important');
                el.style.setProperty('-webkit-text-fill-color', BRIGHT, 'important');
                el.style.setProperty('background-color', BG, 'important');
                el.style.setProperty('opacity', '1', 'important');
            }
            if (el.disabled || el.readOnly || el.getAttribute('disabled') !== null) {
                el.style.setProperty('color', WARN, 'important');
                el.style.setProperty('-webkit-text-fill-color', WARN, 'important');
            }
        });
        document.querySelectorAll('label, .label-wrap, .label-wrap span').forEach(el => {
            el.style.setProperty('color', DIM, 'important');
            el.style.setProperty('-webkit-text-fill-color', DIM, 'important');
        });
        const skipClasses = new Set(['badge-ready','badge-running','badge-error',
                                      'heartbeat-ready','heartbeat-running','heartbeat-error']);
        document.querySelectorAll('span, p, h1, h2, h3, h4, details summary').forEach(el => {
            if (![...el.classList].some(c => skipClasses.has(c))) {
                el.style.setProperty('color', BRIGHT, 'important');
            }
        });
    }

    // Run at multiple intervals to catch Svelte hydration at any timing
    [200, 600, 1200, 2500, 5000].forEach(t => setTimeout(applyInlineStyles, t));

    // Watch for any DOM mutations and re-apply
    const observer = new MutationObserver(mutations => {
        let hasInputs = mutations.some(m =>
            [...m.addedNodes].some(n => n.nodeType === 1 &&
                (n.matches('input,textarea,select,label') ||
                 n.querySelector('input,textarea,select,label')))
        );
        if (hasInputs) applyInlineStyles();
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
})();
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
            {"name": "Messaging", "role": "Push Notifications", "model": settings.MESSAGING_MODEL, "status": "READY"},
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

    # ── Persistence helpers ──────────────────────────────────────────────────
    from app.core.settings_store import SettingsStore
    
    if os.path.exists("/app/data"):
        EXPORT_JSON_PATH   = "/app/data/settings_export.json"
        ENV_PATH           = "/app/.env"
    else:
        EXPORT_JSON_PATH   = os.path.join(os.path.dirname(__file__), "..", "..", "data", "settings_export.json")
        EXPORT_JSON_PATH   = os.path.normpath(EXPORT_JSON_PATH)
        ENV_PATH           = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
        ENV_PATH           = os.path.normpath(ENV_PATH)

    DEFAULTS = {
        "OPENAI_API_KEY": "",
        "ANTHROPIC_API_KEY": "",
        "PUSHOVER_USER": "",
        "PUSHOVER_TOKEN": "",
        "MODAL_TOKEN_ID": "",
        "MODAL_TOKEN_SECRET": "",
        "DEAL_THRESHOLD": 50.0,
        "SCAN_INTERVAL_MINUTES": 5,
        "SCANNER_MODEL": "gpt-4o-mini",
        "FRONTIER_MODEL": "gpt-4o",
        "MESSAGING_MODEL": "claude-3-5-sonnet-20241022",
        "ENSEMBLE_WEIGHTS": "0.8, 0.1, 0.1",
        "CHROMA_DB_PATH": "./data/products_vectorstore",
        "EMBEDDING_MODEL": "sentence-transformers/all-MiniLM-L6-v2",
        "CHROMA_RESULTS": 5,
        "RAG_MAX_POINTS": 1000,
        "PUSHOVER_SOUND": "pushover",
        "NOTIFICATION_TITLE": "The Price Is Right Alert",
        "NOTIF_MIN_INTERVAL": 5,
        "RSS_FEEDS": "https://www.dealnews.com/rss.html\nhttps://feeds.feedburner.com/techbargains\nhttps://slickdeals.net/newsearch.php?mode=frontpage&searcharea=deals&searchin=first&rss=1",
        "MAX_DEALS_PER_SCAN": 50,
        "MEMORY_FILE": "./data/memory.json",
        "LOG_LEVEL": "INFO",
        "DNN_WEIGHTS_PATH": "./data/dnn_weights.pt",
        "DASHBOARD_PORT": 7860,
        "API_PORT": 8000,
    }

    def _load_persisted():
        """Load saved settings from ui_settings.json, falling back to DEFAULTS."""
        saved = SettingsStore.read()
        return {**DEFAULTS, **saved}

    def _write_env(d: dict):
        """Write all settings to .env file."""
        rss_oneline = ",".join(line.strip() for line in d.get("RSS_FEEDS", "").splitlines() if line.strip())
        lines = [
            f"OPENAI_API_KEY={d.get('OPENAI_API_KEY', '')}",
            f"ANTHROPIC_API_KEY={d.get('ANTHROPIC_API_KEY', '')}",
            f"PUSHOVER_USER={d.get('PUSHOVER_USER', '')}",
            f"PUSHOVER_TOKEN={d.get('PUSHOVER_TOKEN', '')}",
            f"MODAL_TOKEN_ID={d.get('MODAL_TOKEN_ID', '')}",
            f"MODAL_TOKEN_SECRET={d.get('MODAL_TOKEN_SECRET', '')}",
            f"DEAL_THRESHOLD={d.get('DEAL_THRESHOLD', 50)}",
            f"SCAN_INTERVAL_MINUTES={int(d.get('SCAN_INTERVAL_MINUTES', 5))}",
            f"SCANNER_MODEL={d.get('SCANNER_MODEL', 'gpt-4o-mini')}",
            f"FRONTIER_MODEL={d.get('FRONTIER_MODEL', 'gpt-4o')}",
            f"MESSAGING_MODEL={d.get('MESSAGING_MODEL', 'claude-3-5-sonnet-20241022')}",
            f"ENSEMBLE_WEIGHTS={d.get('ENSEMBLE_WEIGHTS', '0.8, 0.1, 0.1')}",
            f"CHROMA_DB_PATH={d.get('CHROMA_DB_PATH', './data/products_vectorstore')}",
            f"EMBEDDING_MODEL={d.get('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')}",
            f"RSS_FEED_URLS={rss_oneline}",
            f"MAX_DEALS_PER_SCAN={int(d.get('MAX_DEALS_PER_SCAN', 50))}",
            f"PUSHOVER_SOUND={d.get('PUSHOVER_SOUND', 'pushover')}",
            f"NOTIFICATION_TITLE={d.get('NOTIFICATION_TITLE', 'The Price Is Right Alert')}",
            f"NOTIF_MIN_INTERVAL={int(d.get('NOTIF_MIN_INTERVAL', 5))}",
            f"MEMORY_FILE={d.get('MEMORY_FILE', './data/memory.json')}",
            f"LOG_LEVEL={d.get('LOG_LEVEL', 'INFO')}",
            f"DNN_WEIGHTS_PATH={d.get('DNN_WEIGHTS_PATH', './data/dnn_weights.pt')}",
            f"DASHBOARD_PORT={int(d.get('DASHBOARD_PORT', 7860))}",
            f"API_PORT={int(d.get('API_PORT', 8000))}",
        ]
        with open(ENV_PATH, "w") as f:
            f.write("\n".join(lines) + "\n")

    def save_settings(openai_key, anthropic_key, pushover_user, pushover_token, modal_id, modal_secret,
                      deal_threshold, scan_interval, scanner_model, frontier_model, messaging_model,
                      ens_weights, chroma_path, embed_model, chroma_results, rag_max_points,
                      notif_sound, notif_title, notif_min_interval,
                      rss_feeds, max_deals, memory_file, log_level, dnn_weights, dashboard_port, api_port):
        d = {
            "OPENAI_API_KEY": openai_key or "",
            "ANTHROPIC_API_KEY": anthropic_key or "",
            "PUSHOVER_USER": pushover_user or "",
            "PUSHOVER_TOKEN": pushover_token or "",
            "MODAL_TOKEN_ID": modal_id or "",
            "MODAL_TOKEN_SECRET": modal_secret or "",
            "DEAL_THRESHOLD": float(deal_threshold),
            "SCAN_INTERVAL_MINUTES": int(scan_interval),
            "SCANNER_MODEL": scanner_model,
            "FRONTIER_MODEL": frontier_model,
            "MESSAGING_MODEL": messaging_model,
            "ENSEMBLE_WEIGHTS": ens_weights,
            "CHROMA_DB_PATH": chroma_path,
            "EMBEDDING_MODEL": embed_model,
            "CHROMA_RESULTS": int(chroma_results),
            "RAG_MAX_POINTS": int(rag_max_points),
            "PUSHOVER_SOUND": notif_sound,
            "NOTIFICATION_TITLE": notif_title,
            "NOTIF_MIN_INTERVAL": int(notif_min_interval),
            "RSS_FEEDS": rss_feeds,
            "MAX_DEALS_PER_SCAN": int(max_deals),
            "MEMORY_FILE": memory_file,
            "LOG_LEVEL": log_level,
            "DNN_WEIGHTS_PATH": dnn_weights,
            "DASHBOARD_PORT": int(dashboard_port),
            "API_PORT": int(api_port),
        }
        try:
            # 1. Persist to ui_settings.json (survives tab switches & page refreshes)
            SettingsStore.write(d)
            # 2. Write .env so agents pick up changes on next restart
            _write_env(d)
            return gr.update(value="✅ Settings saved to disk and .env updated. Restart services to apply agent changes.", visible=True)
        except Exception as e:
            return gr.update(value=f"❌ Error saving settings: {e}", visible=True)

    def load_saved_settings():
        """Called on page load — returns all 26 component values from persisted JSON."""
        d = _load_persisted()
        return (
            d["OPENAI_API_KEY"],
            d["ANTHROPIC_API_KEY"],
            d["PUSHOVER_USER"],
            d["PUSHOVER_TOKEN"],
            d["MODAL_TOKEN_ID"],
            d["MODAL_TOKEN_SECRET"],
            float(d["DEAL_THRESHOLD"]),
            int(d["SCAN_INTERVAL_MINUTES"]),
            d["SCANNER_MODEL"],
            d["FRONTIER_MODEL"],
            d["MESSAGING_MODEL"],
            d["ENSEMBLE_WEIGHTS"],
            d["CHROMA_DB_PATH"],
            d["EMBEDDING_MODEL"],
            int(d["CHROMA_RESULTS"]),
            int(d["RAG_MAX_POINTS"]),
            d["PUSHOVER_SOUND"],
            d["NOTIFICATION_TITLE"],
            int(d["NOTIF_MIN_INTERVAL"]),
            d["RSS_FEEDS"],
            int(d["MAX_DEALS_PER_SCAN"]),
            d["MEMORY_FILE"],
            d["LOG_LEVEL"],
            d["DNN_WEIGHTS_PATH"],
            int(d["DASHBOARD_PORT"]),
            int(d["API_PORT"]),
        )

    def validate_settings(openai_key, anthropic_key, pushover_user, pushover_token, modal_id, *args):
        msgs = []
        msgs.append("✅ OpenAI key format valid" if openai_key and openai_key.startswith("sk-") else "⚠️ OpenAI key missing or invalid format")
        msgs.append("✅ Anthropic key format valid" if anthropic_key and anthropic_key.startswith("sk-ant-") else "⚠️ Anthropic key missing or invalid format")
        msgs.append("✅ Pushover user key provided" if pushover_user else "⚠️ Pushover user key missing")
        msgs.append("✅ Pushover token provided" if pushover_token else "⚠️ Pushover token missing")
        msgs.append("✅ Modal token ID provided" if modal_id else "ℹ️ Modal token not set (optional — disables Specialist Agent)")
        return gr.update(value="\n".join(msgs), visible=True)

    def reset_settings():
        d = DEFAULTS
        return (
            d["OPENAI_API_KEY"], d["ANTHROPIC_API_KEY"], d["PUSHOVER_USER"], d["PUSHOVER_TOKEN"],
            d["MODAL_TOKEN_ID"], d["MODAL_TOKEN_SECRET"],
            float(d["DEAL_THRESHOLD"]), int(d["SCAN_INTERVAL_MINUTES"]),
            d["SCANNER_MODEL"], d["FRONTIER_MODEL"], d["MESSAGING_MODEL"],
            d["ENSEMBLE_WEIGHTS"], d["CHROMA_DB_PATH"], d["EMBEDDING_MODEL"],
            int(d["CHROMA_RESULTS"]), int(d["RAG_MAX_POINTS"]),
            d["PUSHOVER_SOUND"], d["NOTIFICATION_TITLE"], int(d["NOTIF_MIN_INTERVAL"]),
            d["RSS_FEEDS"], int(d["MAX_DEALS_PER_SCAN"]),
            d["MEMORY_FILE"], d["LOG_LEVEL"], d["DNN_WEIGHTS_PATH"],
            int(d["DASHBOARD_PORT"]), int(d["API_PORT"]),
            gr.update(value="🔄 Settings reset to defaults. Click Save & Apply to persist.", visible=True)
        )

    def export_settings(openai_key, anthropic_key, pushover_user, pushover_token, modal_id, modal_secret,
                        deal_threshold, scan_interval, scanner_model, frontier_model, messaging_model,
                        ens_weights, chroma_path, embed_model, chroma_results, rag_max_points,
                        notif_sound, notif_title, notif_min_interval,
                        rss_feeds, max_deals, memory_file, log_level, dnn_weights, dashboard_port, api_port):
        """Write settings_export.json (secrets redacted) and show CLI instructions."""
        export_data = {
            "_comment": "Exported from The Price Is Right AI — secrets are REDACTED. Fill them in before importing.",
            "_exported_at": datetime.now().isoformat(),
            "OPENAI_API_KEY": "sk-REPLACE_ME" if openai_key else "",
            "ANTHROPIC_API_KEY": "sk-ant-REPLACE_ME" if anthropic_key else "",
            "PUSHOVER_USER": "REPLACE_ME" if pushover_user else "",
            "PUSHOVER_TOKEN": "REPLACE_ME" if pushover_token else "",
            "MODAL_TOKEN_ID": "REPLACE_ME" if modal_id else "",
            "MODAL_TOKEN_SECRET": "REPLACE_ME" if modal_secret else "",
            "DEAL_THRESHOLD": float(deal_threshold),
            "SCAN_INTERVAL_MINUTES": int(scan_interval),
            "SCANNER_MODEL": scanner_model,
            "FRONTIER_MODEL": frontier_model,
            "MESSAGING_MODEL": messaging_model,
            "ENSEMBLE_WEIGHTS": ens_weights,
            "CHROMA_DB_PATH": chroma_path,
            "EMBEDDING_MODEL": embed_model,
            "CHROMA_RESULTS": int(chroma_results),
            "RAG_MAX_POINTS": int(rag_max_points),
            "PUSHOVER_SOUND": notif_sound,
            "NOTIFICATION_TITLE": notif_title,
            "NOTIF_MIN_INTERVAL": int(notif_min_interval),
            "RSS_FEEDS": rss_feeds,
            "MAX_DEALS_PER_SCAN": int(max_deals),
            "MEMORY_FILE": memory_file,
            "LOG_LEVEL": log_level,
            "DNN_WEIGHTS_PATH": dnn_weights,
            "DASHBOARD_PORT": int(dashboard_port),
            "API_PORT": int(api_port),
        }
        try:
            os.makedirs(os.path.dirname(EXPORT_JSON_PATH), exist_ok=True)
            with open(EXPORT_JSON_PATH, "w") as f:
                json.dump(export_data, f, indent=2)
            export_path_display = EXPORT_JSON_PATH
        except Exception as ex:
            export_path_display = f"(could not write file: {ex})"

        cli_instructions = f"""# Settings exported to: {export_path_display}
# Fill in REPLACE_ME values with your real secrets, then import:

# === Linux / macOS / WSL ===
./manage.sh import-settings data/settings_export.json

# === Windows PowerShell ===
.\\manage.ps1 import-settings data\\settings_export.json

# === Manual .env update ===
# Copy data/settings_export.json to a text editor, fill in secrets,
# then run: ./manage.sh patch

# === JSON content preview ===
{json.dumps(export_data, indent=2)}"""
        return gr.update(value=cli_instructions, visible=True)

    # ─── Build Gradio UI ─────────────────────────────────────────────────────
    with gr.Blocks(
        title="The Price Is Right — AI Deal Hunter",
        css=CUSTOM_CSS,
        js=_JS_FIX,
        theme=gr.themes.Base(
            primary_hue=gr.themes.colors.orange,
            secondary_hue=gr.themes.colors.teal,
            neutral_hue=gr.themes.colors.stone,
            font=gr.themes.GoogleFont("Hanken Grotesk"),
            font_mono=gr.themes.GoogleFont("JetBrains Mono"),
            text_size=gr.themes.sizes.text_md,
        ).set(
            # ── Body text ──────────────────────────────────────────────────
            body_text_color="#f7ddd5",
            body_text_color_subdued="#e1bfb5",
            # ── Input fields ───────────────────────────────────────────────
            input_background_fill="#1a0a00",
            input_background_fill_dark="#1a0a00",
            input_background_fill_focus="#261814",
            input_border_color="#594139",
            input_border_color_focus="#ffb59d",
            input_placeholder_color="#7a5a50",
            # ── Blocks / panels ────────────────────────────────────────────
            block_background_fill="#2a1c18",
            block_background_fill_dark="#2a1c18",
            block_border_color="#594139",
            block_label_text_color="#e1bfb5",
            block_label_text_color_dark="#e1bfb5",
            block_title_text_color="#f7ddd5",
            block_title_text_color_dark="#f7ddd5",
            panel_background_fill="#261814",
            panel_border_color="#594139",
            # ── Buttons ────────────────────────────────────────────────────
            button_secondary_text_color="#f7ddd5",
            button_secondary_background_fill="#2a1c18",
            button_secondary_border_color="#594139",
            button_primary_text_color="#5d1900",
            button_primary_background_fill="#ffb59d",
            # ── Table ──────────────────────────────────────────────────────
            table_text_color="#f7ddd5",
            # ── Checkbox ───────────────────────────────────────────────────
            checkbox_background_color="#1a0a00",
            checkbox_border_color="#594139",
            checkbox_label_text_color="#f7ddd5",
            # ── Slider ─────────────────────────────────────────────────────
            slider_color="#ffb59d",
            # ── Stat card ──────────────────────────────────────────────────
            stat_background_fill="#2a1c18",
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
                            openai_key = gr.Textbox(label="OPENAI API KEY", placeholder="sk-...", type="password", elem_classes=["pir-input"])
                            with gr.Row():
                                test_openai_btn = gr.Button("Test OpenAI", size="sm", variant="secondary")
                                openai_status = gr.Textbox(label="", show_label=False, interactive=False, scale=3, elem_classes=["pir-status"])
                        with gr.Column():
                            anthropic_key = gr.Textbox(label="ANTHROPIC API KEY", placeholder="sk-ant-...", type="password", elem_classes=["pir-input"])
                            with gr.Row():
                                test_anthropic_btn = gr.Button("Test Anthropic", size="sm", variant="secondary")
                                anthropic_status = gr.Textbox(label="", show_label=False, interactive=False, scale=3, elem_classes=["pir-status"])
                    with gr.Row():
                        with gr.Column():
                            pushover_user = gr.Textbox(label="PUSHOVER USER KEY", placeholder="User Key", type="password", elem_classes=["pir-input"])
                            with gr.Row():
                                test_pushover_btn = gr.Button("Test Pushover", size="sm", variant="secondary")
                                pushover_status = gr.Textbox(label="", show_label=False, interactive=False, scale=3, elem_classes=["pir-status"])
                        with gr.Column():
                            pushover_token = gr.Textbox(label="PUSHOVER APP TOKEN", placeholder="App Token", type="password", elem_classes=["pir-input"])
                    with gr.Row():
                        with gr.Column():
                            modal_id = gr.Textbox(label="MODAL TOKEN ID", placeholder="ak-...", type="password", elem_classes=["pir-input"])
                        with gr.Column():
                            modal_secret = gr.Textbox(label="MODAL TOKEN SECRET", placeholder="...", type="password", elem_classes=["pir-input"])
                            with gr.Row():
                                test_modal_btn = gr.Button("Test Modal", size="sm", variant="secondary")
                                modal_status = gr.Textbox(label="", show_label=False, interactive=False, scale=3, elem_classes=["pir-status"])

                # Section 2: Agent Configuration
                with gr.Accordion("🤖 Agent Configuration", open=True):
                    with gr.Row():
                        deal_threshold = gr.Slider(label="DEAL THRESHOLD (%)", minimum=1, maximum=90, value=50, step=1, elem_classes=["pir-slider"])
                        scan_interval = gr.Slider(label="SCAN INTERVAL (MIN)", minimum=1, maximum=60, value=5, step=1, elem_classes=["pir-slider"])
                    with gr.Row():
                        scanner_model = gr.Dropdown(
                            label="SCANNER MODEL",
                            choices=["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
                            value="gpt-4o-mini",
                            elem_classes=["pir-dropdown"]
                        )
                        frontier_model = gr.Dropdown(
                            label="FRONTIER MODEL",
                            choices=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
                            value="gpt-4o",
                            elem_classes=["pir-dropdown"]
                        )
                        messaging_model = gr.Dropdown(
                            label="MESSAGING MODEL",
                            choices=["claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-haiku-20240307"],
                            value="claude-3-5-sonnet-20241022",
                            elem_classes=["pir-dropdown"]
                        )
                    ens_weights = gr.Textbox(
                        label="ENSEMBLE WEIGHTS (FRONTIER, SPECIALIST, DNN — MUST SUM TO 1.0)",
                        value="0.8, 0.1, 0.1",
                        placeholder="0.8, 0.1, 0.1",
                        elem_classes=["pir-input"]
                    )

                # Section 3: RAG Database
                with gr.Accordion("🧠 RAG Database", open=False):
                    with gr.Row():
                        chroma_path = gr.Textbox(label="CHROMADB STORAGE PATH", value="./data/products_vectorstore", elem_classes=["pir-input"])
                        embed_model = gr.Dropdown(
                            label="EMBEDDING MODEL",
                            choices=["sentence-transformers/all-MiniLM-L6-v2", "text-embedding-3-small", "text-embedding-ada-002"],
                            value="sentence-transformers/all-MiniLM-L6-v2",
                            elem_classes=["pir-dropdown"]
                        )
                    with gr.Row():
                        chroma_results = gr.Slider(label="RAG RESULTS COUNT", minimum=1, maximum=20, value=5, step=1, elem_classes=["pir-slider"])
                        rag_max_points = gr.Slider(label="VISUALISATION MAX POINTS", minimum=100, maximum=5000, value=1000, step=100, elem_classes=["pir-slider"])

                # Section 4: Notifications
                with gr.Accordion("🔔 Notifications", open=False):
                    with gr.Row():
                        notif_sound = gr.Dropdown(
                            label="PUSHOVER SOUND",
                            choices=["pushover", "bike", "bugle", "cashregister", "classical", "cosmic", "falling", "gamelan", "incoming", "intermission", "magic", "mechanical", "pianobar", "siren", "spacealarm", "tugboat", "alien", "climb", "persistent", "echo", "updown"],
                            value="pushover",
                            elem_classes=["pir-dropdown"]
                        )
                        notif_title = gr.Textbox(label="NOTIFICATION TITLE", value="The Price Is Right Alert", elem_classes=["pir-input"])
                    notif_min_interval = gr.Slider(label="MIN INTERVAL BETWEEN NOTIFICATIONS (MIN)", minimum=1, maximum=60, value=5, step=1, elem_classes=["pir-slider"])

                # Section 5: RSS Feeds
                with gr.Accordion("📡 RSS Feeds", open=True):
                    rss_feeds = gr.Textbox(
                        label="FEED SOURCES (ONE PER LINE)",
                        value="https://www.dealnews.com/rss.html\nhttps://feeds.feedburner.com/techbargains\nhttps://slickdeals.net/newsearch.php?mode=frontpage&searcharea=deals&searchin=first&rss=1",
                        lines=5,
                        placeholder="https://...",
                        elem_classes=["pir-input"]
                    )
                    max_deals = gr.Slider(label="MAX DEALS PER SCAN", minimum=1, maximum=200, value=50, step=1, elem_classes=["pir-slider"])

                # Section 6: Advanced
                with gr.Accordion("⚙️ Advanced", open=False):
                    with gr.Row():
                        memory_file = gr.Textbox(label="MEMORY FILE PATH", value="./data/memory.json", elem_classes=["pir-input"])
                        log_level = gr.Dropdown(label="LOG LEVEL", choices=["DEBUG", "INFO", "WARNING", "ERROR"], value="INFO", elem_classes=["pir-dropdown"])
                    with gr.Row():
                        dnn_weights = gr.Textbox(label="DNN WEIGHTS PATH", value="./data/dnn_weights.pt", elem_classes=["pir-input"])
                        dashboard_port = gr.Number(label="DASHBOARD PORT", value=7860, elem_classes=["pir-number"])
                    api_port = gr.Number(label="API PORT", value=8000, elem_classes=["pir-number"])

                # ── Settings Action Buttons ──────────────────────────────────────────────
                gr.HTML('<div style="height:16px"></div>')
                with gr.Row():
                    reset_btn = gr.Button("🔄 Reset to Defaults", variant="secondary")
                    validate_btn = gr.Button("✅ Validate Only", variant="secondary")
                    export_btn = gr.Button("📤 Export Settings", variant="secondary")
                save_btn = gr.Button("💾 Save & Apply", variant="primary", size="lg")

                settings_msg = gr.Textbox(label="STATUS", interactive=False, visible=False, elem_classes=["pir-status"])
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

        # ── All 26 settings inputs/outputs (shared across handlers) ───────────────────
        ALL_SETTINGS_INPUTS = [
            openai_key, anthropic_key, pushover_user, pushover_token, modal_id, modal_secret,
            deal_threshold, scan_interval, scanner_model, frontier_model, messaging_model,
            ens_weights, chroma_path, embed_model, chroma_results, rag_max_points,
            notif_sound, notif_title, notif_min_interval,
            rss_feeds, max_deals, memory_file, log_level, dnn_weights, dashboard_port, api_port
        ]
        ALL_SETTINGS_OUTPUTS = [
            openai_key, anthropic_key, pushover_user, pushover_token, modal_id, modal_secret,
            deal_threshold, scan_interval, scanner_model, frontier_model, messaging_model,
            ens_weights, chroma_path, embed_model, chroma_results, rag_max_points,
            notif_sound, notif_title, notif_min_interval,
            rss_feeds, max_deals, memory_file, log_level, dnn_weights, dashboard_port, api_port
        ]

        # ── Event Wiring ────────────────────────────────────────────────────────────────
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

        # ── PERSISTENCE: reload saved settings on every page load ────────────────────
        # This fires automatically when the browser opens/refreshes the page.
        app.load(
            fn=load_saved_settings,
            inputs=None,
            outputs=ALL_SETTINGS_OUTPUTS
        )

        # ── Save & Apply ─────────────────────────────────────────────────────────────
        save_btn.click(
            fn=save_settings,
            inputs=ALL_SETTINGS_INPUTS,
            outputs=[settings_msg]
        ).then(lambda: gr.update(visible=True), outputs=[settings_msg])

        # ── Validate Only ───────────────────────────────────────────────────────────
        validate_btn.click(
            fn=validate_settings,
            inputs=[openai_key, anthropic_key, pushover_user, pushover_token, modal_id],
            outputs=[settings_msg]
        ).then(lambda: gr.update(visible=True), outputs=[settings_msg])

        # ── Reset to Defaults ─────────────────────────────────────────────────────────
        reset_btn.click(
            fn=reset_settings,
            outputs=ALL_SETTINGS_OUTPUTS + [settings_msg]
        )

        # ── Export Settings ──────────────────────────────────────────────────────────
        export_btn.click(
            fn=export_settings,
            inputs=ALL_SETTINGS_INPUTS,
            outputs=[export_output]
        ).then(lambda: gr.update(visible=True), outputs=[export_output])

        # ── API Key Test Buttons ─────────────────────────────────────────────────────
        test_openai_btn.click(
            fn=lambda k: "✅ Format OK (sk-...)" if k and k.startswith("sk-") else "⚠️ Invalid format",
            inputs=[openai_key], outputs=[openai_status]
        )
        test_anthropic_btn.click(
            fn=lambda k: "✅ Format OK (sk-ant-...)" if k and k.startswith("sk-ant-") else "⚠️ Invalid format",
            inputs=[anthropic_key], outputs=[anthropic_status]
        )
        test_pushover_btn.click(
            fn=lambda k: "✅ Key provided" if k else "⚠️ Key missing",
            inputs=[pushover_user], outputs=[pushover_status]
        )
        test_modal_btn.click(
            fn=lambda k: "✅ Token provided" if k else "⚠️ Token missing (optional)",
            inputs=[modal_id], outputs=[modal_status]
        )

        # Persistence load on page render
        app.load(
            fn=load_saved_settings,
            inputs=[],
            outputs=all_settings_inputs
        )

    return app
