# AgentFeeds Plugin

Ready-to-read context cache for personal agents.

AgentFeeds keeps changing context warm on disk — calendars, inboxes, reminders, GitHub, RSS/news, weather, notes, dashboards, and approved local sources — so Claude can read compact local stream state before scanning skills, searching the web, re-fetching APIs, or asking the user to repeat context.

## Skill Included

### agentfeeds

**Purpose:** Give Claude a local, refreshable context cache for fresh state that should not live in long-term memory.

**Activates when you say:**

```text
Set up AgentFeeds with useful safe default streams for this agent.
```

```text
What fresh context does AgentFeeds already have available?
```

```text
Use AgentFeeds first. What should I pay attention to today?
```

```text
Subscribe AgentFeeds to my calendar, reminders, unread mail, GitHub activity, and a few AI news sources.
```

```text
Before searching the web, check AgentFeeds for relevant cached context.
```

**What it does:**

- Discovers reusable stream templates such as macOS Calendar/Mail/Reminders/Notes/Messages, RSS, GitHub, weather, local files, and approved local commands.
- Creates concrete subscriptions and keeps them refreshed in the background.
- Emits a compact stream brief for session-start context.
- Lets Claude search/read local stream state before expensive external lookups.
- Keeps volatile context out of long-term memory.

## Installation

Install from this marketplace:

```bash
/plugin marketplace add mhattingpete/claude-skills-marketplace/agentfeeds-plugin
```

Then ask Claude:

```text
Set up AgentFeeds with useful safe default streams for this agent.
```

The skill will run its bundled setup script when needed:

```bash
python3 scripts/setup.py
```

## Notes

- Requires shell access and Python 3.11+.
- Background polling supports macOS, Linux, FreeBSD, and WSL-style POSIX environments.
- macOS personal sources may ask for Calendar, Reminders, Automation, Messages/Mail, or Full Disk Access permissions on first refresh.
- Local command templates are argv-only and require explicit operator approval before execution.

## Feedback Wanted

What is the first local or private source you would want your agent to subscribe to and keep ready — calendar, inbox, GitHub, notes, finance, dashboards, messages, something else?

Repo: https://github.com/verkyyi/agentfeeds
