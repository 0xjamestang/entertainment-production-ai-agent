# 🎬 Entertainment Production AI Agent

**An Autonomous, Production-Ready AI System for Short Drama & Short-Form Video Creation**

---

## Overview

**Entertainment Production AI Agent** is a production-grade, autonomous AI system designed for the **short drama and short-form video industry**.

Unlike generic script-writing tools, this system covers the **entire entertainment production workflow** — from script generation to production planning, visual execution, and post-production guidance — with **engineering-level reliability** and **test-driven guarantees**.

> **It doesn’t just write stories.
> It thinks like a production team.**

---

## What This Agent Does

The agent transforms a high-level creative brief into a **complete, ready-to-shoot production package**.

### ✍️ Script Generation & Polishing

* Genre-aware and platform-optimized scripts
* Strong hooks within the first 3–5 seconds
* Natural, conversational dialogue
* Shootability and cost-awareness validation

### 🎥 Production Breakdown

* Automatic script breakdown into:

  * Characters
  * Locations (INT/EXT, Day/Night)
  * Props, wardrobe, makeup
  * Special requirements (stunts, VFX, vehicles)
* Early cost and feasibility flags

### 🎞 Storyboard & Shot List

* Shot-by-shot storyboard generation
* Detailed shot lists with:

  * Camera framing and movement
  * Visual continuity checks
  * Duration estimates optimized for short-form pacing

### 🎧 Production & Post-Production Advisory

* Actionable filming guidance:

  * Continuity risks
  * Coverage and B-roll suggestions
  * Audio capture best practices
* Editing and delivery guidance:

  * Platform-specific pacing
  * Subtitle and sound recommendations
  * Common revision pitfalls

---

## How It Works

The system is built around an **autonomous development and execution loop** (Ralph Wiggum Loop):

```
Implement → Test → Validate → Iterate
```

* Every component is fully tested before progression
* Any failure triggers an automatic debug–fix–retest cycle
* No feature advances while tests are failing
* All outputs are generated as structured, production-ready assets

**Current Test Coverage:**
✅ 114/114 tests passing (100%)

---

## Example Output

For a sample prompt like:

> *“Generate a 45-second romantic comedy short drama for TikTok, single location, two characters.”*

The system produces:

* Script with hook, scenes, dialogue, and actions
* Production breakdown (CSV / JSON)
* Storyboard with shot-by-shot planning
* Shot list with camera specifications
* Production notes (continuity & coverage)
* Post-production notes (editing & platform delivery)

All outputs are validated and ready for real-world production use.

---

## Project Structure

```text
.
├─ .kiro/                  # Agent specs, tasks, and loop configuration
├─ src/                    # Core system logic
│  ├─ generators/          # Script, breakdown, storyboard, advisory generators
│  ├─ models/              # Strongly-typed domain models
│  ├─ workflow/            # End-to-end production orchestration
│  └─ loop_controller.py   # Autonomous loop engine
├─ tests/                  # Comprehensive test suite
├─ loop/                   # System state & agent prompts
├─ requirements.txt
├─ run_loop.py
└─ README.md
```

---

## Getting Started

### Requirements

* Python 3.10+
* Git
* (Optional) Kiro Agent Runtime

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run a Demo Production

```bash
python demo_production.py
```

### Run the Autonomous Loop

```bash
python run_loop.py
```

---

## Who This Is For

* 🎬 Short drama studios
* 📱 Short-form video creators
* 🎥 Production teams and agencies
* 🧠 Platforms building AI-assisted content pipelines
* 🚀 Teams exploring industrialized content creation

---

## Design Philosophy

* **Production-first**, not demo-first
* **Test-driven creativity**
* **Autonomous iteration over manual prompting**
* **Structured outputs over free-form text**
* **Engineering discipline applied to creative workflows**

---

## Roadmap

* CLI & API interfaces
* Multi-agent roles (Writer / Director / Producer)
* Video generation & editing tool integrations
* Asset management & storage backends
* SaaS-ready deployment architecture

---

## License

MIT.

---

## Contact

Built by **James Tang**
GitHub: [https://github.com/0xjamestang](https://github.com/0xjamestang)

---

> **From idea to shoot-ready plan — automatically.**
