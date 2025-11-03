# Visual Documentation Plugin

Create stunning visual HTML documentation with modern UI design, SVG diagrams, and interactive visualizations.

**Version:** 1.1.0

---

## Skills

### architecture-diagram-creator

**Activates when you say:**
- "Create an architecture diagram"
- "Generate a project architecture overview"
- "Document the system architecture"
- "Create a high-level system design"

**What it does:**
Creates comprehensive HTML architecture diagrams covering business objectives, data flows, processing pipelines, features (functional and non-functional), system architecture, deployment information, and reference tables. Perfect for documenting entire software projects.

---

### flowchart-creator

**Activates when you say:**
- "Create a flowchart for deployment"
- "Make a process flow diagram"
- "Generate a decision tree"

**What it does:**
Creates HTML flowcharts with color-coded stages, decision trees, arrows, and swimlanes.

---

### dashboard-creator

**Activates when you say:**
- "Create a dashboard for metrics"
- "Make a KPI visualization"
- "Generate a performance dashboard"

**What it does:**
Creates HTML dashboards with metric cards, charts, progress indicators, and data visualizations.

---

### technical-doc-creator

**Activates when you say:**
- "Create API documentation"
- "Document the architecture"
- "Generate technical docs"

**What it does:**
Creates comprehensive HTML documentation with code blocks, API workflows, and system diagrams.

---

### timeline-creator

**Activates when you say:**
- "Create a project timeline"
- "Make a roadmap"
- "Generate a Gantt chart"

**What it does:**
Creates HTML timelines and roadmaps with milestones, phase groupings, and progress indicators.

---

## Features

- Modern gradient design with semantic color system
- Responsive, mobile-first layout
- WCAG AA accessibility compliance
- Self-contained HTML (no external dependencies)
- SVG diagrams and visualizations

---

## Installation

Add to your `.claude-plugin/marketplace.json`:

```json
{
  "plugins": [
    {
      "name": "visual-documentation-plugin",
      "source": "github:anthropics/claude-skills-marketplace/visual-documentation-plugin",
      "version": "1.1.0"
    }
  ]
}
```

---

## Author

**mhattingpete**
