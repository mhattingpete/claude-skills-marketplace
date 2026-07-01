# Xquik Data Skills Plugin

Skills for integrating Xquik REST API and remote MCP workflows into agent and application projects.

## Skills

### xquik-integrating

**Activates when you say:**
- "Set up Xquik MCP"
- "Use Xquik for tweet search"
- "Build with the Xquik REST API"
- "Export X followers with Xquik"

**What it does:**
- Selects REST API or remote MCP based on the task
- Checks the live OpenAPI spec or MCP manifest before endpoint-specific work
- Applies approval gates for private reads, writes, persistent monitors, webhooks, and bulk jobs
- Keeps API keys in the host secret store

## Installation

```bash
/plugin marketplace add mhattingpete/claude-skills-marketplace/xquik-data-skills-plugin
```
