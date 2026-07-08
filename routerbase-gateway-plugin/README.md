# RouterBase Gateway Plugin

Skills for integrating OpenAI-compatible AI apps with [routerbase](https://routerbase.com/) model routing, fallback design, safe API key handling, and media-generation workflows.

**Version:** 1.0.0

---

## Skills

### 1. routing-with-routerbase

**Activates when you say:**
- "Route this OpenAI client through RouterBase"
- "Choose RouterBase models and fallbacks"
- "Add RouterBase image or video generation"

**What it does:**
- Migrates OpenAI-compatible SDK configuration to `https://routerbase.com/v1`
- Keeps RouterBase keys server-side with environment variables
- Plans primary and fallback model routing for chat, embeddings, image, video, audio, and speech workflows
- Adds production checks for retries, streaming, JSON mode, tool calling, and async media jobs

---

## Installation

Add the marketplace, then install the RouterBase gateway plugin:

```bash
/plugin marketplace add mhattingpete/claude-skills-marketplace
/plugin install routerbase-gateway-skills@mhattingpete-claude-skills
```

---

## Source

- [routerbase](https://routerbase.com/)
- [RouterBase agent skills](https://github.com/zenlee123/routerbase-agent-skills)

## Author

**zenlee123**
