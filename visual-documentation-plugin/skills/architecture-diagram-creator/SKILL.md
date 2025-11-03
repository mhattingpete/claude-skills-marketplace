---
name: architecture-diagram-creator
description: Create comprehensive project architecture diagrams showing data flows, business objectives, features, technical architecture, and deployment. Use when users request system architecture, project documentation, high-level overviews, or technical specifications for any software project.
---

# Architecture Diagram Creator

Create professional, comprehensive HTML architecture diagrams that document entire software projects with data flows, business context, features (functional and non-functional), processing pipelines, system architecture, and deployment information.

## When to Use This Skill

Activate this skill when users request:
- "Create an architecture diagram for [project]"
- "Generate a high-level overview of [system]"
- "Document the system architecture for [project]"
- "Create a project architecture report"
- "Show me the data flow and processing pipeline"
- "Generate comprehensive technical documentation"
- "Create a system design document"

## Capabilities

### Architecture Components

**Business Context Section:**
- Business objectives and goals
- End users and stakeholders
- Business value and ROI
- Primary use cases
- Success metrics

**Data Flow Diagrams:**
- Input data sources with details
- Processing engine visualization
- Output destinations
- Data transformation steps
- Source-to-target mapping

**Processing Pipeline:**
- Multi-stage pipeline visualization
- Sequential and parallel processing
- Data transformations at each stage
- External service integrations
- Checkpointing and caching

**System Architecture:**
- Layered architecture (data, processing, services, output)
- Core components and modules
- External dependencies and APIs
- Configuration management
- Supporting tools and utilities

**Features Documentation:**
- Functional features with details
- Non-functional requirements (performance, security, maintainability)
- Feature cards with bullet points
- Technology stack and dependencies

**Deployment Information:**
- Deployment model (local, cloud, hybrid)
- Prerequisites and requirements
- Typical workflows
- Output delivery methods

**Reference Tables:**
- Data mappings and transformations
- Configuration references
- Module/component relationships
- Important rules and constraints

### Design Features

**Color System:**
- Data Sources: `#4299e1` (blue)
- Processing: `#ed8936` (orange)
- AI/ML Services: `#9f7aea` (purple)
- Output/Success: `#48bb78` (green)
- Configuration: `#f59e0b` (amber)
- Supporting Tools: `#718096` (gray)
- Warning/Critical: `#e53e3e` (red)
- Information: `#38b2ac` (teal)

**Layout:**
- Responsive design with max-width containers
- Gradient header backgrounds
- Section-based organization
- Grid layouts for feature cards
- SVG diagrams with proper viewBox scaling
- Mobile-friendly (768px breakpoint)

## Workflow

### Step 1: Gather Project Context

Analyze the project to extract:
- **Project purpose**: What problem does it solve?
- **Data sources**: What data inputs exist?
- **Processing logic**: How is data transformed?
- **Technology stack**: What frameworks/libraries/APIs are used?
- **Output artifacts**: What does the system produce?
- **Users and stakeholders**: Who uses this system?

**Key files to examine:**
- README.md, CLAUDE.md, or project documentation
- Source code structure (main scripts, modules)
- Configuration files (YAML, JSON, .env)
- Package managers (package.json, requirements.txt, pyproject.toml)
- Data files or database schemas

### Step 2: Identify Architecture Patterns

Determine the architectural style:

**Data Pipeline Architecture:**
- Input → Processing → Output flow
- ETL (Extract, Transform, Load) pattern
- Batch or stream processing
- Example: Data consolidation, report generation

**Microservices Architecture:**
- Multiple independent services
- API-based communication
- Service mesh or API gateway
- Example: Web applications, distributed systems

**Layered Architecture:**
- Presentation layer
- Business logic layer
- Data access layer
- Infrastructure layer
- Example: Traditional web apps, enterprise systems

**Event-Driven Architecture:**
- Event producers and consumers
- Message queues or brokers
- Asynchronous processing
- Example: Real-time systems, notifications

### Step 3: Document Business Context

Create business objectives section with:

**Objective Cards:**
```html
<div class="feature-card">
    <h3>Primary Objective</h3>
    <ul>
        <li>Main goal statement</li>
        <li>Problem being solved</li>
        <li>Expected outcomes</li>
    </ul>
</div>
```

