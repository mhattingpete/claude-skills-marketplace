---
name: timeline-creator
description: Create stunning HTML timelines and project roadmaps with Gantt charts, milestones, phase groupings, and progress indicators. Use when users explicitly request timelines, roadmaps, Gantt charts, project schedules, or milestone visualizations in HTML format.
---

# Timeline Creator

Create professional HTML timelines and project roadmaps with Gantt charts, milestone markers, phase groupings, progress indicators, and dependency arrows.

## When to Use This Skill

Activate this skill when users request:
- "Create a timeline for [project]"
- "Generate a roadmap showing [milestones]"
- "Make a Gantt chart for [schedule]"
- "Build a project timeline with [phases]"
- "Create a visual schedule for [plan]"

## Capabilities

### Timeline Components

**Horizontal Timelines:**
- Left-to-right progression
- Time period markers (months, quarters, years)
- Milestone circles with labels
- Progress bars showing completion
- Current date indicators

**Vertical Timelines:**
- Top-to-bottom progression
- Event boxes with dates
- Connecting vertical line
- Status indicators
- Expandable detail sections

**Gantt Charts:**
- Task bars with duration
- Start and end dates
- Dependencies between tasks
- Resource allocation
- Progress tracking

**Roadmap Views:**
- Quarterly or monthly groupings
- Feature cards with descriptions
- Priority indicators
- Release milestones
- Phase transitions

### Design Features

**Color System:**
- Completed: `#48bb78` (green)
- In Progress: `#f59e0b` (amber)
- Pending/Planned: `#cbd5e0` (gray)
- Critical: `#f56565` (red)
- Standard: `#4299e1` (blue)
- Special: `#9f7aea` (purple)

**Layout:**
- Responsive scaling
- Auto-adjusting to content length
- Flexible spacing
- Mobile-friendly horizontal scrolling

## Workflow

### Step 1: Understand the Timeline

Analyze the user's request to identify:
- **Time span**: Days, weeks, months, quarters, years?
- **Events/Milestones**: What needs to be shown?
- **Status**: What's completed, in progress, pending?
- **Dependencies**: Are there task dependencies?
- **Actors**: Single team or multiple teams/swimlanes?

### Step 2: Choose Timeline Type

**Horizontal Timeline (Recommended for):**
- Project overviews
- Historical events
- Release schedules
- Sequential milestones
- Time spans: months to years

**Vertical Timeline (Recommended for):**
- Detailed event descriptions
- Chronological stories
- Process documentation
- Long lists of events
- Mobile-first displays

**Gantt Chart (Recommended for):**
- Project management
- Task dependencies
- Resource planning
- Parallel work streams
- Detailed schedules

**Roadmap View (Recommended for):**
- Product planning
- Feature releases
- Strategic initiatives
- Quarterly goals
- Executive presentations

### Step 3: Build HTML Structure

Use the base template from `../visual-html-creator/assets/templates/base_template.html` for the HTML/CSS framework.

Use timeline components from `../visual-html-creator/assets/templates/timeline_components.html` for timeline patterns.

Reference design patterns from `../visual-html-creator/references/design_patterns.md` for colors and spacing.

Reference SVG techniques from `../visual-html-creator/references/svg_library.md` for shapes and connectors.

**Standard structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Timeline Title]</title>
    <style>
        /* Embedded CSS from base template */
    </style>
</head>
<body>
    <div class="container">
        <h1>[Project/Timeline Name]</h1>
        <p class="subtitle">[Time period or description]</p>

        <!-- Optional: Summary metrics -->
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-value">[Number]</div>
                <div class="metric-label">[Label]</div>
            </div>
        </div>

        <!-- Main timeline -->
        <div class="section">
            <h2 class="section-title">Timeline</h2>
            <div class="diagram-container">
                <svg viewBox="0 0 1200 400">
                    <!-- Timeline content -->
                </svg>
            </div>
        </div>

        <!-- Legend -->
        <div class="legend">
            <div class="legend-item">
                <div class="legend-box" style="background: #48bb78;"></div>
                <span>Completed</span>
            </div>
            <!-- More legend items -->
        </div>
    </div>
