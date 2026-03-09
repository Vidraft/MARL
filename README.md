<div align="center">

# MARL — Model-Agnostic Runtime Middleware for LLMs

**The 3rd approach after fine-tuning & RAG — restructure how LLMs reason at runtime, not their weights.**

[![PyPI](https://img.shields.io/pypi/v/marl-middleware?color=6366f1&label=PyPI)](https://pypi.org/project/marl-middleware/)
[![License](https://img.shields.io/badge/License-Apache%202.0-0d9488)](LICENSE)
[![HuggingFace](https://img.shields.io/badge/🤗%20Demo-HuggingFace-ff9d00)](https://huggingface.co/spaces/VIDraft/MARL)
[![FINAL Bench](https://img.shields.io/badge/🏆%20FINAL%20Bench-Global%20%235-16a34a)](https://huggingface.co/spaces/FINAL-Bench/Leaderboard)

`pip install marl-middleware` · `docker run vidraft/marl`

**Multi-stage multi-agent reasoning pipeline that works with any LLM.**

</div>

---

## What is MARL?

MARL (Model-Agnostic Runtime Middleware) is a **multi-stage multi-agent reasoning pipeline that decomposes a single LLM call into multiple independent expert roles**.

The two dominant approaches to improving LLM quality — **fine-tuning** and **RAG** — each have fundamental limitations. Fine-tuning requires millions of dollars in GPU costs and weeks of training. RAG supplements external knowledge but cannot improve the model's reasoning ability itself.

MARL is the **3rd approach**: it **redesigns the structure of reasoning at runtime without touching model weights**. It works with any LLM — GPT-5.4, Claude Opus, Gemini, DeepSeek, Llama, or local open-source models — with a single line of code. Switch models freely; MARL's effect remains.

```
┌─ Your App ─────────────────────────────────────────┐
│  OpenClaw / Cursor / Custom App / Any LLM Client    │
│  client = OpenAI(base_url="http://MARL:8080/v1")    │
└────────────────────┬───────────────────────────────┘
                     │ HTTP (OpenAI API format)
                     ▼
┌─ MARL Middleware ──────────────────────────────────┐
│  Multi-stage Multi-agent Reasoning Pipeline         │
│  9 Emergence Engines · 70%+ Hallucination Reduction │
│  FINAL Bench: MA=0.694 vs ER=0.302                  │
└────────────────────┬───────────────────────────────┘
                     │ API calls
                     ▼
┌─ Any LLM ──────────────────────────────────────────┐
│  GPT-5.4 · Claude · Gemini · DeepSeek · Ollama …   │
└────────────────────────────────────────────────────┘
```

---

## Why MARL?

### The Problem: LLMs answer confidently even when wrong — and can't stop themselves

**Metacognition** is the ability of an AI to recognize that its own answer might be wrong and self-correct. Research from **FINAL Bench**, the world's first AI metacognition benchmark, confirmed that even the most advanced models — GPT-5.2, Claude Opus 4.6, Gemini 3 Pro — have critically insufficient self-correction capabilities.

Due to their autoregressive architecture, once an LLM begins generating a response, earlier tokens determine later ones. The model cannot pause mid-generation to say "I was wrong" and change direction.

### The Solution: Multi-stage Independent Expert Pipeline

MARL routes a single question through multiple independent expert agents in sequence. Instead of one chef handling everything alone, MARL assigns a recipe planner to design the optimal approach, a head chef to execute, a quality inspector to audit, and a Michelin judge to deliver the final verdict.

Each agent carries a distinct role and perspective — **hypothesis exploration → core solving → consistency auditing → adversarial verification → metacognitive synthesis** — producing emergent reasoning and self-correction capabilities that no single model call can achieve.

This architecture resolves two fundamental LLM limitations:

- **Emergent reasoning**: New perspectives arise through multi-stage interaction that never surface in a single model call.
- **Structural self-correction**: While a standard LLM cannot reverse course mid-generation, MARL's adversarial verification stage re-examines the draft for errors, and the final synthesis stage produces an entirely new answer incorporating all corrections.

---

## Results

| Metric | Value |
|--------|-------|
| Hallucination reduction | **70%+** (FINAL Bench verified) |
| Self-correction contribution | **94.8%** (Error Recovery drives 94.8% of total improvement) |
| FINAL Bench MA vs ER | **0.694 vs 0.302** |
| FINAL Bench Dataset ranking | **HuggingFace Global Top 5** |
| Monthly Active Users (MAU) | **2M+** |
| Public AI models & tools | **1,500+** |
| HuggingFace STAR AI | **2024 Top 12 (only Korean company selected)** |
| FACTS Grounding | **Google DeepMind Leaderboard #2 worldwide** |

---

## Installation

### pip (Linux x86_64 / Python 3.12)

```bash
pip install marl-middleware
```

### Docker (All OS — Mac · Windows · Linux)

```bash
docker run -p 8080:8080 vidraft/marl
```

### HuggingFace Space (No install required)

> [https://huggingface.co/spaces/VIDraft/MARL](https://huggingface.co/spaces/VIDraft/MARL)

---

## Usage

### Python SDK

```python
from marl import Marl, MarlConfig

# OpenAI
ml = Marl.from_openai("sk-...", config=MarlConfig(
    mode="emergence", emergence_type="create"
))
result = ml.run("Generate 10 movie loglines never seen before")
print(result.answer)

# Anthropic
ml = Marl.from_anthropic("sk-ant-...", model="claude-sonnet-4-20250514")

# Ollama (local)
ml = Marl.from_ollama("llama3.1")

# Groq (free)
ml = Marl.from_openai_compatible(
    "https://api.groq.com/openai/v1", "gsk-...", "openai/gpt-oss-120b"
)

# Any OpenAI-compatible API (DeepSeek, xAI, Friendli, etc.)
ml = Marl.from_openai_compatible("https://api.deepseek.com/v1", "key", "deepseek-v3")
```

### 1-Line Integration (Any LLM App)

Add `base_url` — **one line** — and every call passes through the MARL pipeline:

```python
# Before
client = OpenAI(api_key="sk-...")

# After — just add base_url
client = OpenAI(api_key="sk-...", base_url="http://localhost:8080/v1")
```

---

## Works With Every LLM

MARL is **model-agnostic** middleware. It works instantly with any LLM that supports the OpenAI API format. You are never locked into a specific provider — when a better model launches, switch immediately.

```
OpenAI        — GPT-5.4, GPT-5.2, GPT-4.1, o4-mini, GPT-OSS-120B
Anthropic     — Claude Opus 4.6, Sonnet 4.6, Haiku 4.5
Google        — Gemini 3.1 Pro, Gemini 3 Flash, Gemini 2.5 Pro/Flash
DeepSeek      — DeepSeek-V3, DeepSeek-R1, R2
xAI           — Grok-4, Grok-3
Groq          — gpt-oss-120b, Llama 4, DeepSeek-R1, QwQ-32b (free)
Meta          — Llama 4 Scout/Maverick
Alibaba       — Qwen3.5 series
Ollama        — Any local open-source model
Custom        — Any OpenAI-compatible endpoint
```

> This list is illustrative. **MARL works with any LLM supporting the OpenAI API format — zero code changes required.**

---

## 9 Emergence Engines

Beyond the default reasoning enhancement (Insight mode), MARL includes **9 specialized emergence engines**. Each engine is powered by a proprietary knowledge matrix and emergence rules designed to generate domain-specific ideas that a single LLM cannot produce alone.

| Engine | Strengths |
|--------|-----------|
| 🔧 **Invent** | Technology fusion–based invention. Cross-applies TRIZ principles, bio-inspired patterns, and contradiction resolution strategies to generate patent-level concepts. |
| ✨ **Create** | Universal creative engine. Drives idea generation through cliché inversion, paradox engines, genre fusion, sensory collision, and cultural cross-pollination. |
| 🍳 **Recipe** | Culinary emergence. Crosses cooking methods, textures, architectural structures, and flavor grammar to develop novel dish concepts with built-in taste chemistry validation. |
| 💊 **Pharma** | Drug & compound ideation. Drug repositioning, mechanism crossing, delivery innovation, multi-target design, and scaffold hopping for novel therapeutic concepts. |
| 🧬 **Genomics** | Genomics & bio emergence. Pathway crosstalk discovery, synthetic lethality exploration, phenotype bridging, and technology platform transfer. |
| 🧪 **Chemistry** | Materials & chemistry emergence. Achieving contradictory properties simultaneously, nano↔macro scale shifting, biomimicry, and waste-to-value transformation. |
| 🌍 **Ecology** | Environmental & conservation emergence. Conservation model transfer, species protection network effects, threat-to-resource inversion, and ecosystem service stacking. |
| ⚖️ **Law** | Legal & regulatory emergence. Cross-jurisdiction framework transplantation, regulatory mechanism inversion, tech-law collision resolution, and legal instrument innovation. |
| 📄 **Document** | Report & document engine. Metacognitive document generation based on structured writing principles and policy dilemma frameworks. |

### Mode Switching

Append `::mode` to any model name to switch engines:

```
model="gpt-5.4"             →  🔬 Insight (default — fact-check · strategy)
model="gpt-5.4::invent"     →  🔧 Invent
model="gpt-5.4::create"     →  ✨ Create
model="gpt-5.4::recipe"     →  🍳 Recipe
model="gpt-5.4::pharma"     →  💊 Pharma
model="gpt-5.4::genomics"   →  🧬 Genomics
model="gpt-5.4::chemistry"  →  🧪 Chemistry
model="gpt-5.4::ecology"    →  🌍 Ecology
model="gpt-5.4::law"        →  ⚖️ Law
model="gpt-5.4::document"   →  📄 Document
```

> Replace `gpt-5.4` with any model name you prefer.

---

## OpenClaw Integration

MARL serves as **the brain for OpenClaw**. Before OpenClaw acts (emails, files, scheduling), MARL thinks deeply first.

```bash
# Step 1: Install MARL locally
docker run -p 8080:8080 vidraft/marl

# Step 2: Set OpenClaw config.json
{
  "llm": {
    "baseURL": "http://localhost:8080/v1",
    "model": "gpt-5.4::create"
  }
}

# Step 3: Chat naturally
"Analyze this with MARL"
"Use MARL pharma mode for drug repositioning candidates"
```

---

## IP Protection

MARL's core reasoning engine — the multi-stage pipeline, weighted attention matrices, and agent prompts — is delivered as **compiled binaries (.so)** to protect proprietary technology. At the same time, all interface code needed for installation, testing, configuration, and API integration is openly available, so anyone can try MARL immediately and integrate it into their own environment.

---

## About VIDRAFT

**VIDRAFT** is an AI startup founded in 2024 with the goal of developing True-AGI by 2030. Based at **Seoul AI Hub**, the team focuses on LLM metacognition enhancement and multi-agent reasoning technology.

| Achievement | Detail |
|-------------|--------|
| FINAL Bench | World's first AI metacognition benchmark · HuggingFace Global Top 5 dataset |
| FINAL Bench Leaderboard | HuggingFace "Spaces of the Week" selected |
| HuggingFace Heatmap Leaderboard | Global #4 |
| STAR AI Top 12 | 2024 selected (only Korean company) |
| Medical AI | Google DeepMind FACTS Grounding Leaderboard #2 worldwide |
| MAU | 2M+ |
| Cumulative visitors | 30M+ |
| Public AI models & tools | 1,500+ |
| NIPA H200 GPU×8 | National AI infrastructure grant recipient |
| Seoul AI Hub | Resident company |
| NH Open Innovation | 2025 selected |
| Press | Seoul Shinmun, Asia Economy, IT Chosun, and more |

---

## Roadmap

- **MARL Enterprise Edition** — Private deployment, custom pipelines, SLA support (H1 2026)
- **Academic publication** — FINAL Bench–based validation paper for international journal
- **US market entry** — Silicon Valley partnership program
- **OpenClaw ClawHub** — Skill registration for the 247K+ community

---

## Links

| | |
|---|---|
| 🌐 Website | [https://vidraft.net](https://vidraft.net) |
| 🤗 MARL Demo | [https://huggingface.co/spaces/VIDraft/MARL](https://huggingface.co/spaces/VIDraft/MARL) |
| 🏆 FINAL Bench | [https://huggingface.co/spaces/FINAL-Bench/Leaderboard](https://huggingface.co/spaces/FINAL-Bench/Leaderboard) |
| 📦 PyPI | [https://pypi.org/project/marl-middleware/](https://pypi.org/project/marl-middleware/) |
| ✉️ Contact | arxivgpt@gmail.com (Minsik KIM, CEO) |

---

## License

Apache License 2.0 — Copyright 2025-2026 VIDRAFT / Vidraft Inc.

---

<div align="center">

**MARL** · Model-Agnostic Runtime Middleware for LLMs

*"Don't change the model. Change how the model thinks."*

— Minsik KIM, CEO of VIDRAFT

</div>
