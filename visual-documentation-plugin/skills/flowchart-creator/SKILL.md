---
name: flowchart-creator
description: Create stunning HTML flowcharts and process flow diagrams with decision trees, color-coded stages, arrows, and swimlanes. Use when users explicitly request visual flowcharts, process diagrams, workflow visualizations, or decision trees in HTML format.
---

# Flowchart Creator

Create professional HTML flowcharts and process flow diagrams with modern SVG graphics, decision trees, color-coded stages, arrows, and swimlane layouts.

## When to Use This Skill

Activate this skill when users request:
- "Create a flowchart for [process]"
- "Generate a process flow diagram showing [steps]"
- "Make a visual workflow for [system]"
- "Build a decision tree for [logic]"
- "Create a swimlane diagram for [multi-team process]"

## Capabilities

### Flowchart Components

**Process Boxes:**
- Rounded rectangles with labels
- Color-coded by status or type
- Multi-line text support
- Status indicators (success, in-progress, pending, error)

**Decision Diamonds:**
- Yes/No branching logic
- Multiple outcome paths
- Conditional routing
- Clear labeling on branches

**Connectors:**
- Straight arrows (horizontal, vertical, diagonal)
- L-shaped connectors for layout flexibility
- Curved connectors for complex flows
- Dashed lines for optional/uncertain paths

**Start/End Nodes:**
- Circular start nodes
- Terminal end nodes
- Color differentiation

**Swimlanes:**
- Horizontal or vertical lanes
- Department/role separation
- Cross-lane connectors
- Background shading for clarity

### Design Features

**Color System:**
- Success/Completed: `#48bb78` (green)
- Warning/Attention: `#f59e0b` (amber)
- Info/Standard: `#4299e1` (blue)
- Error/Failed: `#f56565` (red)
- Process/Active: `#ed8936` (orange)
- Special/Highlight: `#9f7aea` (purple)

**Layout:**
- Responsive SVG with viewBox scaling
- Auto-adjusting to container width
- Maintains aspect ratio
- Mobile-friendly design

## Workflow

### Step 1: Understand the Process

Analyze the user's request to identify:
- **Process steps**: What actions occur?
- **Decision points**: Where are choices made?
- **Flow direction**: Linear, branching, or circular?
- **Actors/Roles**: Who performs each step?
- **Start and end points**: Where does the process begin and end?

### Step 2: Choose Layout Pattern

**Linear Flow (Left to Right):**
```
Start → Step 1 → Step 2 → Decision → End
```
Use for: Simple sequential processes

**Vertical Flow (Top to Bottom):**
```
Start
  ↓
Step 1
  ↓
Step 2
  ↓
End
```
Use for: Hierarchical processes, top-down workflows

**Multi-Path Flow:**
```
         → Path A →
Start → Decision        → Merge → End
         → Path B →
```
Use for: Conditional logic, parallel processing

**Swimlane Layout:**
```
Team A: [Step 1] → [Step 3]
Team B:    ↓         ↓
        [Step 2] → [Step 4]
```
Use for: Cross-functional processes, multi-department workflows

### Step 3: Build HTML Structure

Use the base template from `../visual-html-creator/assets/templates/base_template.html` for the HTML/CSS framework.

Use flowchart components from `../visual-html-creator/assets/templates/flowchart_components.html` for SVG patterns.

Reference design patterns from `../visual-html-creator/references/design_patterns.md` for colors and spacing.

Reference SVG techniques from `../visual-html-creator/references/svg_library.md` for shapes and connectors.

**Standard structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Flowchart Title]</title>
    <style>
        /* Embedded CSS from base template */
    </style>
</head>
<body>
    <div class="container">
        <h1>[Process Name]</h1>
        <p class="subtitle">[Description]</p>

        <!-- Optional: Overview metrics -->
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-value">[Number]</div>
                <div class="metric-label">[Label]</div>
            </div>
        </div>

        <!-- Main flowchart -->
        <div class="section">
            <h2 class="section-title">Process Flow</h2>
            <div class="diagram-container">
                <svg viewBox="0 0 1200 800">
                    <defs>
                        <!-- Arrow markers -->
                        <marker id="arrowhead" markerWidth="10" markerHeight="10"
                                refX="9" refY="3" orient="auto">
                            <polygon points="0 0, 10 3, 0 6" fill="#2d3748"/>
                        </marker>
                    </defs>

                    <!-- Flowchart content -->
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

### Step 4: Create SVG Flowchart

**Process box pattern:**
```xml
<rect x="100" y="100" width="200" height="80" rx="10"
      fill="#4299e1" stroke="#2b6cb0" stroke-width="3"/>
<text x="200" y="135" text-anchor="middle" fill="white"
      font-size="14" font-weight="bold">
    Process Name
</text>
<text x="200" y="155" text-anchor="middle" fill="white" font-size="11">
    Subtitle or detail
</text>
```