</body>
</html>
```

### Step 4: Create Horizontal Timeline

**Basic horizontal timeline:**
```xml
<svg viewBox="0 0 1200 400">
    <!-- Title -->
    <text x="600" y="30" text-anchor="middle" font-size="20"
          font-weight="bold" fill="#2d3748">
        Project Timeline
    </text>

    <!-- Main timeline bar -->
    <rect x="100" y="180" width="1000" height="20" rx="10" fill="#e2e8f0"/>
    <!-- Progress (60%) -->
    <rect x="100" y="180" width="600" height="20" rx="10" fill="#4299e1"/>

    <!-- Current date indicator -->
    <line x1="700" y1="150" x2="700" y2="230" stroke="#f56565"
          stroke-width="3" stroke-dasharray="5,5"/>
    <text x="700" y="140" text-anchor="middle" font-size="12"
          fill="#f56565" font-weight="bold">
        TODAY
    </text>

    <!-- Milestone 1 (completed) -->
    <circle cx="200" cy="190" r="15" fill="#48bb78"
            stroke="#2f855a" stroke-width="3"/>
    <text x="200" y="250" text-anchor="middle" font-size="14"
          fill="#2d3748" font-weight="bold">
        Q1
    </text>
    <text x="200" y="270" text-anchor="middle" font-size="12"
          fill="#718096">
        Planning
    </text>
    <text x="200" y="120" text-anchor="middle" font-size="11"
          fill="#48bb78" font-weight="bold">
        ✓ Complete
    </text>

    <!-- Milestone 2 (completed) -->
    <circle cx="450" cy="190" r="15" fill="#48bb78"
            stroke="#2f855a" stroke-width="3"/>
    <text x="450" y="250" text-anchor="middle" font-size="14"
          fill="#2d3748" font-weight="bold">
        Q2
    </text>
    <text x="450" y="270" text-anchor="middle" font-size="12"
          fill="#718096">
        Development
    </text>
    <text x="450" y="120" text-anchor="middle" font-size="11"
          fill="#48bb78" font-weight="bold">
        ✓ Complete
    </text>

    <!-- Milestone 3 (in progress) -->
    <circle cx="700" cy="190" r="15" fill="#f59e0b"
            stroke="#d97706" stroke-width="3"/>
    <text x="700" y="250" text-anchor="middle" font-size="14"
          fill="#2d3748" font-weight="bold">
        Q3
    </text>
    <text x="700" y="270" text-anchor="middle" font-size="12"
          fill="#718096">
        Testing
    </text>
    <text x="700" y="120" text-anchor="middle" font-size="11"
          fill="#f59e0b" font-weight="bold">
        ⟳ In Progress
    </text>

    <!-- Milestone 4 (pending) -->
    <circle cx="950" cy="190" r="15" fill="#cbd5e0"
            stroke="#a0aec0" stroke-width="3"/>
    <text x="950" y="250" text-anchor="middle" font-size="14"
          fill="#2d3748" font-weight="bold">
        Q4
    </text>
    <text x="950" y="270" text-anchor="middle" font-size="12"
          fill="#718096">
        Launch
    </text>
    <text x="950" y="120" text-anchor="middle" font-size="11"
          fill="#718096">
        Pending
    </text>
</svg>
```

### Step 5: Create Vertical Timeline

**Vertical timeline with event boxes:**
```xml
<svg viewBox="0 0 800 1000">
    <!-- Title -->
    <text x="400" y="30" text-anchor="middle" font-size="20"
          font-weight="bold" fill="#2d3748">
        Project History
    </text>

    <!-- Vertical line -->
    <line x1="100" y1="80" x2="100" y2="950" stroke="#e2e8f0" stroke-width="4"/>

    <!-- Event 1 (completed) -->
    <circle cx="100" cy="120" r="12" fill="#48bb78"
            stroke="#2f855a" stroke-width="3"/>
    <rect x="140" y="80" width="600" height="80" rx="10"
          fill="#e6f4ea" stroke="#48bb78" stroke-width="2"/>
    <text x="160" y="105" font-size="14" fill="#2d3748" font-weight="bold">
        Phase 1: Requirements Gathering
    </text>
    <text x="160" y="130" font-size="12" fill="#718096">
        January 2025 • Duration: 2 weeks
    </text>
    <text x="160" y="150" font-size="11" fill="#48bb78" font-weight="bold">
        ✓ Completed
    </text>

    <!-- Event 2 (completed) -->
    <circle cx="100" cy="250" r="12" fill="#48bb78"
            stroke="#2f855a" stroke-width="3"/>
    <rect x="140" y="210" width="600" height="80" rx="10"
          fill="#e6f4ea" stroke="#48bb78" stroke-width="2"/>
    <text x="160" y="235" font-size="14" fill="#2d3748" font-weight="bold">
        Phase 2: Design & Architecture
    </text>
    <text x="160" y="260" font-size="12" fill="#718096">
        February 2025 • Duration: 3 weeks
    </text>
    <text x="160" y="280" font-size="11" fill="#48bb78" font-weight="bold">
        ✓ Completed
    </text>

    <!-- Event 3 (in progress) -->
    <circle cx="100" cy="400" r="12" fill="#f59e0b"
            stroke="#d97706" stroke-width="3"/>
    <rect x="140" y="360" width="600" height="80" rx="10"
          fill="#fffbeb" stroke="#f59e0b" stroke-width="2"/>
    <text x="160" y="385" font-size="14" fill="#2d3748" font-weight="bold">
        Phase 3: Development Sprint 1
    </text>
    <text x="160" y="410" font-size="12" fill="#718096">
        March 2025 • Duration: 4 weeks
    </text>
    <text x="160" y="430" font-size="11" fill="#f59e0b" font-weight="bold">
        ⟳ In Progress (60% complete)
    </text>

    <!-- More events... -->
