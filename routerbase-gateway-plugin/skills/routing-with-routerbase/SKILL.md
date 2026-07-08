---
name: routing-with-routerbase
description: Integrate OpenAI-compatible AI applications with RouterBase. Use when migrating OpenAI SDK clients to RouterBase, configuring safe server-side API keys, choosing model routing and fallbacks, or adding RouterBase image, video, audio, speech, chat, or embedding workflows.
---

# Routing With RouterBase

Use [routerbase](https://routerbase.com/) as an OpenAI-compatible gateway for model routing across chat, embeddings, image, video, audio, and speech workloads.

## When to Use

- Migrating an OpenAI-compatible SDK or HTTP client to RouterBase.
- Choosing RouterBase model IDs for chat, vision, embeddings, image, video, audio, or speech.
- Designing primary and fallback model routing for cost, latency, quality, or availability.
- Adding RouterBase media generation with sync image calls or async video/audio jobs.
- Reviewing RouterBase API key handling, request logging, retry policy, or smoke tests.

## Instructions

### 1. Classify the request

Identify whether the user needs a new integration, migration, debugging, model selection, fallback planning, media generation, or documentation.

### 2. Keep credentials server-side

Store keys in environment variables or a secret manager:

```bash
ROUTERBASE_API_KEY=your_routerbase_key_here
ROUTERBASE_BASE_URL=https://routerbase.com/v1
```

Never put RouterBase keys in browser code, mobile bundles, public repositories, screenshots, or logs.

### 3. Reuse OpenAI-compatible clients

Change the base URL to `https://routerbase.com/v1`, then choose a RouterBase model ID that matches the workload.

Python:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["ROUTERBASE_API_KEY"],
    base_url="https://routerbase.com/v1",
)

response = client.chat.completions.create(
    model="google/gemini-2.5-flash",
    messages=[{"role": "user", "content": "Write one sentence about model routing."}],
)
print(response.choices[0].message.content)
```

JavaScript:

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.ROUTERBASE_API_KEY,
  baseURL: "https://routerbase.com/v1",
});

const response = await client.chat.completions.create({
  model: "google/gemini-2.5-flash",
  messages: [{ role: "user", content: "Write one sentence about model routing." }],
});
console.log(response.choices[0].message.content);
```

### 4. Verify models and pricing when it matters

If credentials are available, query the live catalog before final production recommendations:

```bash
curl "https://routerbase.com/api/v1/models?task=chat" \
  -H "Authorization: Bearer $ROUTERBASE_API_KEY"
```

Treat example model IDs as starting points unless you verified current availability.

### 5. Design conservative fallbacks

Shortlist one primary model and one or two fallback models with the same modality and similar capability shape. Retry transient network failures, timeouts, `429`, and `5xx`. Do not blindly retry auth failures, invalid model IDs, validation errors, or policy errors.

### 6. Route media by modality

- Image: `POST https://routerbase.com/v1/images/generations`
- Video: `POST https://routerbase.com/v1/videos/generations`
- Speech/audio: `POST https://routerbase.com/v1/audio/speech` or `POST https://routerbase.com/v1/audio/generations`

Treat image generation as synchronous unless current RouterBase docs say otherwise. Treat video and audio jobs as asynchronous: persist task IDs, poll with backoff, support callbacks only with a durable webhook receiver, and store generated assets before retention expiry.

## Output Checklist

- Base URL set to `https://routerbase.com/v1`.
- `ROUTERBASE_API_KEY` stays server-side.
- Model IDs and pricing assumptions are verified or clearly marked as examples.
- Fallback behavior retries only retryable errors.
- Media workflows document sync versus async behavior.
- A smoke test or dry-run validation path is included.