**End Users:**
- Who uses the system?
- What are their roles?
- What are their needs?

**Business Value:**
- Cost savings
- Efficiency improvements
- Quality enhancements
- Risk reduction

### Step 4: Create Data Flow Diagram

Build SVG diagram showing:

**Input Sources (Left):**
```xml
<rect x="50" y="50" width="250" height="200" rx="15"
      fill="#4299e1" stroke="#2b6cb0" stroke-width="3"/>
<text x="175" y="85" text-anchor="middle" fill="white"
      font-size="16" font-weight="bold">Source 1</text>
<text x="175" y="110" text-anchor="middle" fill="white"
      font-size="12">Details about source</text>
```

**Processing Engine (Center):**
```xml
<rect x="450" y="200" width="300" height="150" rx="15"
      fill="#ed8936" stroke="#c05621" stroke-width="3"/>
<text x="600" y="235" text-anchor="middle" fill="white"
      font-size="16" font-weight="bold">Processing Engine</text>
<text x="600" y="260" text-anchor="middle" fill="white"
      font-size="11">• Step 1</text>
```

**Output (Right):**
```xml
<rect x="900" y="175" width="250" height="200" rx="15"
      fill="#48bb78" stroke="#2f855a" stroke-width="3"/>
<text x="1025" y="210" text-anchor="middle" fill="white"
      font-size="16" font-weight="bold">Output</text>
```

**Connectors with arrows:**
```xml
<defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10"
            refX="9" refY="3" orient="auto">
        <polygon points="0 0, 10 3, 0 6" fill="#2d3748"/>
    </marker>
</defs>
<path d="M 300 150 L 450 250" stroke="#2d3748"
      stroke-width="3" marker-end="url(#arrowhead)"/>
```

### Step 5: Build Processing Pipeline Diagram

Create multi-stage pipeline visualization:

**Sequential stages (vertical or horizontal):**
```
Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5
   ↓         ↓         ↓         ↓         ↓
Details   Details   Details   Details   Details
```

**Include for each stage:**
- Stage name and number
- Key operations performed
- Technologies/libraries used
- Input and output
- Error handling approach

**Show branching when applicable:**
```
Stage 3 → Stage 4A (Parallel)
       → Stage 4B (Parallel) → Merge → Stage 5
```

### Step 6: Document System Architecture

Create layered architecture diagram:

**Layer 1: Data Sources**
- External files, databases, APIs
- Configuration files
- User inputs

**Layer 2: Core Processing**
- Main application logic
- Business rules
- Data transformations

**Layer 3: External Services**
- Third-party APIs (AI/ML, cloud services)
- Authentication services
- Monitoring and logging

**Layer 4: Output & Storage**
- Generated files
- Database writes
- API responses
- Caching and checkpoints

**Layer 5: Supporting Tools**
- Utilities and helpers
- Testing frameworks
- Development tools

### Step 7: Document Features

Create two feature sections:

**Functional Features:**
```html
<div class="feature-grid">
    <div class="feature-card">
        <h3>Feature Name</h3>
        <ul>
            <li>Capability 1</li>
            <li>Capability 2</li>
            <li>Capability 3</li>
        </ul>
    </div>
</div>
```

**Non-Functional Features:**
- Performance characteristics
- Scalability considerations
- Security measures
- Maintainability features
- Reliability/availability
- Monitoring and observability

### Step 8: Add Key Metrics

Include metrics at the top:
```html
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-value">42</div>
        <div class="metric-label">Key Metric</div>
    </div>
</div>
```

**Common metrics:**
- Number of data sources
- Processing stages count
- External dependencies
- Key performance numbers (throughput, latency)
- Lines of code or file count

### Step 9: Create Reference Tables

For complex mappings or relationships:

**Table format:**
```html
<!-- SVG-based table for visual consistency -->
<rect x="50" y="50" width="140" height="40" fill="#667eea"/>
<text x="120" y="75" text-anchor="middle" fill="white">Column 1</text>

<rect x="50" y="90" width="140" height="50" fill="#e6fffa"/>
<text x="120" y="120" text-anchor="middle" fill="#234e52">Data 1</text>
```

