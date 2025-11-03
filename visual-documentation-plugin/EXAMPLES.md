# Visual Documentation Skills - Examples

This document provides example prompts and use cases for each of the visual documentation skills.

---

## 1. Architecture Diagram Creator

**When to use:** Comprehensive project documentation, system architecture overviews, technical specifications, project onboarding, stakeholder presentations

### Example Prompts

**Simple:**
```
Create an architecture diagram for this project
```

**Detailed:**
```
Create a comprehensive architecture diagram for my data processing pipeline project:

**Project Context:**
- Consolidates customer data from 3 sources (Salesforce API, MySQL database, CSV exports)
- Processes ~100K records daily using Python ETL scripts
- Uses AWS services (S3, Lambda, RDS)
- Outputs to data warehouse for analytics

**Key Features:**
- Automated data validation and deduplication
- Real-time anomaly detection with ML model
- Configurable transformation rules
- Error handling and retry logic

**End Users:**
- Data analysts and scientists
- Business intelligence team
- Marketing automation systems

Include sections for: business objectives, data flow diagram, processing pipeline,
system architecture (layers), functional and non-functional features, and deployment info.
```

**From Existing Codebase:**
```
Analyze the current project directory and create a comprehensive architecture diagram
documenting: data sources, processing logic, external APIs/services, output artifacts,
features, and deployment model. Read CLAUDE.md, README.md, and source files to gather context.
```

### Expected Output
- Professional HTML file with multiple sections:
  - Business objectives and end users
  - Key project metrics (sources, stages, dependencies)
  - Data flow diagram (source → processing → output)
  - Multi-stage processing pipeline visualization
  - System architecture with layers (data, processing, services, output)
  - Functional features (with feature cards)
  - Non-functional features (performance, security, etc.)
  - Deployment information
  - Reference tables (data mappings, configurations)
- Modern gradient styling with semantic colors
- Responsive design for mobile and desktop
- Self-contained HTML with no external dependencies

---

## 2. Flowchart Creator

**When to use:** Process flows, decision trees, workflow diagrams, authentication flows, state machines

### Example Prompts

**Simple:**
```
Create a flowchart showing the user authentication process
```

**Detailed:**
```
Create a flowchart for our e-commerce checkout process:
1. User adds items to cart
2. User clicks checkout
3. System validates cart (if invalid, show error)
4. User enters shipping information
5. User selects payment method
6. System processes payment
   - If payment fails: show error and return to payment step
   - If payment succeeds: create order
7. System sends confirmation email
8. Display order confirmation page

Use different colors for user actions, system processes, and decision points.
```

### Expected Output
- Professional HTML file with SVG flowchart
- Color-coded nodes by type (user action, system process, decision)
- Clear arrows showing flow direction
- Decision diamonds with Yes/No branches
- Error handling paths
- Legend explaining colors and symbols

---

## 3. Dashboard Creator

**When to use:** Metrics dashboards, KPI displays, monitoring interfaces, analytics views, system health displays

### Example Prompts

**Simple:**
```
Create a dashboard showing server performance metrics
```

**Detailed:**
```
Create a system monitoring dashboard with the following metrics:

**System Health:**
- CPU Usage: 45% (normal)
- Memory Usage: 68% (warning)
- Disk Usage: 52% (good)
- Network I/O: 2.3 GB/s (normal)

**Application Metrics:**
- Active Users: 1,247
- Requests/sec: 3,421
- Average Response Time: 142ms
- Error Rate: 0.3%

**Database Performance:**
- Query Performance: 23ms avg (excellent)
- Active Connections: 45/100 (45%)
- Cache Hit Rate: 94%

Use color coding (green/yellow/red) based on status and include progress bars for percentage metrics.
```

### Expected Output
- Professional HTML dashboard with metric cards
- Color-coded status indicators (green/yellow/red)
- Progress bars for percentage values
- SVG charts for data visualization
- Clean grid layout
- Responsive design

---

## 4. Timeline Creator

**When to use:** Project timelines, roadmaps, Gantt charts, milestone tracking, release schedules, project planning

### Example Prompts

**Simple:**
```
Create a timeline for our Q1 2025 product launch
```

