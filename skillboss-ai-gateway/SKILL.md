---
name: skillboss-ai-gateway
description: Unified AI gateway providing one API key for 100+ AI services. Use when accessing multiple AI models (Claude, GPT, Gemini), generating images/videos, synthesizing voice, or scraping websites. Triggers on mentions of switching models, image generation, video creation, or multi-API access.
model: sonnet
---

# SkillBoss AI Gateway

Access 100+ AI services through a single, OpenAI-compatible API. Stop juggling multiple API keys.

## When to Use

- User needs to switch between Claude, GPT, Gemini, DeepSeek models
- Generating images with DALL-E, Midjourney, Flux, Stable Diffusion
- Creating videos with Runway, Kling, Veo 2
- Voice synthesis with ElevenLabs or OpenAI TTS
- Web scraping with Firecrawl or Jina AI
- User mentions "multiple AI providers", "unified API", or "one API key"

## Available Services

| Category | Services |
|----------|----------|
| 🧠 Language Models | Claude Opus 4.6, GPT-5, Gemini 3 Pro, DeepSeek R1 |
| 🎨 Image Generation | DALL-E, Midjourney, Flux, Stable Diffusion |
| 🎬 Video Generation | Runway Gen-4, Kling, Veo 2 |
| 🎤 Voice | ElevenLabs, OpenAI TTS/STT |
| 🌐 Web Scraping | Firecrawl, Jina AI |
| 💳 Business | Stripe, Resend |

## Instructions

### MCP Server Setup (Claude Code / Cursor / Windsurf)

Add to MCP settings:

```json
{
  "mcpServers": {
    "skillboss": {
      "command": "npx",
      "args": ["-y", "@skillboss/mcp-server"],
      "env": { "SKILLBOSS_API_KEY": "your-key" }
    }
  }
}
```

### OpenAI SDK Usage

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-skillboss-key",
    base_url="https://api.heybossai.com/v1"
)

# Use any model
response = client.chat.completions.create(
    model="claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Image Generation

```python
response = client.images.generate(
    model="flux-1.1-pro",
    prompt="A futuristic city at sunset",
    size="1024x1024"
)
```

## Get Your API Key

Visit https://skillboss.co/dashboard

## Resources

- Website: https://skillboss.co
- Docs: https://skillboss.co/docs
- GitHub: https://github.com/heeyo-life/skillboss-mcp
- npm: https://www.npmjs.com/package/@skillboss/mcp-server
