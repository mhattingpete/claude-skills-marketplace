---
name: dashboard-creator
description: Create stunning, interactive HTML dashboards with KPI metric cards, bar/pie/line charts, progress indicators, and data visualizations. Use when users request dashboards, metrics displays, KPI visualizations, data charts, or monitoring interfaces - regardless of whether they specify HTML format.
---

# Dashboard Creator

Create professional HTML dashboards with KPI metric cards, charts, progress indicators, and data visualizations using modern SVG graphics and gradient styling.

## When to Use This Skill

Activate this skill when users request:
- "Create a dashboard showing [metrics]"
- "Make a KPI dashboard for [data]"
- "Generate a metrics visualization for [statistics]"
- "Build a data dashboard with [charts]"
- "Create a visual display of [performance metrics]"

## Capabilities

### Dashboard Components

**Metric Cards:**
- Large numeric displays with gradient backgrounds
- Labels and subtitles
- Icon or emoji indicators
- Color-coded by status or category
- Responsive grid layout

**Charts:**
- Bar charts (vertical and horizontal)
- Pie/donut charts
- Line charts with data points
- Progress bars and gauges
- Radial progress indicators

**Status Indicators:**
- Traffic light style (good/warning/critical)
- Percentage displays
- Trend arrows (up/down)
- Comparison tables

### Design Features

**Color System:**
- Success/Positive: `#48bb78` (green)
- Warning/Attention: `#f59e0b` (amber)
- Info/Standard: `#4299e1` (blue)
- Error/Critical: `#f56565` (red)
- Secondary: `#ed8936` (orange)
- Accent: `#9f7aea` (purple)

**Layout:**
- Responsive grid (1-4 columns)
- Mobile-first design
- Auto-adjusting card sizes
- Flexible spacing

## Workflow

### Step 1: Understand the Data

Analyze the user's request to identify:
- **Metrics**: What numbers need to be displayed?
- **Categories**: How are metrics grouped?
- **Relationships**: Which metrics compare to each other?
- **Trends**: Is time-series data involved?
- **Goals/Targets**: Are there benchmarks or thresholds?

### Step 2: Choose Dashboard Layout

**Metric Grid (Top):**
```
[Card 1] [Card 2] [Card 3] [Card 4]
```
Use for: Key performance indicators, headline numbers

**Charts Below:**
```
[Metric Cards Row]
[Chart 1]     [Chart 2]
[Chart 3 spanning full width]
```
Use for: Supporting visualizations, trend analysis

**Comparison Layout:**
```
[Metric Cards]
[Before/After or Target/Actual Comparison]
[Detailed Breakdown Chart]
```
Use for: Performance tracking, goal comparison

**Multi-Section:**
```
[Overview Cards]
[Section 1: Charts]
[Section 2: Tables]
[Section 3: Details]
```
Use for: Comprehensive dashboards, executive summaries

### Step 3: Build HTML Structure

Use the base template from `../visual-html-creator/assets/templates/base_template.html` for the HTML/CSS framework.

Use dashboard components from `../visual-html-creator/assets/templates/dashboard_components.html` for charts and metrics.

Reference design patterns from `../visual-html-creator/references/design_patterns.md` for colors and spacing.

Reference SVG techniques from `../visual-html-creator/references/svg_library.md` for chart creation.

**Standard structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Dashboard Title]</title>
    <style>
        /* Embedded CSS from base template */
    </style>
</head>
<body>
    <div class="container">
        <h1>[Dashboard Name]</h1>
        <p class="subtitle">[Time period or description]</p>

        <!-- Metric Cards -->
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-value">[Number]</div>
                <div class="metric-label">[Label]</div>
            </div>
            <!-- More cards -->
        </div>

        <!-- Charts Section -->
        <div class="section">
            <h2 class="section-title">Detailed Analysis</h2>
            <div class="diagram-container">
                <svg viewBox="0 0 1200 400">
                    <!-- Chart content -->
                </svg>
            </div>
        </div>

        <!-- Legend or Notes -->
        <div class="legend">
            <!-- Legend items -->
        </div>
    </div>