**Include critical information:**
- Data mappings (source → target)
- Module relationships
- Configuration references
- Important rules and constraints

### Step 10: Add Deployment Section

Document deployment with feature cards:

**Deployment Model:**
- Local execution, cloud-hosted, hybrid
- Runtime environment (Docker, serverless, VMs)

**Prerequisites:**
- Software dependencies
- API keys or credentials
- System requirements

**Typical Workflow:**
- Step-by-step usage instructions
- Common commands
- Configuration steps

**Output Delivery:**
- Where outputs are stored
- How users access results
- Integration with other systems

## HTML Template Structure

Use this standard structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Project Name] Architecture</title>
    <style>
        /* Base styles */
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 3rem;
        }

        h1 {
            font-size: 2.5rem;
            color: #2d3748;
            margin-bottom: 0.5rem;
            text-align: center;
        }

        .subtitle {
            text-align: center;
            color: #718096;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }

        /* Metrics grid */
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }

        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            color: white;
        }

        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }

        .metric-label {
            font-size: 0.9rem;
            opacity: 0.9;
        }

        /* Section styles */
        .section {
            margin: 2rem 0;
        }

        .section-title {
            font-size: 1.5rem;
            color: #2d3748;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid #667eea;
        }

        /* Diagram container */
        .diagram-container {
            background: #f7fafc;
            border-radius: 12px;
            padding: 2rem;
            margin: 1rem 0;
            overflow-x: auto;
        }

        svg {
            width: 100%;
            height: auto;
            display: block;
        }

        /* Feature grid */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin: 1rem 0;
        }

        .feature-card {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 1.5rem;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .feature-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        .feature-card h3 {
            color: #667eea;
            margin-bottom: 0.5rem;
            font-size: 1.2rem;
        }

        .feature-card ul {
            list-style: none;
            color: #4a5568;
            line-height: 1.8;
        }

        .feature-card ul li:before {
            content: "→ ";
            color: #667eea;
            font-weight: bold;
        }

        /* Legend */
        .legend {
            display: flex;
            flex-wrap: wrap;
            gap: 1.5rem;
            margin-top: 2rem;
            padding: 1.5rem;
            background: #f7fafc;
            border-radius: 12px;
            justify-content: center;
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .legend-box {
            width: 20px;
            height: 20px;
            border-radius: 4px;
            border: 2px solid #2d3748;
        }

        /* Footer */
        footer {
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 2px solid #e2e8f0;
            text-align: center;
            color: #718096;
            font-size: 0.9rem;
        }

        /* Mobile responsive */
        @media (max-width: 768px) {
            body { padding: 1rem; }
            .container { padding: 1.5rem; }
            h1 { font-size: 1.8rem; }
            .metric-grid { grid-template-columns: 1fr; }
            .feature-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>[Project Icon] [Project Name]</h1>
        <p class="subtitle">[One-line project description]</p>

        <!-- Key Metrics -->
        <div class="metric-grid">
            <!-- Metric cards here -->
        </div>

        <!-- Business Context -->
        <div class="section">
            <h2 class="section-title">📊 Business Objectives & End Users</h2>
            <div class="feature-grid">
                <!-- Feature cards here -->
            </div>
        </div>

        <!-- Data Flow -->
        <div class="section">
            <h2 class="section-title">📥 Data Input Overview</h2>
            <div class="diagram-container">
                <svg viewBox="0 0 1200 600">
                    <!-- SVG diagram here -->
                </svg>
            </div>
        </div>

        <!-- Processing Pipeline -->
        <div class="section">
            <h2 class="section-title">⚙️ Data Processing Pipeline</h2>
            <div class="diagram-container">
                <svg viewBox="0 0 1400 700">
                    <!-- Pipeline diagram here -->
                </svg>
            </div>
        </div>

        <!-- Functional Features -->
        <div class="section">
            <h2 class="section-title">✨ Functional Features</h2>
            <div class="feature-grid">
                <!-- Feature cards here -->
            </div>
        </div>

        <!-- Non-Functional Features -->
        <div class="section">
            <h2 class="section-title">🛡️ Non-Functional Features</h2>
            <div class="feature-grid">
                <!-- Feature cards here -->
            </div>
        </div>

        <!-- System Architecture -->
        <div class="section">
            <h2 class="section-title">🏗️ System Architecture</h2>
            <div class="diagram-container">
                <svg viewBox="0 0 1400 800">
                    <!-- Architecture diagram here -->
                </svg>
            </div>
        </div>

        <!-- Deployment -->
        <div class="section">
            <h2 class="section-title">🚀 Deployment & Usage</h2>
            <div class="feature-grid">
                <!-- Deployment info cards here -->
            </div>
        </div>

        <!-- Legend -->
        <div class="legend">
            <div class="legend-item">
                <div class="legend-box" style="background: #4299e1;"></div>
                <span>Data Sources</span>
            </div>
            <!-- More legend items -->
        </div>

        <footer>
            <strong>[Project Name] Architecture v[Version]</strong><br>
            Generated: [Date] | [Short description]<br>
            Technologies: [Tech stack]
        </footer>
    </div>
</body>
</html>
```

## Best Practices

### Content Organization

**Start with overview:**
- Project name and description
- Key metrics (4-8 high-level numbers)
- Quick visual summary

**Progress from high-level to detailed:**
1. Business context (why)
2. Data flow (what)
3. Processing pipeline (how)
4. Features (capabilities)
5. Architecture (structure)
6. Deployment (usage)

**Include context for each section:**
- Explain what the section shows
- Define any technical terms
- Provide examples where helpful

### Visual Design

**Consistency:**
- Use the same color for the same concept throughout
- Maintain consistent spacing and sizing
- Use the same icon style (emoji recommended)

**Hierarchy:**
- Larger headings for major sections
- Clear visual separation between sections
- Grouped related information

**Readability:**
- High contrast text (WCAG AA: 4.5:1)
- Adequate white space
- Avoid text cramming
- Use bullet points over paragraphs

### SVG Diagram Guidelines

**Spacing:**
- Minimum 50px between small elements
- Minimum 100px between major components
- Leave 50px padding around diagram edges

**Text sizing:**
- Titles: 14-16px
- Body text: 10-12px
- Labels: 9-11px
- Ensure text doesn't overflow boxes

**Colors:**
- Use semantic colors consistently
- Provide legend for color meanings
- Ensure sufficient contrast for text

**Arrows and connectors:**
- Use clear, thick lines (3px recommended)
- Add arrow markers for direction
- Label important connections
- Keep paths simple (prefer orthogonal)

### Technical Accuracy

**Verify information:**
- Cross-reference with actual code
- Check configuration files for accuracy
- Validate technology versions
- Confirm API integrations

**Be specific:**
- Use actual file names and paths
- Include real metric values when available
- Reference specific technologies (not "database", but "PostgreSQL 14")
- List actual environment variables

**Handle missing information:**
- Mark as "[To be determined]" if unknown
- Use placeholder values with clear indication
- Note assumptions made

## Common Patterns

### Data Pipeline Projects

**Characteristics:**
- Clear input → processing → output flow
- ETL/ELT operations
- Data transformation and enrichment
- Batch or stream processing

**Focus on:**
- Data sources and formats
- Transformation logic and stages
- Error handling and validation
- Output formats and destinations
- Performance and throughput

### Web Applications

**Characteristics:**
- Frontend and backend layers
- API endpoints
- Database interactions
- User authentication

**Focus on:**
- Request/response flow
- API architecture
- Data models
- Authentication/authorization
- Frontend components

### Machine Learning Projects

**Characteristics:**
- Data ingestion and preprocessing
- Model training and evaluation
- Inference/prediction serving
- Monitoring and retraining

**Focus on:**
- Dataset characteristics
- Model architecture
- Training pipeline
- Deployment strategy
- Monitoring and metrics

### Microservices

**Characteristics:**
- Multiple independent services
- Inter-service communication
- Service discovery
- API gateway

**Focus on:**
- Service boundaries
- Communication protocols
- Data consistency
- Deployment topology
- Observability

## Example Sections

### Example: Business Objectives

```html
<div class="section">
    <h2 class="section-title">📊 Business Objectives & End Users</h2>
    <div class="feature-grid">
        <div class="feature-card">
            <h3>Primary Objective</h3>
            <ul>
                <li>Consolidate duplicate defect tracking across sites</li>
                <li>Eliminate redundant maintenance efforts</li>
                <li>Create unified improvement roadmap</li>
                <li>Enable data-driven prioritization</li>
            </ul>
        </div>
        <div class="feature-card">
            <h3>End Users</h3>
            <ul>
                <li>Manufacturing Engineers (2 sites)</li>
                <li>Quality Assurance Teams</li>
                <li>Subject Matter Experts (SMEs)</li>
                <li>Vendor Partners (5+ vendors)</li>
                <li>Fleet 4 Project Managers</li>
            </ul>
        </div>
        <div class="feature-card">
            <h3>Business Value</h3>
            <ul>
                <li>Reduce duplicate vendor investigations</li>
                <li>Standardize problem categorization</li>
                <li>Improve cross-site collaboration</li>
                <li>Accelerate issue resolution</li>
            </ul>
        </div>
    </div>
</div>
```

### Example: Data Flow Diagram

```html
<div class="section">
    <h2 class="section-title">📥 Data Input Overview</h2>
    <div class="diagram-container">
        <svg viewBox="0 0 1200 400">
            <defs>
                <marker id="arrowhead" markerWidth="10" markerHeight="10"
                        refX="9" refY="3" orient="auto">
                    <polygon points="0 0, 10 3, 0 6" fill="#2d3748"/>
                </marker>
            </defs>

            <!-- Source 1 -->
            <rect x="50" y="50" width="200" height="120" rx="15"
                  fill="#4299e1" stroke="#2b6cb0" stroke-width="3"/>
            <text x="150" y="85" text-anchor="middle" fill="white"
                  font-size="14" font-weight="bold">Source Database</text>
            <text x="150" y="110" text-anchor="middle" fill="white"
                  font-size="10">PostgreSQL 14</text>
            <text x="150" y="125" text-anchor="middle" fill="white"
                  font-size="10">~1M records</text>
            <text x="150" y="140" text-anchor="middle" fill="white"
                  font-size="10">User events table</text>

            <!-- Processing -->
            <rect x="350" y="75" width="220" height="100" rx="15"
                  fill="#ed8936" stroke="#c05621" stroke-width="3"/>
            <text x="460" y="110" text-anchor="middle" fill="white"
                  font-size="14" font-weight="bold">ETL Pipeline</text>
            <text x="460" y="130" text-anchor="middle" fill="white"
                  font-size="10">Apache Airflow</text>
            <text x="460" y="145" text-anchor="middle" fill="white"
                  font-size="10">Daily batch job</text>

            <!-- Output -->
            <rect x="670" y="50" width="200" height="120" rx="15"
                  fill="#48bb78" stroke="#2f855a" stroke-width="3"/>
            <text x="770" y="85" text-anchor="middle" fill="white"
                  font-size="14" font-weight="bold">Analytics DB</text>
            <text x="770" y="110" text-anchor="middle" fill="white"
                  font-size="10">BigQuery</text>
            <text x="770" y="125" text-anchor="middle" fill="white"
                  font-size="10">Aggregated metrics</text>
            <text x="770" y="140" text-anchor="middle" fill="white"
                  font-size="10">Daily snapshots</text>

            <!-- Arrows -->
            <path d="M 250 110 L 350 125" stroke="#2d3748"
                  stroke-width="3" marker-end="url(#arrowhead)"/>
            <path d="M 570 125 L 670 110" stroke="#2d3748"
                  stroke-width="3" marker-end="url(#arrowhead)"/>

            <!-- Labels -->
            <text x="300" y="100" text-anchor="middle" fill="#2d3748"
                  font-size="10" font-weight="bold">Raw events</text>
            <text x="620" y="100" text-anchor="middle" fill="#2d3748"
                  font-size="10" font-weight="bold">Aggregated</text>
        </svg>
    </div>
</div>
```

### Example: Feature Cards

```html
<div class="section">
    <h2 class="section-title">✨ Functional Features</h2>
    <div class="feature-grid">
        <div class="feature-card">
            <h3>Real-Time Processing</h3>
            <ul>
                <li>Kafka consumer for event streaming</li>
                <li>Sub-second latency for 95th percentile</li>
                <li>Automatic scaling based on load</li>
                <li>Dead-letter queue for failed events</li>
            </ul>
        </div>
        <div class="feature-card">
            <h3>Data Validation</h3>
            <ul>
                <li>JSON schema validation for all inputs</li>
                <li>Business rule validation engine</li>
                <li>Anomaly detection with ML models</li>
                <li>Comprehensive error reporting</li>
            </ul>
        </div>
        <div class="feature-card">
            <h3>API Integration</h3>
            <ul>
                <li>RESTful API with OpenAPI spec</li>
                <li>OAuth 2.0 authentication</li>
                <li>Rate limiting (1000 req/min)</li>
                <li>Webhook notifications</li>
            </ul>
        </div>
    </div>
</div>
```

## Troubleshooting

**Issue:** Too much information, diagram feels cluttered
- **Solution**: Break into multiple sections, create separate diagrams for different aspects, use collapsible sections

**Issue:** SVG text overflows boxes
- **Solution**: Increase box width, reduce font size, or split text into multiple lines

**Issue:** Colors don't provide enough contrast
- **Solution**: Use darker text (#2d3748) on light backgrounds, white text on dark backgrounds, ensure 4.5:1 ratio

**Issue:** Diagram doesn't scale well on mobile
- **Solution**: Use responsive viewBox, test at 768px width, consider mobile-first layout

**Issue:** Missing critical project information
- **Solution**: Mark as "[TBD]", note assumptions, ask user for clarification, research documentation

## Resources

This skill includes dedicated templates and examples:

**Templates:**
- `assets/templates/base_template.html` - Complete HTML/CSS framework with responsive design, metric cards, feature grids, diagram containers, and legend
- `assets/templates/architecture_components.html` - Reusable SVG components including data source boxes, processing engines, output boxes, AI service boxes, arrows/connectors, pipeline stages, layered architecture, tables, and annotations

**Reference Example:**
- `references/example_architecture.html` - Complete working example of a data pipeline architecture diagram showing all sections: business objectives, data flows, processing pipeline, features, system architecture, and deployment

**How to use:**
1. Reference the base template for HTML structure and CSS styling
2. Copy SVG component patterns from architecture_components.html
3. Study the example_architecture.html to see how all pieces fit together
4. Adapt the structure and components to the specific project being documented

## Output Checklist

Before delivering the architecture diagram, verify:

- [ ] All sections present: Business, Data Flow, Pipeline, Features, Architecture, Deployment
- [ ] Key metrics included and accurate
- [ ] SVG diagrams render correctly
- [ ] All text is readable (contrast, size)
- [ ] Colors are used consistently
- [ ] Legend explains all colors/symbols
- [ ] Feature cards are well-organized
- [ ] Technical details are accurate
- [ ] Mobile responsive layout works
- [ ] Footer includes date and tech stack
- [ ] No placeholder text left (except intentional "[TBD]")

## Example Use Cases

**Use Case 1: Data Pipeline Documentation**
```
User: "Create an architecture diagram for my ETL pipeline that consolidates customer data from 3 sources"
Assistant: *Activates architecture-diagram-creator skill*
Output: Comprehensive HTML with data sources, transformation stages, output warehouse, and deployment info
```

**Use Case 2: Web Application Overview**
```
User: "Generate a high-level architecture doc for my e-commerce web app"
Assistant: *Activates architecture-diagram-creator skill*
Output: Diagram showing frontend, API layer, microservices, databases, and third-party integrations
```

**Use Case 3: ML System Documentation**
```
User: "Document the architecture of our ML recommendation system"
Assistant: *Activates architecture-diagram-creator skill*
Output: Pipeline from data ingestion → training → model serving → monitoring, with feature engineering details
```

**Use Case 4: Existing Project Analysis**
```
User: "Analyze my codebase and create an architecture diagram"
Assistant: *Reads project files, identifies patterns*
Assistant: *Activates architecture-diagram-creator skill*
Output: Complete architecture documentation based on discovered code structure
```
