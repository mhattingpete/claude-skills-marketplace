---
name: technical-doc-creator
description: Create stunning HTML technical documentation with code blocks, API workflows, system architecture diagrams, and syntax highlighting. Use when users explicitly request technical documentation, API docs, code examples, or system architecture visualizations in HTML format.
---

# Technical Documentation Creator

Create professional HTML technical documentation with code blocks, API workflows, system architecture diagrams, syntax highlighting, and example sections.

## When to Use This Skill

Activate this skill when users request:
- "Create technical documentation for [API/system]"
- "Generate API documentation for [endpoints]"
- "Make a visual guide for [technical feature]"
- "Document the [system architecture]"
- "Create HTML docs showing [code examples]"

## Capabilities

### Technical Doc Components

**Code Blocks:**
- Syntax-highlighted code samples
- Dark themed code display
- Support for multiple languages
- Line numbers (optional)
- Copy-friendly formatting

**API Workflows:**
- Request/response flow diagrams
- HTTP method indicators (GET, POST, PUT, DELETE)
- JSON/XML payload examples
- Authentication flows
- Error handling paths

**Architecture Diagrams:**
- System component boxes
- Connection arrows showing data flow
- Database/service representations
- Network layer visualization
- Integration points

**Example Sections:**
- Bordered example boxes
- Before/after comparisons
- Use case demonstrations
- Step-by-step tutorials
- Best practices callouts

### Design Features

**Color System:**
- Success/200 responses: `#48bb78` (green)
- Warning/Deprecation: `#f59e0b` (amber)
- Info/General: `#4299e1` (blue)
- Error/4xx-5xx: `#f56565` (red)
- Methods/Actions: `#ed8936` (orange)
- Special features: `#9f7aea` (purple)

**Code Styling:**
- Background: `#2d3748` (dark)
- Text: `#e2e8f0` (light)
- Highlights: `#fbbf24` (amber)
- Comments: `#718096` (gray)

## Workflow

### Step 1: Understand the Technical Content

Analyze the user's request to identify:
- **Type**: API docs, architecture, tutorial, reference
- **Audience**: Developers, DevOps, architects, end-users
- **Scope**: Single feature, full system, specific component
- **Examples needed**: Code samples, curl commands, responses
- **Diagrams**: Flow, architecture, sequence

### Step 2: Choose Documentation Structure

**API Reference:**
```
[Overview]
[Authentication]
[Endpoints Section 1]
  - Endpoint details
  - Request format
  - Response format
  - Examples
[Error Codes]
```

**System Architecture:**
```
[Overview Diagram]
[Component Details]
[Data Flow]
[Integration Points]
[Deployment Architecture]
```

**Tutorial/Guide:**
```
[Introduction]
[Prerequisites]
[Step 1: Setup]
[Step 2: Implementation]
[Step 3: Testing]
[Troubleshooting]
```

**Feature Documentation:**
```
[Feature Overview]
[How It Works (with diagram)]
[Usage Examples]
[Configuration]
[Best Practices]
```

### Step 3: Build HTML Structure

Use the base template from `../visual-html-creator/assets/templates/base_template.html` for the HTML/CSS framework.

Use flowchart components from `../visual-html-creator/assets/templates/flowchart_components.html` for architecture diagrams.

Reference design patterns from `../visual-html-creator/references/design_patterns.md` for colors and spacing.

Reference SVG techniques from `../visual-html-creator/references/svg_library.md` for diagram creation.

**Standard structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Technical Doc Title]</title>
    <style>
        /* Embedded CSS from base template */
    </style>
</head>
<body>
    <div class="container">
        <h1>[Documentation Title]</h1>
        <p class="subtitle">[API Version or Description]</p>

        <!-- Table of Contents (Optional) -->
        <div class="section">
            <h2 class="section-title">Contents</h2>
            <ul>
                <li><a href="#section1">Section 1</a></li>
                <!-- More links -->
            </ul>
        </div>

        <!-- Main Content Sections -->
        <div class="section" id="section1">
            <h2 class="section-title">Section Title</h2>

            <!-- Code Block -->
            <div class="code-block">
<span class="highlight">// Code example</span>
function example() {
    return "code";
}
            </div>

            <!-- Example Box -->
            <div class="example-box">
                <div class="example-title">Example: [Title]</div>
                <p>Example content...</p>
            </div>

            <!-- Diagram -->
            <div class="diagram-container">
                <svg viewBox="0 0 1200 600">
                    <!-- Diagram content -->
                </svg>
            </div>
        </div>

        <!-- Legend -->
        <div class="legend">
            <div class="legend-item">
                <div class="legend-box" style="background: #48bb78;"></div>
                <span>HTTP 200 - Success</span>
            </div>
            <!-- More legend items -->
        </div>
    </div>