</body>
</html>
```

### Step 4: Create Metric Cards

**Standard metric card:**
```html
<div class="metric-card">
    <div class="metric-value">1,234</div>
    <div class="metric-label">Total Users</div>
</div>
```

**With custom color:**
```html
<div class="metric-card" style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);">
    <div class="metric-value">✓ 98%</div>
    <div class="metric-label">Uptime<br><small>Last 30 days</small></div>
</div>
```

**Color selection:**
- Green gradient: Positive metrics (revenue, growth, completion)
- Red gradient: Critical metrics (errors, failures, alerts)
- Blue gradient: Neutral metrics (users, items, totals)
- Amber gradient: Warning metrics (pending, review needed)

### Step 5: Create Charts

**Bar Chart pattern:**
```xml
<svg viewBox="0 0 1200 400">
    <!-- Title -->
    <text x="600" y="30" text-anchor="middle" font-size="20"
          font-weight="bold" fill="#2d3748">
        Chart Title
    </text>

    <!-- Axes -->
    <line x1="100" y1="350" x2="1100" y2="350"
          stroke="#2d3748" stroke-width="2"/>
    <line x1="100" y1="350" x2="100" y2="80"
          stroke="#2d3748" stroke-width="2"/>

    <!-- Bar -->
    <rect x="200" y="150" width="200" height="200" rx="5"
          fill="#4299e1" stroke="#2b6cb0" stroke-width="2"/>
    <text x="300" y="260" text-anchor="middle" fill="white"
          font-size="24" font-weight="bold">
        456
    </text>
    <text x="300" y="380" text-anchor="middle" font-size="14"
          fill="#2d3748">
        Category A
    </text>
</svg>
```

**Progress Bar pattern:**
```xml
<text x="50" y="100" font-size="14" fill="#2d3748" font-weight="500">
    Task Completion
</text>
<!-- Background -->
<rect x="150" y="80" width="800" height="40" rx="20" fill="#e2e8f0"/>
<!-- Progress (75%) -->
<rect x="150" y="80" width="600" height="40" rx="20" fill="#48bb78"/>
<text x="970" y="105" font-size="14" fill="#2d3748" font-weight="bold">
    75%
</text>
```

**Gauge/Radial Progress:**
```xml
<svg viewBox="0 0 400 300">
    <text x="200" y="30" text-anchor="middle" font-size="18"
          font-weight="bold" fill="#2d3748">
        System Health
    </text>

    <!-- Background arc -->
    <path d="M 100 200 A 100 100 0 0 1 300 200"
          stroke="#e2e8f0" stroke-width="30" fill="none"
          stroke-linecap="round"/>

    <!-- Progress arc (75%) -->
    <path d="M 100 200 A 100 100 0 1 1 271 129"
          stroke="#48bb78" stroke-width="30" fill="none"
          stroke-linecap="round"/>

    <!-- Center text -->
    <text x="200" y="190" text-anchor="middle" font-size="48"
          font-weight="bold" fill="#2d3748">
        75%
    </text>
    <text x="200" y="215" text-anchor="middle" font-size="14"
          fill="#718096">
        Excellent
    </text>