**Decision diamond pattern:**
```xml
<path d="M 600 100 L 700 100 L 750 150 L 700 200 L 500 200 L 450 150 Z"
      fill="#fbbf24" stroke="#d97706" stroke-width="3"/>
<text x="600" y="155" text-anchor="middle" font-size="13" font-weight="bold">
    Decision?
</text>
```

**Arrow connector:**
```xml
<path d="M 300 140 L 450 140" stroke="#2d3748" stroke-width="3"
      marker-end="url(#arrowhead)"/>
<text x="375" y="130" text-anchor="middle" fill="#2d3748"
      font-weight="bold" font-size="12">
    YES
</text>
```

### Step 5: Add Interactivity (Optional)

**Status indicators:**
- ✓ Checkmarks for completed steps
- ⟳ Arrows for in-progress
- ⚠ Warning symbols for attention needed
- ✗ X marks for failed/blocked

**Annotations:**
- Callout boxes with additional details
- Dashed leader lines to relevant nodes
- Footnote references

### Step 6: Include Documentation

Add a legend explaining:
- Color meanings
- Symbol definitions
- Process flow direction
- Special cases or exceptions

Add a footer with:
- Process name and version
- Last updated date
- Contact or reference information

## Best Practices

### Layout Guidelines

**Spacing:**
- Minimum 100px between major nodes
- 50px padding around diagram edges
- 20px gap for branch labels
- Consistent node sizes within categories

**Text Sizing:**
- Node labels: 14-16px
- Decision text: 12-14px
- Branch labels: 11-12px
- Annotations: 10-11px

**Alignment:**
- Horizontal flows: align nodes to grid
- Vertical flows: center-align when possible
- Keep connectors orthogonal (90° angles) when feasible
- Group related steps visually

### Color Usage

**Semantic meaning:**
- Use green for successful/completed paths
- Use red for error/failure paths
- Use amber for warnings/attention
- Use blue for standard/neutral paths
- Use purple for special/optional paths

**Consistency:**
- Same color = same status across entire diagram
- Provide legend if using multiple colors
- Ensure 4.5:1 contrast ratio for text on colored backgrounds

### Complexity Management

**For simple processes (3-8 steps):**
- Single linear or branching flow
- Minimal decision points
- Clear start and end

**For medium processes (9-20 steps):**
- Group related steps visually
- Use color coding for stages
- Add section labels
- Include intermediate milestones

**For complex processes (20+ steps):**
- Consider multiple diagrams (high-level + detailed views)
- Use swimlanes for multi-actor processes
- Add collapsible/expandable sections in description
- Provide process overview before detailed diagram

## Common Patterns

### Linear Workflow
```
[Start] → [Step 1] → [Step 2] → [Step 3] → [End]
```

### Conditional Branch
```
              → [Success Path] →
[Start] → [Decision]              [Merge] → [End]
              → [Failure Path] →
```

### Loop/Iteration
```
[Start] → [Process] → [Check] → [Continue?]
                        ↑            ↓ No
                        └────[Yes]───┘
```

### Parallel Processing
```
           → [Task A] →
[Start] →  → [Task B] →  → [Merge] → [End]
           → [Task C] →
```

### Swimlane Multi-Actor
```
Actor A: [Task 1] ──→ [Task 3]
Actor B:    ↓           ↓
         [Task 2] ──→ [Task 4]
```

## Example Output Structure

**User request:** "Create a flowchart for our order processing system"

**Generated output includes:**
1. **Title and description**: "Order Processing Workflow"
2. **Process steps**:
   - Order received
   - Validate payment
   - Check inventory
   - Process fulfillment
   - Ship order
3. **Decision points**:
   - Payment valid?
   - Items in stock?
   - Shipping address valid?
4. **Error paths**:
   - Payment failed → Notify customer
   - Out of stock → Backorder or cancel
5. **Legend**: Color meanings and symbols
6. **Footer**: Process version and last updated

## Resources

This skill uses shared resources from the visual-html-creator skill:
- `../visual-html-creator/assets/templates/base_template.html` - CSS framework
- `../visual-html-creator/assets/templates/flowchart_components.html` - SVG patterns
- `../visual-html-creator/references/design_patterns.md` - Design system
- `../visual-html-creator/references/svg_library.md` - SVG techniques

## Troubleshooting

**Issue:** Arrows not pointing correctly
- **Solution**: Adjust marker refX/refY values, check path endpoints

**Issue:** Text overlapping nodes
- **Solution**: Increase viewBox size, adjust font sizes, shorten labels

**Issue:** Layout looks cramped
- **Solution**: Increase spacing between nodes (100-150px), expand viewBox

**Issue:** Diagram too wide/tall
- **Solution**: Reorganize into multi-level flow, use swimlanes, split into multiple diagrams