**Detailed:**
```
Create a product development timeline from October 2024 to June 2025:

**Q4 2024:**
- Oct 2024: Project kickoff and requirements gathering
- Nov 2024: Design system and wireframes complete
- Dec 2024: MVP development begins

**Q1 2025:**
- Jan 2025: Core features development
  - User authentication system
  - Dashboard implementation
  - API integration
- Feb 2025: Beta testing phase
  - Internal testing
  - Bug fixes and optimization
- Mar 2025: Beta user feedback and iterations

**Q2 2025:**
- Apr 2025: Final testing and polish
- May 2025: Marketing campaign launch
- Jun 2025: Public release v1.0

Show completed milestones in green, current work in yellow, and future work in gray.
```

### Expected Output
- Professional HTML timeline with milestone markers
- Color-coded by status (completed, in progress, pending)
- Chronological flow (horizontal or vertical)
- Grouped events by phase/quarter
- Clear date labels
- Visual distinction between major and minor milestones

---

## 5. Technical Documentation Creator

**When to use:** API documentation, developer guides, code examples, system architecture docs, integration guides

### Example Prompts

**Simple:**
```
Create technical documentation for our REST API authentication endpoint
```

**Detailed:**
```
Create API documentation for the User Management Service:

**Base URL:** https://api.example.com/v1

**Authentication:** Bearer token in Authorization header

**Endpoints:**

1. GET /users
   - Description: Retrieve paginated list of users
   - Query Parameters:
     - page (integer, optional): Page number, default 1
     - limit (integer, optional): Items per page, default 20, max 100
     - role (string, optional): Filter by role (admin, user, guest)
   - Response 200:
     {
       "users": [
         {"id": "usr_123", "email": "user@example.com", "role": "user"}
       ],
       "pagination": {"page": 1, "total_pages": 5, "total_items": 98}
     }

2. POST /users
   - Description: Create a new user
   - Request Body:
     {
       "email": "newuser@example.com",
       "password": "secure_password",
       "role": "user"
     }
   - Response 201: User object with generated ID
   - Errors: 400 (validation), 409 (email exists)

3. GET /users/:id
   - Get specific user by ID
   - Response 200: User object
   - Errors: 404 (not found)

**Rate Limiting:** 1000 requests/hour per API key

Include code examples in JavaScript and Python.
```

### Expected Output
- Professional HTML technical documentation
- Table of contents with navigation
- Color-coded HTTP methods (GET, POST, PUT, DELETE)
- Syntax-highlighted JSON examples
- Parameter tables with types and descriptions
- Request/response examples
- Error documentation with status codes
- Code snippets in multiple languages
- Clean, readable typography

---

## Tips for Best Results

### General Guidelines

1. **Be specific about data**: Provide actual values, labels, and names rather than placeholders
2. **Specify colors/themes**: Mention color schemes or status indicators you want
3. **Include hierarchy**: Describe relationships, groupings, or phases
4. **Mention interactivity**: Ask for legends, tooltips, or navigation if needed

### Architecture Diagrams
- Describe the project's purpose and users
- List all data sources and outputs
- Mention key technologies and frameworks
- Identify processing stages or components
- Note any external services or APIs

### Flowcharts
- List all steps in order
- Identify decision points clearly
- Specify error/alternative paths
- Mention any actors or swimlanes

### Dashboards
- Provide metric names and current values
- Indicate thresholds (good/warning/critical)
- Specify chart types if you have preferences
- Group related metrics together

### Timelines
- Give specific dates or time ranges
- Indicate status of each milestone
- Group events by phase or category
- Mention dependencies if relevant

### Technical Docs
- Include all endpoints/functions
- Provide example inputs and outputs
- List all parameters with types
- Show error scenarios
- Mention authentication requirements

---

## Customization

All skills support customization through natural language:

```
Create a flowchart for login process with a dark theme
```

```
Create a dashboard with blue gradient metric cards
```

```
Create a timeline in vertical layout instead of horizontal
```

```
Create API docs with curl examples instead of JavaScript
```

---

## Output Location

Generated HTML files are saved to:
- Current working directory by default
- User-specified location if provided in prompt
- Each file is self-contained with embedded CSS and SVG

---

## Browser Compatibility

All generated HTML files work in:
- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers (responsive design)

No external dependencies required - all styles and graphics are embedded.