</body>
</html>
```

### Step 4: Create Code Blocks

**Basic code block:**
```html
<div class="code-block">
<span class="highlight">// Highlighted comment or keyword</span>
const apiUrl = "https://api.example.com/v1";

function getData() {
    fetch(apiUrl + "/users")
        .then(response => response.json())
        .then(data => console.log(data));
}
</div>
```

**API Request example:**
```html
<div class="code-block">
<span class="highlight">POST</span> /api/v1/users
<span class="highlight">Content-Type:</span> application/json
<span class="highlight">Authorization:</span> Bearer {token}

{
    "name": "John Doe",
    "email": "john@example.com"
}
</div>
```

**Response example:**
```html
<div class="code-block">
<span class="highlight">HTTP/1.1 201 Created</span>
<span class="highlight">Content-Type:</span> application/json

{
    "id": "12345",
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2025-01-20T10:30:00Z"
}
</div>
```

### Step 5: Create Architecture Diagrams

**API Flow diagram:**
```xml
<svg viewBox="0 0 1200 600">
    <!-- Client -->
    <rect x="50" y="250" width="200" height="100" rx="10"
          fill="#4299e1" stroke="#2b6cb0" stroke-width="3"/>
    <text x="150" y="295" text-anchor="middle" fill="white"
          font-size="16" font-weight="bold">
        Client App
    </text>

    <!-- Arrow -->
    <path d="M 250 300 L 400 300" stroke="#2d3748" stroke-width="3"
          marker-end="url(#arrowhead)"/>
    <text x="325" y="290" text-anchor="middle" font-size="12"
          fill="#2d3748" font-weight="bold">
        HTTP Request
    </text>

    <!-- API Gateway -->
    <rect x="400" y="250" width="200" height="100" rx="10"
          fill="#48bb78" stroke="#2f855a" stroke-width="3"/>
    <text x="500" y="295" text-anchor="middle" fill="white"
          font-size="16" font-weight="bold">
        API Gateway
    </text>

    <!-- Arrow -->
    <path d="M 600 300 L 750 300" stroke="#2d3748" stroke-width="3"
          marker-end="url(#arrowhead)"/>

    <!-- Service -->
    <rect x="750" y="250" width="200" height="100" rx="10"
          fill="#9f7aea" stroke="#6b46c1" stroke-width="3"/>
    <text x="850" y="295" text-anchor="middle" fill="white"
          font-size="16" font-weight="bold">
        Backend Service
    </text>

    <!-- Arrow marker -->
    <defs>
        <marker id="arrowhead" markerWidth="10" markerHeight="10"
                refX="9" refY="3" orient="auto">
            <polygon points="0 0, 10 3, 0 6" fill="#2d3748"/>
        </marker>
    </defs>
</svg>
```

**System architecture:**
```xml
<svg viewBox="0 0 1200 800">
    <!-- Title -->
    <text x="600" y="40" text-anchor="middle" font-size="24"
          font-weight="bold" fill="#2d3748">
        System Architecture
    </text>

    <!-- Frontend Layer -->
    <rect x="50" y="100" width="1100" height="150" rx="10"
          fill="#e6f2ff" stroke="#4299e1" stroke-width="2"/>
    <text x="600" y="135" text-anchor="middle" font-size="16"
          font-weight="bold" fill="#2d3748">
        Frontend Layer
    </text>

    <!-- Components in Frontend -->
    <rect x="100" y="160" width="150" height="70" rx="8"
          fill="#4299e1" stroke="#2b6cb0" stroke-width="2"/>
    <text x="175" y="200" text-anchor="middle" fill="white"
          font-size="13" font-weight="bold">
        Web App
    </text>

    <!-- Backend Layer -->
    <rect x="50" y="300" width="1100" height="150" rx="10"
          fill="#e6ffe6" stroke="#48bb78" stroke-width="2"/>
    <text x="600" y="335" text-anchor="middle" font-size="16"
          font-weight="bold" fill="#2d3748">
        Backend Layer
    </text>

    <!-- Data Layer -->
    <rect x="50" y="500" width="1100" height="150" rx="10"
          fill="#fff5e6" stroke="#f59e0b" stroke-width="2"/>
    <text x="600" y="535" text-anchor="middle" font-size="16"
          font-weight="bold" fill="#2d3748">
        Data Layer
    </text>

    <!-- Connection arrows between layers -->
    <path d="M 600 250 L 600 300" stroke="#2d3748" stroke-width="3"
          marker-end="url(#arrowhead)" stroke-dasharray="5,5"/>
    <path d="M 600 450 L 600 500" stroke="#2d3748" stroke-width="3"
          marker-end="url(#arrowhead)" stroke-dasharray="5,5"/>