</svg>
```

### Step 6: Add Context and Insights

**Comparison Indicators:**
- Show vs previous period: "↑ 12% vs last month"
- Show vs target: "95% of 100% goal"
- Color code: Green for above target, red for below

**Status Messages:**
- Good: "✓ All systems operational"
- Warning: "⚠ 2 items need attention"
- Critical: "✗ 5 critical alerts"

**Time Context:**
- Include date range in subtitle
- Add "Last updated" timestamp in footer
- Show data freshness indicators

## Best Practices

### Metric Selection

**Choose the right metrics:**
- Focus on actionable insights
- Avoid vanity metrics
- Include both leading and lagging indicators
- Show trends over time when relevant

**Metric hierarchy:**
1. Primary KPIs (largest, most prominent)
2. Supporting metrics (medium size)
3. Detailed breakdowns (smaller, in sections)

### Visual Hierarchy

**Size and prominence:**
- Largest: Critical KPIs (metric cards at top)
- Medium: Charts showing trends or comparisons
- Smallest: Supporting details, legends, footnotes

**Color usage:**
- Consistent color = same meaning throughout
- Use sparingly: 3-4 colors maximum in a single chart
- Reserve red for alerts/problems only
- Green for positive/success consistently

### Layout Guidelines

**Spacing:**
- 20px gap between metric cards
- 40-60px between major sections
- 30px padding in diagram containers
- Generous whitespace for readability

**Responsiveness:**
- Metric grid: 4 columns desktop → 2 columns tablet → 1 column mobile
- Charts scale proportionally with viewBox
- Stack sections vertically on narrow screens

**Alignment:**
- Center-align metric card content
- Left-align chart titles
- Grid-align multiple charts horizontally
- Maintain consistent baseline

### Data Presentation

**Number formatting:**
- Large numbers: Use commas (1,234) or abbreviations (1.2K)
- Percentages: Include % symbol
- Currency: Include symbol and appropriate decimals
- Decimals: Limit to 1-2 places unless precision is critical

**Clarity:**
- Label everything explicitly
- Include units (ms, MB, $, users, etc.)
- Provide legends for color-coded data
- Add tooltips or annotations for complex metrics

## Common Patterns

### Executive Dashboard
```
[Revenue] [Users] [Growth] [Conversion]
[Revenue Trend Chart - Line Graph]
[User Acquisition - Bar Chart]
```

### Performance Dashboard
```
[Uptime] [Response Time] [Error Rate] [Throughput]
[System Health Gauge]
[Performance Over Time - Line Chart]
```

### Project Dashboard
```
[Tasks Complete] [In Progress] [Blocked] [Overdue]
[Progress by Phase - Horizontal Bars]
[Team Workload - Stacked Bar]
```

### Sales Dashboard
```
[Total Sales] [New Customers] [Avg Order Value] [Conversion Rate]
[Sales by Product - Pie Chart]
[Monthly Trend - Line Chart]
[Top Performers - Table]
```

## Example Output Structure

**User request:** "Create a dashboard showing website analytics"

**Generated output includes:**
1. **Metric Cards (Top)**:
   - Total Visitors: 12,450
   - Page Views: 45,230
   - Bounce Rate: 32%
   - Avg Session: 4:32
2. **Charts**:
   - Traffic over time (line chart)
   - Top pages (bar chart)
   - Traffic sources (pie chart)
3. **Context**:
   - Date range: "Last 30 days"
   - Comparisons: "↑ 12% vs previous period"
   - Status: "All tracking active"
4. **Legend**: Color meanings

## Resources

This skill uses shared resources from the visual-html-creator skill:
- `../visual-html-creator/assets/templates/base_template.html` - CSS framework
- `../visual-html-creator/assets/templates/dashboard_components.html` - Chart patterns
- `../visual-html-creator/references/design_patterns.md` - Design system
- `../visual-html-creator/references/svg_library.md` - SVG techniques

## Troubleshooting

**Issue:** Numbers don't fit in metric cards
- **Solution**: Use abbreviations (K, M, B), reduce font size, or split into multiple cards

**Issue:** Chart bars overlap
- **Solution**: Increase viewBox width, reduce number of bars, or rotate labels

**Issue:** Colors look too similar
- **Solution**: Use high contrast combinations, reference semantic color palette

**Issue:** Dashboard looks cluttered
- **Solution**: Limit to 3-4 main metrics, use white space, group related items
