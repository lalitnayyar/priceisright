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
        import logging
        logging.getLogger(__name__).info("save_settings called from UI")
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
            # ── Checkbox ───────────────────────────────────────────────────
            checkbox_background_color="#1a0a00",
            checkbox_border_color="#594139",
            checkbox_label_text_color="#f7ddd5",
            # ── Slider ─────────────────────────────────────────────────────
            slider_color="#ffb59d",
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
                    gr.HTML("""
                    <div id="dynamic-agent-status-container">
                        <div style="padding:20px;text-align:center;color:#e1bfb5;font-family:'JetBrains Mono',monospace">
                            Loading agent status...
                        </div>
                    </div>
                    
                    <script>
                    async function fetchAgentStatus() {
                        try {
                            const res = await fetch("/status");
                            if (!res.ok) throw new Error("Status API returned " + res.status);
                            
                            const statuses = await res.json();
                            
                            let rows = "";
                            statuses.forEach(s => {
                                const status = s.status || "READY";
                                let badge = "";
                                let hb = "";
                                
                                if (status === "RUNNING") {
                                    badge = '<span class="badge-running">RUNNING ●</span>';
                                    hb = '<span class="heartbeat-running">●</span>';
                                } else if (status === "ERROR") {
                                    badge = '<span class="badge-error">⚠ ERROR</span>';
                                    hb = '<span class="heartbeat-error">●</span>';
                                } else {
                                    badge = '<span class="badge-ready">READY</span>';
                                    hb = '<span class="heartbeat-ready">●</span>';
                                }
                                
                                rows += `
                                <tr>
                                    <td style="padding:12px 16px;border-bottom:1px solid rgba(89,65,57,0.3);color:#f7ddd5;font-weight:500">${s.name || ''}</td>
                                    <td style="padding:12px 16px;border-bottom:1px solid rgba(89,65,57,0.3)">${badge}</td>
                                    <td style="padding:12px 16px;border-bottom:1px solid rgba(89,65,57,0.3)">${hb}</td>
                                </tr>`;
                            });
                            
                            const html = `
                            <div style="overflow-x:auto;background:#1d100c;border-radius:8px;border:1px solid #594139">
                            <table style="width:100%;border-collapse:collapse;font-family:'JetBrains Mono',monospace;font-size:13px">
                                <thead>
                                    <tr style="background:#261814;border-bottom:1px solid #594139">
                                        <th style="padding:12px 16px;text-align:left;color:#e1bfb5;text-transform:uppercase;font-size:11px;letter-spacing:0.05em">Agent Module</th>
                                        <th style="padding:12px 16px;text-align:left;color:#e1bfb5;text-transform:uppercase;font-size:11px;letter-spacing:0.05em">Current Status</th>
                                        <th style="padding:12px 16px;text-align:left;color:#e1bfb5;text-transform:uppercase;font-size:11px;letter-spacing:0.05em">Heartbeat</th>
                                    </tr>
                                </thead>
                                <tbody>${rows}</tbody>
                            </table>
                            </div>`;
                            
                            const container = document.getElementById("dynamic-agent-status-container");
                            if (container) container.innerHTML = html;
                        } catch (e) {
                            console.error("Failed to fetch agent status:", e);
                        }
                    }
                    
                    // Fetch immediately and then poll every 5 seconds
                    document.addEventListener("DOMContentLoaded", () => {
                        fetchAgentStatus();
                        setInterval(fetchAgentStatus, 5000);
                    });
                    </script>
                    """)

                # Section 2: Deal Opportunities
                with gr.Accordion("🔥 Deal Opportunities Found", open=True):
                    gr.HTML("""
                    <div id="dynamic-deals-container">
                        <div style="padding:24px;text-align:center;color:#e1bfb5;font-family:'JetBrains Mono',monospace">
                            Loading deals...
                        </div>
                    </div>
                    
                    <script>
                    async function fetchDeals() {
                        try {
                            const res = await fetch("/results");
                            if (!res.ok) return;
                            
                            const results = await res.json();
                            
                            if (!results || results.length === 0) {
                                document.getElementById("dynamic-deals-container").innerHTML = 
                                    '<div style="padding:24px;text-align:center;color:#e1bfb5;font-family:\\'JetBrains Mono\\',monospace">No deals scanned yet. Click "Scan for Deals Now" to begin.</div>';
                                return;
                            }
                            
                            let cards = "";
                            results.forEach(r => {
                                const deal = r.deal || {};
                                const ensemble = r.ensemble_result || {};
                                const is_great = ensemble.is_great_deal || false;
                                const discount = ensemble.discount_pct || 0;
                                const estimated = ensemble.estimated_price || 0;
                                const listed = deal.price || 0;
                                const title = deal.title || "Unknown Product";
                                const url = deal.url || "#";
                                
                                const great_badge = is_great ? '<span style="background:#ff6b35;color:#5f1900;font-size:10px;font-weight:700;padding:2px 8px;border-radius:999px;font-family:\\'JetBrains Mono\\',monospace">GREAT DEAL</span>' : "";
                                const border_style = is_great ? "border-left:4px solid #ff6b35;box-shadow:0 4px 12px rgba(255,107,53,0.15);" : "";
                                const action_btn = is_great ? 
                                    `<a href="${url}" target="_blank" style="background:#ff6b35;color:#5f1900;padding:4px 12px;border-radius:4px;font-size:11px;font-weight:700;text-decoration:none;font-family:\\'JetBrains Mono\\',monospace">SNIPE NOW</a>` : 
                                    `<a href="${url}" target="_blank" style="color:#ffb59d;font-size:11px;font-weight:700;text-decoration:none;font-family:\\'JetBrains Mono\\',monospace;text-transform:uppercase">Analyze</a>`;
                                const discount_color = is_great ? "#ff6b35" : "#5dd9d0";
                                
                                cards += `
                                <div style="background:#2a1c18;border:1px solid #594139;border-radius:8px;padding:16px;margin-bottom:12px;display:flex;gap:16px;align-items:flex-start;${border_style}">
                                    <div style="width:64px;height:64px;background:#41312c;border-radius:6px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:24px">🏷️</div>
                                    <div style="flex:1">
                                        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px">
                                            <span style="font-weight:700;color:#f7ddd5;font-size:15px">${title}</span>
                                            ${great_badge}
                                        </div>
                                        <div style="display:flex;gap:16px;font-family:'JetBrains Mono',monospace;font-size:12px;margin-bottom:8px">
                                            <span style="color:#e1bfb5">Listed: <span style="color:#f7ddd5;font-weight:700">$${listed.toFixed(2)}</span></span>
                                            <span style="color:#e1bfb5">Est: <span style="color:#f7ddd5">$${estimated.toFixed(2)}</span></span>
                                        </div>
                                        <div style="display:flex;justify-content:space-between;align-items:center">
                                            <span style="color:${discount_color};font-weight:700;font-size:13px">${discount.toFixed(1)}% Off Potential</span>
                                            ${action_btn}
                                        </div>
                                    </div>
                                </div>`;
                            });
                            
                            const container = document.getElementById("dynamic-deals-container");
                            if (container) container.innerHTML = cards;
                        } catch (e) {
                            console.error("Failed to fetch deals:", e);
                        }
                    }
                    
                    // Fetch immediately and then poll every 5 seconds
                    document.addEventListener("DOMContentLoaded", () => {
                        fetchDeals();
                        setInterval(fetchDeals, 5000);
                    });
                    </script>
                    """)

                # Section 3: Live Agent Logs
                with gr.Accordion("📋 Live Agent Logs", open=True):
                    gr.HTML("""
                    <div id="dynamic-logs-container">
                        <div style="background:#000;border:1px solid #594139;border-radius:4px;padding:16px;font-family:'JetBrains Mono',monospace;font-size:12px;max-height:400px;overflow-y:auto;line-height:1.6">
                            <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;border-bottom:1px solid rgba(255,255,255,0.1);padding-bottom:8px">
                                <div style="width:10px;height:10px;border-radius:50%;background:#F85149"></div>
                                <div style="width:10px;height:10px;border-radius:50%;background:#ff6b35"></div>
                                <div style="width:10px;height:10px;border-radius:50%;background:#5DD9D0"></div>
                                <span style="color:rgba(247,221,213,0.4);margin-left:8px">agent_orchestrator_v1.2.log</span>
                            </div>
                            <div id="dynamic-logs-content">
                                <p style="color:rgba(247,221,213,0.4)">Loading logs...</p>
                            </div>
                        </div>
                    </div>
                    
                    <script>
                    async function fetchLogs() {
                        try {
                            const res = await fetch("/results");
                            if (!res.ok) return;
                            
                            const results = await res.json();
                            
                            // For now we'll just extract log-like info from the results since we don't have a dedicated /logs endpoint
                            // If there are results, show that a scan happened
                            let lines = "";
                            const now = new Date();
                            const ts = now.getHours().toString().padStart(2, '0') + ":" + 
                                       now.getMinutes().toString().padStart(2, '0') + ":" + 
                                       now.getSeconds().toString().padStart(2, '0');
                            
                            if (results && results.length > 0) {
                                lines += `<p style="margin:2px 0"><span style="color:#FF6B35">[${ts}]</span> <span style="color:#5DD9D0">System:</span> <span style="color:#4ECDC4">Retrieved ${results.length} recent deals from memory.</span></p>\\n`;
                            } else {
                                lines += `<p style="color:rgba(247,221,213,0.4)">No deals in memory yet. Run a scan to see agent activity.</p>`;
                            }
                            
                            const container = document.getElementById("dynamic-logs-content");
                            if (container && container.innerHTML.includes("Loading")) {
                                container.innerHTML = lines;
                            }
                        } catch (e) {
                            console.error("Failed to fetch logs:", e);
                        }
                    }
                    
                    // Fetch immediately and then poll every 5 seconds
                    document.addEventListener("DOMContentLoaded", () => {
                        fetchLogs();
                        setInterval(fetchLogs, 5000);
                    });
                    </script>
                    """)
                    with gr.Row():
                        scan_btn = gr.Button(
                            "🔍 Scan for Deals Now",
                            variant="primary",
                            size="lg",
                            elem_classes=["scan-btn"]
                        )

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
            # TAB 2 — SETTINGS (PURE HTML + JS FETCH)
            # ════════════════════════════════════════════════════════════════
            with gr.Tab("⚙️ Settings", id="tab-settings"):
                gr.HTML("""<!-- SETTINGS TAB v2.2 -->
                <style>
                    .pir-settings-form { padding: 20px; font-family: 'Hanken Grotesk', sans-serif; color: #f7ddd5; max-width: 1200px; margin: 0 auto; }
                    .pir-settings-form h2 { color: #ffb59d; border-bottom: 1px solid #594139; padding-bottom: 10px; margin-bottom: 8px; font-size: 22px; }
                    .pir-settings-form .pir-subtitle { color: #e1bfb5; margin-bottom: 24px; font-size: 13px; }
                    .pir-group { background: #2a1c18; border: 1px solid #594139; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
                    .pir-group h3 { margin-top: 0; margin-bottom: 16px; color: #e1bfb5; font-size: 14px; font-weight: 700; letter-spacing: 0.5px; }
                    .pir-row { display: flex; gap: 16px; margin-bottom: 14px; flex-wrap: wrap; }
                    .pir-field { flex: 1; min-width: 200px; display: flex; flex-direction: column; gap: 5px; }
                    .pir-field label { font-size: 11px; font-weight: 700; letter-spacing: 1px; color: #e1bfb5; text-transform: uppercase; }
                    .pir-field input, .pir-field select, .pir-field textarea {
                        background: #1a0a00; border: 1px solid #594139; color: #f7ddd5 !important;
                        padding: 10px 12px; border-radius: 6px; font-family: 'JetBrains Mono', monospace; font-size: 13px; width: 100%; box-sizing: border-box;
                    }
                    .pir-field input:focus, .pir-field select:focus, .pir-field textarea:focus { border-color: #ffb59d; outline: none; box-shadow: 0 0 0 2px rgba(255,181,157,0.2); }
                    .pir-field select option { background: #1a0a00; color: #f7ddd5; }
                    /* Slider styling */
                    .pir-slider-row { display: flex; align-items: center; gap: 12px; }
                    .pir-slider-row input[type=range] { flex: 1; accent-color: #ffb59d; cursor: pointer; }
                    .pir-slider-val { background: #1a0a00; border: 1px solid #594139; color: #ffb59d; padding: 4px 10px; border-radius: 4px; font-family: 'JetBrains Mono', monospace; font-size: 13px; min-width: 50px; text-align: center; }
                    /* Test button row */
                    .pir-test-row { display: flex; gap: 12px; margin-top: 10px; flex-wrap: wrap; }
                    .pir-btn-test { background: #352722; border: 1px solid #594139; color: #e1bfb5; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-family: 'JetBrains Mono', monospace; font-size: 12px; display: flex; align-items: center; gap: 8px; transition: all 0.2s; }
                    .pir-btn-test:hover { border-color: #ffb59d; color: #ffb59d; }
                    .pir-test-status { flex: 1; background: #1a0a00; border: 1px solid #594139; border-radius: 6px; padding: 8px 12px; font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #7a5a50; min-width: 120px; }
                    .pir-test-status.ok { color: #4ECDC4; border-color: #2a5a3f; }
                    .pir-test-status.err { color: #ff6b35; border-color: #5a2a2a; }
                    /* Bottom action bar */
                    .pir-action-bar { display: flex; gap: 12px; margin-top: 24px; flex-wrap: wrap; }
                    .pir-btn-secondary { flex: 1; background: #352722; border: 1px solid #594139; color: #e1bfb5; padding: 12px 16px; border-radius: 6px; cursor: pointer; font-family: 'Hanken Grotesk', sans-serif; font-size: 14px; font-weight: 600; transition: all 0.2s; }
                    .pir-btn-secondary:hover { border-color: #ffb59d; color: #ffb59d; }
                    .pir-btn-primary { flex: 2; background: #ffb59d; color: #5d1900; border: none; padding: 14px 24px; font-weight: 700; border-radius: 6px; cursor: pointer; font-size: 15px; font-family: 'Hanken Grotesk', sans-serif; transition: background 0.2s; }
                    .pir-btn-primary:hover { background: #ffc9b8; }
                    #pir-status-msg { margin-top: 14px; padding: 12px 16px; border-radius: 6px; display: none; font-weight: 600; font-size: 13px; }
                    .pir-success { background: #1b3a28; color: #4ECDC4; border: 1px solid #2a5a3f; }
                    .pir-error { background: #3a1b1b; color: #ff6b35; border: 1px solid #5a2a2a; }
                    .pir-warn { background: #3a2e1b; color: #ffb59d; border: 1px solid #5a4a2a; }
                </style>

                <div class="pir-settings-form">
                    <h2>System Configuration</h2>
                    <p class="pir-subtitle">Manage your agent parameters, database connections, and external API integrations. Changes apply immediately to all agents.</p>

                    <form id="pir-settings-form-element">

                        <!-- ──────────────────────────────────────────────────────────────── -->
                        <!-- SECTION 1: API KEYS -->
                        <!-- ──────────────────────────────────────────────────────────────── -->
                        <div class="pir-group">
                            <h3>🔑 API Keys <small style="font-size:11px;color:#a08070;font-weight:normal;margin-left:8px">
                                <label style="cursor:pointer;user-select:none">
                                    <input type="checkbox" id="show-keys-toggle" style="margin-right:4px">Show keys
                                </label>
                            </small></h3>
                            <div class="pir-row">
                                <div class="pir-field"><label>OPENAI API KEY</label>
                                    <input type="text" id="OPENAI_API_KEY" placeholder="sk-..." class="pir-secret-field" autocomplete="off" spellcheck="false">
                                </div>
                                <div class="pir-field"><label>ANTHROPIC API KEY</label>
                                    <input type="text" id="ANTHROPIC_API_KEY" placeholder="sk-ant-..." class="pir-secret-field" autocomplete="off" spellcheck="false">
                                </div>
                            </div>
                            <div class="pir-test-row">
                                <button type="button" class="pir-btn-test" data-test="openai">Test OpenAI</button>
                                <span class="pir-test-status" id="test-openai-status">Not tested</span>
                                <button type="button" class="pir-btn-test" data-test="anthropic">Test Anthropic</button>
                                <span class="pir-test-status" id="test-anthropic-status">Not tested</span>
                            </div>
                            <div class="pir-row" style="margin-top:14px">
                                <div class="pir-field"><label>PUSHOVER USER KEY</label>
                                    <input type="text" id="PUSHOVER_USER" placeholder="User Key" class="pir-secret-field" autocomplete="off" spellcheck="false">
                                </div>
                                <div class="pir-field"><label>PUSHOVER APP TOKEN</label>
                                    <input type="text" id="PUSHOVER_TOKEN" placeholder="App Token" class="pir-secret-field" autocomplete="off" spellcheck="false">
                                </div>
                            </div>
                            <div class="pir-test-row">
                                <button type="button" class="pir-btn-test" data-test="pushover">Test Pushover</button>
                                <span class="pir-test-status" id="test-pushover-status">Not tested</span>
                            </div>
                            <div class="pir-row" style="margin-top:14px">
                                <div class="pir-field"><label>MODAL TOKEN ID</label>
                                    <input type="text" id="MODAL_TOKEN_ID" placeholder="ak-..." class="pir-secret-field" autocomplete="off" spellcheck="false">
                                </div>
                                <div class="pir-field"><label>MODAL TOKEN SECRET</label>
                                    <input type="text" id="MODAL_TOKEN_SECRET" placeholder="..." class="pir-secret-field" autocomplete="off" spellcheck="false">
                                </div>
                            </div>
                            <div class="pir-test-row">
                                <button type="button" class="pir-btn-test" data-test="modal">Test Modal</button>
                                <span class="pir-test-status" id="test-modal-status">Not tested</span>
                            </div>
                        </div>

                        <!-- ──────────────────────────────────────────────────────────────── -->
                        <!-- SECTION 2: AGENT CONFIGURATION -->
                        <!-- ──────────────────────────────────────────────────────────────── -->
                        <div class="pir-group">
                            <h3>🤖 Agent Configuration</h3>
                            <div class="pir-row">
                                <div class="pir-field">
                                    <label>DEAL THRESHOLD (%)</label>
                                    <div class="pir-slider-row">
                                        <input type="range" id="DEAL_THRESHOLD" min="1" max="90" step="1" data-display="deal-thresh-val">
                                        <span class="pir-slider-val" id="deal-thresh-val">50</span>
                                    </div>
                                </div>
                                <div class="pir-field">
                                    <label>SCAN INTERVAL (MIN)</label>
                                    <div class="pir-slider-row">
                                        <input type="range" id="SCAN_INTERVAL_MINUTES" min="1" max="60" step="1" data-display="scan-interval-val">
                                        <span class="pir-slider-val" id="scan-interval-val">5</span>
                                    </div>
                                </div>
                            </div>
                            <div class="pir-row">
                                <div class="pir-field"><label>SCANNER MODEL</label>
                                    <select id="SCANNER_MODEL">
                                        <option value="gpt-4o-mini">gpt-4o-mini</option>
                                        <option value="gpt-4o">gpt-4o</option>
                                        <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
                                    </select>
                                </div>
                                <div class="pir-field"><label>FRONTIER MODEL</label>
                                    <select id="FRONTIER_MODEL">
                                        <option value="gpt-4o">gpt-4o</option>
                                        <option value="gpt-4o-mini">gpt-4o-mini</option>
                                        <option value="gpt-4-turbo">gpt-4-turbo</option>
                                    </select>
                                </div>
                                <div class="pir-field"><label>MESSAGING MODEL</label>
                                    <select id="MESSAGING_MODEL">
                                        <option value="claude-3-5-sonnet-20241022">claude-3-5-sonnet-20241022</option>
                                        <option value="claude-3-opus-20240229">claude-3-opus-20240229</option>
                                        <option value="claude-3-haiku-20240307">claude-3-haiku-20240307</option>
                                    </select>
                                </div>
                            </div>
                            <div class="pir-row">
                                <div class="pir-field"><label>ENSEMBLE WEIGHTS (FRONTIER, SPECIALIST, DNN — MUST SUM TO 1.0)</label><input type="text" id="ENSEMBLE_WEIGHTS" placeholder="0.8, 0.1, 0.1"></div>
                            </div>
                        </div>

                        <!-- ──────────────────────────────────────────────────────────────── -->
                        <!-- SECTION 3: RAG & VECTOR STORE -->
                        <!-- ──────────────────────────────────────────────────────────────── -->
                        <div class="pir-group">
                            <h3>🧠 RAG & Vector Store</h3>
                            <div class="pir-row">
                                <div class="pir-field"><label>CHROMADB STORAGE PATH</label><input type="text" id="CHROMA_DB_PATH" placeholder="./data/products_vectorstore"></div>
                                <div class="pir-field"><label>EMBEDDING MODEL</label>
                                    <select id="EMBEDDING_MODEL">
                                        <option value="sentence-transformers/all-MiniLM-L6-v2">sentence-transformers/all-MiniLM-L6-v2</option>
                                        <option value="text-embedding-3-small">text-embedding-3-small</option>
                                        <option value="text-embedding-3-large">text-embedding-3-large</option>
                                    </select>
                                </div>
                            </div>
                            <div class="pir-row">
                                <div class="pir-field">
                                    <label>RAG RESULTS COUNT</label>
                                    <div class="pir-slider-row">
                                        <input type="range" id="CHROMA_RESULTS" min="1" max="20" step="1" data-display="chroma-results-val">
                                        <span class="pir-slider-val" id="chroma-results-val">5</span>
                                    </div>
                                </div>
                                <div class="pir-field">
                                    <label>VISUALISATION MAX POINTS</label>
                                    <div class="pir-slider-row">
                                        <input type="range" id="RAG_MAX_POINTS" min="100" max="5000" step="100" data-display="rag-max-val">
                                        <span class="pir-slider-val" id="rag-max-val">1000</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- ──────────────────────────────────────────────────────────────── -->
                        <!-- SECTION 4: NOTIFICATIONS -->
                        <!-- ──────────────────────────────────────────────────────────────── -->
                        <div class="pir-group">
                            <h3>🔔 Notifications</h3>
                            <div class="pir-row">
                                <div class="pir-field"><label>PUSHOVER SOUND</label><input type="text" id="PUSHOVER_SOUND" placeholder="pushover"></div>
                                <div class="pir-field"><label>NOTIFICATION TITLE</label><input type="text" id="NOTIFICATION_TITLE" placeholder="The Price Is Right Alert"></div>
                            </div>
                            <div class="pir-row">
                                <div class="pir-field">
                                    <label>MIN INTERVAL BETWEEN NOTIFICATIONS (MIN)</label>
                                    <div class="pir-slider-row">
                                        <input type="range" id="NOTIF_MIN_INTERVAL" min="1" max="60" step="1" data-display="notif-interval-val">
                                        <span class="pir-slider-val" id="notif-interval-val">5</span>
                                    </div>
                                </div>
                                <div class="pir-field"></div>
                            </div>
                        </div>

                        <!-- ──────────────────────────────────────────────────────────────── -->
                        <!-- SECTION 5: FEED SOURCES -->
                        <!-- ──────────────────────────────────────────────────────────────── -->
                        <div class="pir-group">
                            <h3>📡 Feed Sources</h3>
                            <div class="pir-row">
                                <div class="pir-field"><label>FEED SOURCES (ONE PER LINE)</label><textarea id="RSS_FEEDS" rows="5" placeholder="https://www.dealnews.com/rss.html"></textarea></div>
                            </div>
                            <div class="pir-row">
                                <div class="pir-field">
                                    <label>MAX DEALS PER SCAN</label>
                                    <div class="pir-slider-row">
                                        <input type="range" id="MAX_DEALS_PER_SCAN" min="5" max="200" step="5" data-display="max-deals-val">
                                        <span class="pir-slider-val" id="max-deals-val">50</span>
                                    </div>
                                </div>
                                <div class="pir-field"></div>
                            </div>
                        </div>

                        <!-- ──────────────────────────────────────────────────────────────── -->
                        <!-- SECTION 6: SYSTEM -->
                        <!-- ──────────────────────────────────────────────────────────────── -->
                        <div class="pir-group">
                            <h3>⚙️ System</h3>
                            <div class="pir-row">
                                <div class="pir-field"><label>MEMORY FILE PATH</label><input type="text" id="MEMORY_FILE" placeholder="./data/memory.json"></div>
                                <div class="pir-field"><label>LOG LEVEL</label>
                                    <select id="LOG_LEVEL">
                                        <option value="INFO">INFO</option>
                                        <option value="DEBUG">DEBUG</option>
                                        <option value="WARNING">WARNING</option>
                                        <option value="ERROR">ERROR</option>
                                    </select>
                                </div>
                            </div>
                            <div class="pir-row">
                                <div class="pir-field"><label>DNN WEIGHTS PATH</label><input type="text" id="DNN_WEIGHTS_PATH" placeholder="./data/dnn_weights.pt"></div>
                                <div class="pir-field"><label>DASHBOARD PORT</label><input type="number" id="DASHBOARD_PORT" placeholder="7860"></div>
                            </div>
                            <div class="pir-row">
                                <div class="pir-field"><label>API PORT</label><input type="number" id="API_PORT" placeholder="8000"></div>
                                <div class="pir-field"></div>
                            </div>
                        </div>

                        <!-- Action Bar -->
                        <div class="pir-action-bar">
                            <button type="button" class="pir-btn-secondary" id="btn-reset">🔄 Reset to Defaults</button>
                            <button type="button" class="pir-btn-secondary" id="btn-validate">✅ Validate Only</button>
                            <button type="button" class="pir-btn-secondary" id="btn-export">📤 Export Settings</button>
                            <button type="button" class="pir-btn-secondary" id="btn-import-env">📂 Import .env</button>
                            <input type="file" id="env-file-input" accept=".env,text/plain" style="display:none">
                            <button type="submit" class="pir-btn-primary">💾 Save & Apply</button>
                        </div>
                        <div id="pir-status-msg"></div>
                    </form>
                </div>

                <script>
                    const API_BASE = ""; // Relative path — same origin

                    // All field IDs that map 1-to-1 with DEFAULTS keys in dashboard.py
                    const SCALAR_FIELDS = [
                        "OPENAI_API_KEY", "ANTHROPIC_API_KEY",
                        "PUSHOVER_USER", "PUSHOVER_TOKEN",
                        "MODAL_TOKEN_ID", "MODAL_TOKEN_SECRET",
                        "SCANNER_MODEL", "FRONTIER_MODEL", "MESSAGING_MODEL",
                        "ENSEMBLE_WEIGHTS",
                        "CHROMA_DB_PATH", "EMBEDDING_MODEL",
                        "PUSHOVER_SOUND", "NOTIFICATION_TITLE",
                        "MEMORY_FILE", "LOG_LEVEL", "DNN_WEIGHTS_PATH"
                    ];
                    // Slider fields — also need to update the display span
                    const SLIDER_FIELDS = [
                        { id: "DEAL_THRESHOLD",      display: "deal-thresh-val",    isInt: true },
                        { id: "SCAN_INTERVAL_MINUTES", display: "scan-interval-val", isInt: true },
                        { id: "CHROMA_RESULTS",      display: "chroma-results-val", isInt: true },
                        { id: "RAG_MAX_POINTS",      display: "rag-max-val",        isInt: true },
                        { id: "NOTIF_MIN_INTERVAL",  display: "notif-interval-val", isInt: true },
                        { id: "MAX_DEALS_PER_SCAN",  display: "max-deals-val",      isInt: true },
                        { id: "DASHBOARD_PORT",      display: null,                 isInt: true },
                        { id: "API_PORT",            display: null,                 isInt: true }
                    ];

                    // Defaults used by Reset to Defaults
                    const FIELD_DEFAULTS = {
                        OPENAI_API_KEY: "", ANTHROPIC_API_KEY: "",
                        PUSHOVER_USER: "", PUSHOVER_TOKEN: "",
                        MODAL_TOKEN_ID: "", MODAL_TOKEN_SECRET: "",
                        DEAL_THRESHOLD: 50, SCAN_INTERVAL_MINUTES: 5,
                        SCANNER_MODEL: "gpt-4o-mini", FRONTIER_MODEL: "gpt-4o",
                        MESSAGING_MODEL: "claude-3-5-sonnet-20241022",
                        ENSEMBLE_WEIGHTS: "0.8, 0.1, 0.1",
                        CHROMA_DB_PATH: "./data/products_vectorstore",
                        EMBEDDING_MODEL: "sentence-transformers/all-MiniLM-L6-v2",
                        CHROMA_RESULTS: 5, RAG_MAX_POINTS: 1000,
                        PUSHOVER_SOUND: "pushover",
                        NOTIFICATION_TITLE: "The Price Is Right Alert",
                        NOTIF_MIN_INTERVAL: 5,
                        RSS_FEEDS: "https://www.dealnews.com/rss.html\nhttps://feeds.feedburner.com/techbargains\nhttps://slickdeals.net/newsearch.php?mode=frontpage&searcharea=deals&searchin=first&rss=1",
                        MAX_DEALS_PER_SCAN: 50,
                        MEMORY_FILE: "./data/memory.json", LOG_LEVEL: "INFO",
                        DNN_WEIGHTS_PATH: "./data/dnn_weights.pt",
                        DASHBOARD_PORT: 7860, API_PORT: 8000
                    };

                    // ── Helpers ────────────────────────────────────────────────────────
                    function setField(id, value) {
                        const el = document.getElementById(id);
                        if (!el) return;
                        // Use native setter to bypass React/framework value tracking
                        const nativeSetter = Object.getOwnPropertyDescriptor(
                            el.tagName === 'SELECT' ? HTMLSelectElement.prototype :
                            HTMLInputElement.prototype, 'value'
                        );
                        if (nativeSetter && nativeSetter.set) {
                            nativeSetter.set.call(el, value);
                        } else {
                            el.value = value;
                        }
                        // Dispatch events so the browser registers the change visually
                        el.dispatchEvent(new Event('input',  { bubbles: true }));
                        el.dispatchEvent(new Event('change', { bubbles: true }));
                        // Sync slider display span if present
                        const sf = SLIDER_FIELDS.find(s => s.id === id);
                        if (sf && sf.display) {
                            const span = document.getElementById(sf.display);
                            if (span) span.textContent = value;
                        }
                    }

                    function collectData() {
                        const data = {};
                        // Scalar fields — trim whitespace
                        SCALAR_FIELDS.forEach(f => {
                            const el = document.getElementById(f);
                            if (el) data[f] = el.value.trim();
                        });
                        // Slider / numeric fields
                        SLIDER_FIELDS.forEach(sf => {
                            const el = document.getElementById(sf.id);
                            if (el) data[sf.id] = sf.isInt ? parseInt(el.value, 10) : parseFloat(el.value);
                        });
                        // RSS feeds — trim each line, drop blanks
                        const rssEl = document.getElementById("RSS_FEEDS");
                        if (rssEl) {
                            data["RSS_FEEDS"] = rssEl.value
                                .split("\n")
                                .map(l => l.trim())
                                .filter(l => l !== "");
                        }
                        return data;
                    }

                    function showMsg(text, cls) {
                        const msg = document.getElementById("pir-status-msg");
                        msg.textContent = text;
                        msg.className = cls;
                        msg.style.display = "block";
                        if (cls === "pir-success") setTimeout(() => msg.style.display = "none", 5000);
                    }

                    // ── Load settings from /settings ──────────────────────────────────
                    async function loadPirSettings() {
                        try {
                            const res = await fetch(API_BASE + "/settings");
                            if (!res.ok) return;
                            const data = await res.json();
                            // Scalar fields
                            SCALAR_FIELDS.forEach(f => {
                                if (data[f] !== undefined) setField(f, data[f]);
                            });
                            // Slider fields
                            SLIDER_FIELDS.forEach(sf => {
                                if (data[sf.id] !== undefined) setField(sf.id, data[sf.id]);
                            });
                            // RSS feeds — array → newline-separated
                            if (data["RSS_FEEDS"] !== undefined) {
                                const rssEl = document.getElementById("RSS_FEEDS");
                                if (rssEl) {
                                    rssEl.value = Array.isArray(data["RSS_FEEDS"])
                                        ? data["RSS_FEEDS"].join("\n")
                                        : String(data["RSS_FEEDS"]).trim();
                                }
                            }
                            // Re-apply current key visibility state after load
                            const toggle = document.getElementById('show-keys-toggle');
                            toggleKeyVisibility(toggle ? toggle.checked : false);
                        } catch (e) {
                            console.error("Failed to load settings:", e);
                        }
                    }

                    // ── Save settings to /settings ────────────────────────────────────
                    async function savePirSettings() {
                        const btn = document.querySelector(".pir-btn-primary");
                        btn.textContent = "💾 Saving...";
                        btn.disabled = true;
                        try {
                            const res = await fetch(API_BASE + "/settings", {
                                method: "POST",
                                headers: { "Content-Type": "application/json" },
                                body: JSON.stringify(collectData())
                            });
                            if (res.ok) {
                                showMsg("✅ Settings saved! All agents will use the new values immediately.", "pir-success");
                            } else {
                                const err = await res.text();
                                showMsg("❌ Save failed (HTTP " + res.status + "): " + err, "pir-error");
                            }
                        } catch (e) {
                            showMsg("❌ Network error: " + e.message, "pir-error");
                        } finally {
                            btn.textContent = "💾 Save & Apply";
                            btn.disabled = false;
                        }
                    }

                    // ── Reset to Defaults ─────────────────────────────────────────────
                    function resetToDefaults() {
                        if (!confirm("Reset all settings to factory defaults? Unsaved changes will be lost.")) return;
                        Object.entries(FIELD_DEFAULTS).forEach(([k, v]) => {
                            if (k === "RSS_FEEDS") {
                                const el = document.getElementById(k);
                                if (el) el.value = v;
                            } else {
                                setField(k, v);
                            }
                        });
                        showMsg("⚠️ Defaults loaded. Click Save & Apply to persist.", "pir-warn");
                    }

                    // ── Validate Only ─────────────────────────────────────────────────
                    function validateOnly() {
                        const data = collectData();
                        const errors = [];
                        if (!data.OPENAI_API_KEY) errors.push("OpenAI API Key is empty");
                        if (!data.ANTHROPIC_API_KEY) errors.push("Anthropic API Key is empty");
                        const weights = data.ENSEMBLE_WEIGHTS.split(",").map(w => parseFloat(w.trim()));
                        const wSum = weights.reduce((a, b) => a + b, 0);
                        if (Math.abs(wSum - 1.0) > 0.01) errors.push("Ensemble weights must sum to 1.0 (current: " + wSum.toFixed(3) + ")");
                        if (data.DEAL_THRESHOLD < 1 || data.DEAL_THRESHOLD > 90) errors.push("Deal threshold must be 1-90");
                        if (errors.length === 0) {
                            showMsg("✅ Validation passed. All required fields are present and values are in range.", "pir-success");
                        } else {
                            showMsg("❌ Validation errors:\n" + errors.join("\n"), "pir-error");
                        }
                    }

                    // ── Export Settings ───────────────────────────────────────────────
                    function exportSettings() {
                        const data = collectData();
                        // Mask secrets before export
                        const safe = Object.assign({}, data);
                        ["OPENAI_API_KEY","ANTHROPIC_API_KEY","PUSHOVER_USER","PUSHOVER_TOKEN","MODAL_TOKEN_ID","MODAL_TOKEN_SECRET"]
                            .forEach(k => { if (safe[k]) safe[k] = safe[k].substring(0, 4) + "****"; });
                        const blob = new Blob([JSON.stringify(safe, null, 2)], { type: "application/json" });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement("a");
                        a.href = url;
                        a.download = "priceisright_settings_" + new Date().toISOString().slice(0,10) + ".json";
                        a.click();
                        URL.revokeObjectURL(url);
                        showMsg("✅ Settings exported (API keys masked for safety).", "pir-success");
                    }

                    // ── Test API connections ──────────────────────────────────────────
                    async function testApi(service) {
                        const statusEl = document.getElementById("test-" + service + "-status");
                        statusEl.textContent = "⏳ Testing...";
                        statusEl.className = "pir-test-status";
                        try {
                            const res = await fetch(API_BASE + "/test-api/" + service, {
                                method: "POST",
                                headers: { "Content-Type": "application/json" },
                                body: JSON.stringify(collectData())
                            });
                            const result = await res.json();
                            if (result.ok) {
                                statusEl.textContent = "✅ " + (result.message || "Connected");
                                statusEl.className = "pir-test-status ok";
                            } else {
                                statusEl.textContent = "⚠️ " + (result.message || "Failed");
                                statusEl.className = "pir-test-status err";
                            }
                        } catch (e) {
                            statusEl.textContent = "❌ " + e.message;
                            statusEl.className = "pir-test-status err";
                        }
                    }

                    // ── Show/Hide API key visibility ────────────────────────────────
                    function toggleKeyVisibility(show) {
                        document.querySelectorAll('.pir-secret-field').forEach(el => {
                            if (show) {
                                el.style.webkitTextSecurity = 'none';
                                el.style.textSecurity = 'none';
                                el.style.fontFamily = "'JetBrains Mono', monospace";
                            } else {
                                el.style.webkitTextSecurity = 'disc';
                                el.style.textSecurity = 'disc';
                                el.style.fontFamily = "'password', monospace";
                            }
                        });
                    }
                    // Apply masking on load
                    document.addEventListener('DOMContentLoaded', () => toggleKeyVisibility(false));
                    setTimeout(() => toggleKeyVisibility(false), 500);

                    // ── Import .env file ──────────────────────────────────────────────
                    function importEnvFile(input) {
                        const file = input.files[0];
                        if (!file) return;
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            const lines = e.target.result.split("\n");
                            const parsed = {};
                            lines.forEach(line => {
                                line = line.trim();
                                if (!line || line.startsWith("#")) return; // skip comments/blanks
                                const eqIdx = line.indexOf("=");
                                if (eqIdx < 1) return;
                                const key = line.substring(0, eqIdx).trim();
                                let val = line.substring(eqIdx + 1).trim();
                                // Strip surrounding quotes if present
                                if ((val.startsWith('"') && val.endsWith('"')) ||
                                    (val.startsWith("'") && val.endsWith("'"))) {
                                    val = val.slice(1, -1);
                                }
                                parsed[key] = val;
                            });
                            // Map .env keys to form field IDs
                            const ENV_MAP = {
                                OPENAI_API_KEY:    "OPENAI_API_KEY",
                                ANTHROPIC_API_KEY: "ANTHROPIC_API_KEY",
                                PUSHOVER_USER:     "PUSHOVER_USER",
                                PUSHOVER_TOKEN:    "PUSHOVER_TOKEN",
                                MODAL_TOKEN_ID:    "MODAL_TOKEN_ID",
                                MODAL_TOKEN_SECRET:"MODAL_TOKEN_SECRET",
                                DEAL_THRESHOLD:    "DEAL_THRESHOLD",
                                SCAN_INTERVAL_MINUTES: "SCAN_INTERVAL_MINUTES",
                                SCANNER_MODEL:     "SCANNER_MODEL",
                                FRONTIER_MODEL:    "FRONTIER_MODEL",
                                MESSAGING_MODEL:   "MESSAGING_MODEL",
                                CHROMA_DB_PATH:    "CHROMA_DB_PATH",
                                EMBEDDING_MODEL:   "EMBEDDING_MODEL",
                                MEMORY_FILE:       "MEMORY_FILE",
                                LOG_LEVEL:         "LOG_LEVEL",
                                DNN_WEIGHTS_PATH:  "DNN_WEIGHTS_PATH",
                                DASHBOARD_PORT:    "DASHBOARD_PORT",
                                API_PORT:          "API_PORT",
                                RSS_FEED_URLS:     "RSS_FEEDS",  // .env uses RSS_FEED_URLS
                            };
                            let count = 0;
                            Object.entries(parsed).forEach(([envKey, envVal]) => {
                                const fieldId = ENV_MAP[envKey];
                                if (!fieldId) return;
                                if (fieldId === "RSS_FEEDS") {
                                    // Comma-separated in .env → newline-separated in form
                                    const el = document.getElementById(fieldId);
                                    if (el) { el.value = envVal.replace(/,/g, "\n"); count++; }
                                } else {
                                    setField(fieldId, envVal);
                                    count++;
                                }
                            });
                            showMsg("✅ Imported " + count + " value(s) from .env — review values below, then click Save & Apply.", "pir-success");
                            // Auto-show keys so user can verify imported values
                            const toggle = document.getElementById('show-keys-toggle');
                            if (toggle) { toggle.checked = true; toggleKeyVisibility(true); }
                            // Reset file input so same file can be re-imported
                            input.value = "";
                        };
                        reader.readAsText(file);
                    }

                    // ── Wire all event listeners (no inline onclick/onchange) ───────────
                    function wirePirSettings() {
                        // Form submit → save
                        const form = document.getElementById('pir-settings-form-element');
                        if (form) form.addEventListener('submit', e => { e.preventDefault(); savePirSettings(); });

                        // Save & Apply button (primary)
                        const saveBtn = document.querySelector('.pir-btn-primary');
                        if (saveBtn) saveBtn.addEventListener('click', savePirSettings);

                        // Show/hide keys toggle
                        const keyToggle = document.getElementById('show-keys-toggle');
                        if (keyToggle) keyToggle.addEventListener('change', () => toggleKeyVisibility(keyToggle.checked));

                        // Test buttons via data-test attribute
                        document.querySelectorAll('[data-test]').forEach(btn => {
                            btn.addEventListener('click', () => testApi(btn.getAttribute('data-test')));
                        });

                        // Sliders via data-display attribute
                        document.querySelectorAll('input[type=range][data-display]').forEach(slider => {
                            const displayId = slider.getAttribute('data-display');
                            slider.addEventListener('input', () => {
                                const span = document.getElementById(displayId);
                                if (span) span.textContent = slider.value;
                            });
                        });

                        // Action bar buttons
                        const btnReset = document.getElementById('btn-reset');
                        if (btnReset) btnReset.addEventListener('click', resetToDefaults);

                        const btnValidate = document.getElementById('btn-validate');
                        if (btnValidate) btnValidate.addEventListener('click', validateOnly);

                        const btnExport = document.getElementById('btn-export');
                        if (btnExport) btnExport.addEventListener('click', exportSettings);

                        const btnImport = document.getElementById('btn-import-env');
                        const fileInput = document.getElementById('env-file-input');
                        if (btnImport && fileInput) {
                            btnImport.addEventListener('click', () => fileInput.click());
                            fileInput.addEventListener('change', () => importEnvFile(fileInput));
                        }

                        // Load settings after wiring
                        loadPirSettings();
                    }

                    // ── Auto-init: retry until DOM elements exist (Gradio renders async) ───
                    let _loadRetries = 0;
                    const _loadTimer = setInterval(() => {
                        const el = document.getElementById("OPENAI_API_KEY");
                        if (el) { wirePirSettings(); clearInterval(_loadTimer); }
                        if (++_loadRetries > 40) clearInterval(_loadTimer);
                    }, 250);
                </script>
                """)

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

        # ── Event Wiring ────────────────────────────────────────────────────────────────
        scan_btn.click(
            fn=None,
            js="""
            async function() {
                try {
                    await fetch('/scan', { method: 'POST' });
                } catch (e) {
                    console.error('Failed to start scan:', e);
                }
            }
            """
        )



        refresh_rag_btn.click(
            fn=lambda: gr.update(value=build_rag_html(state["rag_stats"])),
            outputs=[rag_html]
        )

    return app
