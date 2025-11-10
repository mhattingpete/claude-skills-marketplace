---
name: technical-doc-creator
description: Create HTML technical documentation with code blocks, API workflows, system architecture diagrams, and syntax highlighting. Use when users request technical documentation, API docs, API references, code examples, or developer documentation.
---

# Technical Documentation Creator

Create comprehensive HTML technical documentation with code examples and API workflows.

## When to Use

- "Create API documentation for [endpoints]"
- "Generate technical docs for [system]"
- "Document API reference"
- "Create developer documentation"

## Components

1. **Overview**: purpose, key features, tech stack
2. **Getting Started**: installation, setup, quick start
3. **API Reference**: endpoints with request/response examples
4. **Code Examples**: syntax-highlighted code blocks
5. **Architecture**: system diagram (SVG)
6. **Workflows**: step-by-step processes

## HTML Structure

```html
<!DOCTYPE html>
<html>
<head>
  <title>[API/System] Documentation</title>
  <style>
    body { font-family: system-ui; max-width: 1000px; margin: 0 auto; }
    pre { background: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 4px; overflow-x: auto; }
    .endpoint { background: #f7fafc; padding: 15px; margin: 10px 0; border-left: 4px solid #4299e1; }
    code { background: #e2e8f0; padding: 2px 6px; border-radius: 3px; }
  </style>
</head>
<body>
  <h1>[System] Documentation</h1>
  <!-- Overview, Getting Started, API Reference, Examples -->
</body>
</html>
```

## API Endpoint Pattern

```html
<div class="endpoint">
  <h3><span style="color: #48bb78;">GET</span> /api/users/{id}</h3>
  <p>Retrieve user by ID</p>

  <h4>Request</h4>
  <pre><code>curl -X GET https://api.example.com/users/123</code></pre>

  <h4>Response</h4>
  <pre><code>{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com"
}</code></pre>
</div>
```

## Code Block Pattern

```html
<pre><code>// Installation
npm install package-name

// Usage
import { feature } from 'package-name';
const result = feature.doSomething();</code></pre>
```

## Workflow

1. Extract API endpoints, methods, parameters
2. Create overview and getting started sections
3. Document each endpoint with examples
4. Add code snippets for common operations
5. Include architecture diagram if relevant
6. Write to `[system]-docs.html`

Use semantic colors for HTTP methods: GET (green), POST (blue), DELETE (red).