</svg>
```

### Step 6: Create Gantt Chart

**Gantt chart with task bars:**
```xml
<svg viewBox="0 0 1200 600">
    <!-- Title -->
    <text x="600" y="30" text-anchor="middle" font-size="20"
          font-weight="bold" fill="#2d3748">
        Project Gantt Chart
    </text>

    <!-- Header row -->
    <rect x="50" y="60" width="250" height="40" fill="#667eea"/>
    <text x="175" y="85" text-anchor="middle" fill="white"
          font-size="14" font-weight="bold">
        Task Name
    </text>

    <!-- Month headers -->
    <rect x="300" y="60" width="200" height="40" fill="#764ba2"/>
    <text x="400" y="85" text-anchor="middle" fill="white"
          font-size="14" font-weight="bold">
        Jan
    </text>

    <rect x="500" y="60" width="200" height="40" fill="#764ba2"/>
    <text x="600" y="85" text-anchor="middle" fill="white"
          font-size="14" font-weight="bold">
        Feb
    </text>

    <rect x="700" y="60" width="200" height="40" fill="#764ba2"/>
    <text x="800" y="85" text-anchor="middle" fill="white"
          font-size="14" font-weight="bold">
        Mar
    </text>

    <!-- Task 1 (completed) -->
    <rect x="50" y="100" width="250" height="60" fill="#f7fafc"
          stroke="#e2e8f0" stroke-width="1"/>
    <text x="70" y="135" font-size="13" fill="#2d3748" font-weight="500">
        Requirements Analysis
    </text>

    <rect x="300" y="100" width="1100" height="60" fill="#fff"
          stroke="#e2e8f0" stroke-width="1"/>
    <rect x="310" y="115" width="180" height="30" rx="5" fill="#48bb78"/>
    <text x="400" y="135" text-anchor="middle" fill="white"
          font-size="11" font-weight="bold">
        ✓ Complete
    </text>

    <!-- Task 2 (in progress) -->
    <rect x="50" y="160" width="250" height="60" fill="#f7fafc"
          stroke="#e2e8f0" stroke-width="1"/>
    <text x="70" y="195" font-size="13" fill="#2d3748" font-weight="500">
        Development Sprint 1
    </text>

    <rect x="300" y="160" width="1100" height="60" fill="#fff"
          stroke="#e2e8f0" stroke-width="1"/>
    <rect x="510" y="175" width="380" height="30" rx="5" fill="#f59e0b"/>
    <text x="700" y="195" text-anchor="middle" fill="white"
          font-size="11" font-weight="bold">
        ⟳ In Progress (65%)
    </text>

    <!-- Dependency arrow -->
    <defs>
        <marker id="dep-arrow" markerWidth="8" markerHeight="8"
                refX="7" refY="3" orient="auto">
            <polygon points="0 0, 8 3, 0 6" fill="#9f7aea"/>
        </marker>
    </defs>
    <path d="M 400 160 L 400 175" stroke="#9f7aea" stroke-width="2"
          marker-end="url(#dep-arrow)" stroke-dasharray="4,2"/>
</svg>
```

### Step 7: Create Roadmap View

**Quarterly roadmap:**
```xml
<svg viewBox="0 0 1200 500">
    <!-- Title -->
    <text x="600" y="30" text-anchor="middle" font-size="20"
          font-weight="bold" fill="#2d3748">
        Product Roadmap 2025
    </text>

    <!-- Q1 -->
    <rect x="50" y="80" width="260" height="150" rx="15"
          fill="#e6f4ea" stroke="#48bb78" stroke-width="3"/>
    <text x="180" y="110" text-anchor="middle" font-size="18"
          fill="#2d3748" font-weight="bold">
        Q1 2025
    </text>
    <text x="180" y="135" text-anchor="middle" font-size="12"
          fill="#48bb78" font-weight="bold">
        ✓ COMPLETED
    </text>
    <text x="70" y="160" font-size="11" fill="#2d3748">
        • User authentication
    </text>
    <text x="70" y="180" font-size="11" fill="#2d3748">
        • Basic dashboard
    </text>
    <text x="70" y="200" font-size="11" fill="#2d3748">
        • API v1.0
    </text>

    <!-- Q2 (in progress) -->
    <rect x="340" y="80" width="260" height="150" rx="15"
          fill="#fffbeb" stroke="#f59e0b" stroke-width="3"/>
    <text x="470" y="110" text-anchor="middle" font-size="18"
          fill="#2d3748" font-weight="bold">
        Q2 2025
    </text>
    <text x="470" y="135" text-anchor="middle" font-size="12"
          fill="#f59e0b" font-weight="bold">
        ⟳ IN PROGRESS
    </text>
    <text x="360" y="160" font-size="11" fill="#2d3748">
        • Advanced analytics
    </text>
    <text x="360" y="180" font-size="11" fill="#2d3748">
        • Team collaboration
    </text>

    <!-- Q3 (planned) -->
    <rect x="630" y="80" width="260" height="150" rx="15"
          fill="#f7fafc" stroke="#cbd5e0" stroke-width="3"/>
    <text x="760" y="110" text-anchor="middle" font-size="18"
          fill="#2d3748" font-weight="bold">
        Q3 2025
    </text>
    <text x="760" y="135" text-anchor="middle" font-size="12"
          fill="#718096" font-weight="bold">
        PLANNED
    </text>

    <!-- Q4 (planned) -->
    <rect x="920" y="80" width="260" height="150" rx="15"
          fill="#f7fafc" stroke="#cbd5e0" stroke-width="3"/>
    <text x="1050" y="110" text-anchor="middle" font-size="18"
          fill="#2d3748" font-weight="bold">
        Q4 2025
    </text>
    <text x="1050" y="135" text-anchor="middle" font-size="12"
          fill="#718096" font-weight="bold">
        PLANNED
    </text>