</svg>
```

### Step 6: Add Examples and Annotations

**Example box pattern:**
```html
<div class="example-box">
    <div class="example-title">Example: User Authentication</div>
    <p><strong>Request:</strong></p>
    <div class="code-block">
POST /api/auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "secret123"
}
    </div>
    <p><strong>Response (Success):</strong></p>
    <div class="code-block">
<span class="highlight">HTTP 200 OK</span>

{
    "token": "eyJhbGc...",
    "expires_in": 3600
}
    </div>
</div>
```

**Callout for important notes:**
```html
<div class="example-box" style="border-color: #f59e0b; background: #fffbeb;">
    <div class="example-title" style="color: #f59e0b;">⚠️ Important Note</div>
    <p>Always store API tokens securely and never commit them to version control.</p>
</div>
```

## Best Practices

### Documentation Structure

**Clear hierarchy:**
- Use h1 for main title
- Use h2 for major sections
- Use h3 for subsections
- Maintain consistent heading levels

**Progressive disclosure:**
1. Start with overview/introduction
2. Show simple examples first
3. Progress to advanced topics
4. End with troubleshooting/FAQ

**Searchability:**
- Use descriptive section titles
- Include keywords in headings
- Add table of contents for long docs
- Use consistent terminology

### Code Presentation

**Formatting:**
- Use consistent indentation (2 or 4 spaces)
- Include language context (curl, JavaScript, Python)
- Show complete, runnable examples
- Highlight key parts with `<span class="highlight">`

**Examples:**
- Provide realistic examples
- Include error cases, not just success
- Show input and expected output
- Add comments explaining non-obvious parts

### Technical Accuracy

**Completeness:**
- Document all required parameters
- Specify data types
- Include default values
- Note optional vs required fields

**Error handling:**
- Document all error codes
- Provide error message examples
- Explain what triggers each error
- Suggest resolution steps

### Visual Aids

**When to use diagrams:**
- System architecture (always)
- Complex data flows (recommended)
- Multi-step processes (helpful)
- Integration patterns (useful)

**Keep diagrams:**
- Simple and focused
- Properly labeled
- Color-coded for clarity
- Consistent with text descriptions

## Common Patterns

### API Endpoint Documentation
```
[Endpoint Name]
[HTTP Method + URL]
[Description]
[Authentication Required]
[Request Parameters]
[Request Body Example]
[Response Format]
[Response Example (Success)]
[Error Responses]
[Code Example (curl/SDK)]
```

### Authentication Guide
```
[Overview]
[Authentication Flow Diagram]
[Getting API Keys]
[Making Authenticated Requests]
[Token Refresh]
[Security Best Practices]
```

### Integration Guide
```
[Prerequisites]
[Installation]
[Configuration]
[Basic Usage Example]
[Advanced Features]
[Troubleshooting]
```

### Architecture Documentation
```
[System Overview Diagram]
[Component Descriptions]
[Data Flow Diagrams]
[Technology Stack]
[Deployment Architecture]
[Scalability Considerations]
```

## Example Output Structure

**User request:** "Create API documentation for our user management endpoints"

**Generated output includes:**
1. **Overview**: API purpose and base URL
2. **Authentication**: How to authenticate requests
3. **Endpoints**:
   - GET /users - List all users
   - POST /users - Create user (with example)
   - GET /users/{id} - Get specific user
   - PUT /users/{id} - Update user
   - DELETE /users/{id} - Delete user
4. **Request/Response examples** for each endpoint
5. **Error codes**: 400, 401, 404, 500 with descriptions
6. **Rate limiting**: Information on limits
7. **Code examples**: curl, JavaScript, Python
8. **Architecture diagram**: Request flow

## Resources

This skill uses shared resources from the visual-html-creator skill:
- `../visual-html-creator/assets/templates/base_template.html` - CSS framework
- `../visual-html-creator/assets/templates/flowchart_components.html` - Diagram patterns
- `../visual-html-creator/references/design_patterns.md` - Design system
- `../visual-html-creator/references/svg_library.md` - SVG techniques

## Troubleshooting

**Issue:** Code blocks lose formatting
- **Solution**: Use `<pre>` tags, preserve whitespace, avoid word wrap

**Issue:** Examples are too complex
- **Solution**: Start simple, build up gradually, split complex examples

**Issue:** Diagrams are cluttered
- **Solution**: Focus on one concept per diagram, use layers/sections, simplify

**Issue:** Missing important details
- **Solution**: Review with checklist, include all parameters, document edge cases