</svg>
```

## Best Practices

### Timeline Design

**Chronological order:**
- Always flow left-to-right or top-to-bottom
- Maintain consistent spacing between events
- Align milestones to grid
- Use current date indicator when relevant

**Status clarity:**
- Use color consistently (green = done, amber = active, gray = pending)
- Include status text with symbols (✓, ⟳, ○)
- Show progress percentages when available
- Update regularly to maintain accuracy

### Information Density

**Keep it scannable:**
- Limit detail on timeline itself
- Use cards/boxes for descriptions
- Group related items visually
- Provide legends for symbols

**Balance detail:**
- High-level view: Major milestones only
- Medium view: Phases with key dates
- Detailed view: All tasks and dependencies
- Choose appropriate level for audience

### Time Scale Selection

**Days/Weeks:**
- Sprint planning
- Short-term projects
- Detailed schedules
- Operations timelines

**Months:**
- Project execution
- Release planning
- Development cycles
- Medium-term roadmaps

**Quarters/Years:**
- Strategic planning
- Product roadmaps
- Business planning
- Long-term vision

### Visual Hierarchy

**Size indicates importance:**
- Larger circles/boxes for major milestones
- Smaller markers for minor events
- Bold text for phase names
- Regular text for details

**Color indicates status:**
- Green for achievements
- Amber for current focus
- Gray for future plans
- Red for delays or issues

## Common Patterns

### Project Timeline
```
[Planning] → [Development] → [Testing] → [Launch]
   Q1            Q2              Q3         Q4
```

### Release Schedule
```
v1.0 (Jan) → v1.1 (Mar) → v2.0 (Jun) → v2.1 (Sep)
```

### Sprint Timeline
```
Sprint 1 | Sprint 2 | Sprint 3 | Sprint 4
[======] [======] [====  ] [      ]
```

### Multi-Track Roadmap
```
Feature Track: [Feature A] → [Feature B] → [Feature C]
Platform Track:   [Platform 1]    →    [Platform 2]
Infrastructure:      [Infrastructure Upgrade]
```

## Example Output Structure

**User request:** "Create a timeline for our product launch"

**Generated output includes:**
1. **Timeline visualization**: 6-month horizontal timeline
2. **Milestones**:
   - Month 1: Planning complete
   - Month 2-3: Development
   - Month 4: Testing
   - Month 5: Beta launch
   - Month 6: Public launch
3. **Status indicators**: Completed (green), in progress (amber), pending (gray)
4. **Current date marker**: Shows where we are now
5. **Legend**: Status meanings
6. **Summary metrics**: Days remaining, % complete

## Resources

This skill uses shared resources from the visual-html-creator skill:
- `../visual-html-creator/assets/templates/base_template.html` - CSS framework
- `../visual-html-creator/assets/templates/timeline_components.html` - Timeline patterns
- `../visual-html-creator/references/design_patterns.md` - Design system
- `../visual-html-creator/references/svg_library.md` - SVG techniques

## Troubleshooting

**Issue:** Timeline too crowded
- **Solution**: Reduce number of events, increase viewBox width, use abbreviations

**Issue:** Dates don't align
- **Solution**: Calculate positions proportionally, use grid system, verify math

**Issue:** Milestones overlap
- **Solution**: Increase spacing, stagger labels above/below line, reduce marker size

**Issue:** Timeline doesn't fit screen
- **Solution**: Make responsive with viewBox, enable horizontal scroll, split into multiple views
