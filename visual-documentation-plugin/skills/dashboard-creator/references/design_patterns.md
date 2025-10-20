# Design Patterns Reference

Complete design system guidelines for creating visually stunning HTML documentation.

## Color System

### Primary Palette

**Gradient Background:**
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```
- Use for: Body background, primary branding elements
- Creates depth and visual interest

**Accent Colors:**
- Primary Purple-Blue: `#667eea`
- Secondary Purple: `#764ba2`
- Use for: Headings, borders, key UI elements

### Semantic Color Scales

#### Success / Confirmed / Positive
- **Base:** `#48bb78` (green)
- **Dark:** `#2f855a` (darker green, for strokes)
- **Light:** `#e6f4ea` (pale green, for backgrounds)
- Use for: Completed tasks, success messages, positive metrics

#### Warning / Uncertain / Attention
- **Base:** `#f59e0b` (amber)
- **Dark:** `#d97706` (darker amber, for strokes)
- **Light:** `#fffbeb` (pale amber, for backgrounds)
- Use for: In-progress items, warnings, items needing attention

#### Info / Primary / Standard
- **Base:** `#4299e1` (blue)
- **Dark:** `#2b6cb0` (darker blue, for strokes)
- **Light:** `#e6f2ff` (pale blue, for backgrounds)
- Use for: Standard information, primary actions, neutral states

#### Error / Critical / Negative
- **Base:** `#f56565` (red)
- **Dark:** `#c53030` (darker red, for strokes)
- **Light:** `#fff5f5` (pale red, for backgrounds)
- Use for: Errors, critical issues, failed states

#### Process / Action / Secondary
- **Base:** `#ed8936` (orange)
- **Dark:** `#c05621` (darker orange, for strokes)
- **Light:** `#fff5e6` (pale orange, for backgrounds)
- Use for: Processing states, secondary actions

#### Special / Highlight / Tertiary
- **Base:** `#9f7aea` (purple)
- **Dark:** `#6b46c1` (darker purple, for strokes)
- **Light:** `#f3e6ff` (pale purple, for backgrounds)
- Use for: Special features, highlights, premium items

### Neutral Palette

**Text Colors:**
- **Dark (Primary text):** `#2d3748` - Headings, important content
- **Medium (Secondary text):** `#718096` - Body text, labels
- **Light (Tertiary text):** `#a0aec0` - Captions, metadata

**UI Elements:**
- **Dark border:** `#cbd5e0`
- **Light border:** `#e2e8f0`
- **Dark background:** `#edf2f7`
- **Light background:** `#f7fafc`
- **White:** `#ffffff`

### Color Contrast Guidelines

**WCAG AA Compliance:**
- Minimum contrast ratio: 4.5:1 for normal text
- Large text (18pt+ or 14pt+ bold): 3:1 minimum
- Safe combinations:
  - Dark text (#2d3748) on light backgrounds (#f7fafc, #ffffff)
  - White text on colored backgrounds (all semantic base colors pass)
  - Medium text (#718096) on white only

## Typography

### Font Families

**Primary (Sans-serif):**
```css
font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
```
- Use for: All body text, headings, UI elements
- Fallback chain ensures availability across platforms

**Code (Monospace):**
```css
font-family: 'Courier New', monospace;
```
- Use for: Code blocks, technical data, fixed-width content

### Type Scale

**Display / Hero:**
- Size: `2.5em` (40px at 16px base)
- Weight: Bold (700)
- Use for: Page title (h1)
- Special effect: Gradient text clip

**Section Heading:**
- Size: `1.8em` (28.8px)
- Weight: Bold (700)
- Color: `#2d3748`
- Use for: Major sections (h2)
- Decoration: Bottom border `3px solid #667eea`

**Subsection:**
- Size: `1.4em` (22.4px)
- Weight: Bold (700)
- Color: `#2d3748`
- Use for: Subsections (h3)

**Body:**
- Size: `1em` (16px base)
- Weight: Normal (400)
- Line height: 1.6
- Color: `#2d3748` or `#4a5568`
- Use for: Paragraphs, general content

**Label / Caption:**
- Size: `0.9-0.95em` (14.4-15.2px)
- Weight: Normal (400) or Medium (500)
- Color: `#718096`
- Use for: Metric labels, chart labels, form labels

**Small / Meta:**
- Size: `0.85em` (13.6px)
- Weight: Normal (400)
- Color: `#a0aec0`
- Use for: Footnotes, timestamps, metadata

**SVG Text:**
- Small labels: `11-12px`
- Standard text: `13-14px`
- Emphasis: `15-16px`
- Large values: `18-24px`
- Metric displays: `48px+`

### Text Effects

**Gradient Text (for h1):**
```css
h1 {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
```

**Code Highlighting:**
```css
.highlight {
    color: #fbbf24;  /* Amber highlight */
    font-weight: bold;
}
```

## Spacing & Layout

### Container Sizing

**Max Width:**
- Container: `1400px`
- Comfortable reading: `800-1000px`
- Full width sections: No max-width

**Padding:**
- Desktop container: `40px`
- Mobile container: `20px`
- Diagram containers: `30px`
- Content boxes: `20px`
- Metric cards: `25px`

**Margins:**
- Section bottom: `60px`
- Element groups: `30px`
- Individual elements: `20px`
- Small gaps: `10px`

### Grid Systems

**Metric Grid:**
```css
display: grid;
grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
gap: 20px;
```
- Automatically responsive
- Minimum card width: 200px
- Equal width distribution

**Custom Grids:**
- 2-column: `grid-template-columns: 1fr 1fr;`
- 3-column: `grid-template-columns: repeat(3, 1fr);`
- Sidebar layout: `grid-template-columns: 300px 1fr;`

### Flexbox Patterns

**Horizontal Center:**
```css
display: flex;
justify-content: center;
align-items: center;
```

**Space Between:**
```css
display: flex;
justify-content: space-between;
align-items: center;
```

**Wrapped Row:**
```css
display: flex;
flex-wrap: wrap;
gap: 20px;
```

## Visual Effects

### Shadows

**Card Shadow:**
```css
box-shadow: 0 20px 60px rgba(0,0,0,0.3);
```
- Use for: Main container, elevated cards

**Metric Card Shadow:**
```css
box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
```
- Use for: Metric cards, smaller elevation

**Subtle Shadow:**
```css
box-shadow: 0 2px 8px rgba(0,0,0,0.1);
```
- Use for: Buttons, small cards, hover states

### Border Radius

**Large (Containers):**
- Container: `20px`
- Diagram containers: `15px`

**Medium (Cards & Boxes):**
- Metric cards: `15px`
- Content boxes: `10px`
- SVG shapes: `10px`

**Small (UI Elements):**
- Buttons: `8px`
- Small badges: `5px`

**Pills / Rounded:**
- Full rounded: `50%` (circles) or `9999px` (pills)
- Timeline progress bars: `20px`

### Opacity

**Overlays:**
- Light overlay: `0.3`
- Medium overlay: `0.5-0.6`
- Strong overlay: `0.8-0.9`

**Hover States:**
- Slight fade: `0.9`
- Clear fade: `0.7-0.8`

**Disabled:**
- `0.5-0.6`

## Responsive Breakpoints

### Mobile First Strategy

**Breakpoints:**
```css
/* Mobile: default styles, no media query needed */

/* Tablet */
@media (min-width: 768px) { ... }

/* Desktop */
@media (min-width: 1024px) { ... }

/* Large Desktop */
@media (min-width: 1440px) { ... }
```

**Common Pattern (Desktop First):**
```css
@media (max-width: 768px) {
    .container { padding: 20px; }
    h1 { font-size: 1.8em; }
    .section-title { font-size: 1.4em; }
    .metric-grid { grid-template-columns: 1fr; }
}
```

### Responsive Typography

**Desktop:**
- h1: `2.5em`
- h2: `1.8em`
- h3: `1.4em`
- body: `1em`

**Mobile (max-width: 768px):**
- h1: `1.8em`
- h2: `1.4em`
- h3: `1.2em`
- body: `0.95em`

**SVG Text Scaling:**
- Use `viewBox` for automatic scaling
- Font sizes in px remain constant
- Increase viewBox dimensions rather than reducing font sizes

## Component Patterns

### Metric Cards

**Standard Pattern:**
```html
<div class="metric-card">
    <div class="metric-value">[LARGE NUMBER]</div>
    <div class="metric-label">[DESCRIPTION]</div>
</div>
```

**With Custom Color:**
```html
<div class="metric-card" style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);">
    <div class="metric-value">✓ [NUMBER]</div>
    <div class="metric-label">[DESCRIPTION]</div>
</div>
```

### Code Blocks

**Standard:**
```html
<div class="code-block">
<span class="highlight">Key term:</span> Regular code text
    Indented content
</div>
```

**CSS:**
```css
.code-block {
    background: #2d3748;
    color: #e2e8f0;
    padding: 20px;
    border-radius: 10px;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
    overflow-x: auto;
    line-height: 1.6;
}
```

### Example Boxes

**Pattern:**
```html
<div class="example-box">
    <div class="example-title">[TITLE]</div>
    <p>[CONTENT]</p>
</div>
```

**CSS:**
```css
.example-box {
    background: #fff;
    border: 2px solid #667eea;
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
}
```

### Legends

**Pattern:**
```html
<div class="legend">
    <div class="legend-item">
        <div class="legend-box" style="background: #4299e1;"></div>
        <span>[DESCRIPTION]</span>
    </div>
    <!-- More items -->
</div>
```

**CSS:**
```css
.legend {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    padding: 20px;
    background: #edf2f7;
    border-radius: 10px;
}
```

## SVG Styling

### Default SVG Styles

**Container:**
```css
svg {
    width: 100%;
    height: auto;
}
```

**Text:**
```css
svg text {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
```

### Common Stroke/Fill Combinations

**Primary Box:**
- Fill: `#4299e1`
- Stroke: `#2b6cb0`
- Stroke-width: `3`

**Success Box:**
- Fill: `#48bb78`
- Stroke: `#2f855a`
- Stroke-width: `3`

**Warning Box:**
- Fill: `#f59e0b`
- Stroke: `#d97706`
- Stroke-width: `3`

**Neutral/Pending:**
- Fill: `#cbd5e0`
- Stroke: `#a0aec0`
- Stroke-width: `2-3`

### ViewBox Guidelines

**Common Aspect Ratios:**
- Wide: `viewBox="0 0 1200 400"` (3:1)
- Standard: `viewBox="0 0 1200 600"` (2:1)
- Balanced: `viewBox="0 0 1200 800"` (3:2)
- Square: `viewBox="0 0 600 600"` (1:1)
- Portrait: `viewBox="0 0 800 1000"` (4:5)

**Coordinate System:**
- Origin: Top-left (0, 0)
- X increases rightward
- Y increases downward
- Units are relative to viewBox

## Accessibility

### Color Blindness

**Safe Patterns:**
- Don't rely on color alone (use icons, labels, patterns)
- Use both fill and stroke for differentiation
- Ensure shapes differ (circle vs square vs diamond)
- Add text labels to all visual elements

**Color Combinations to Avoid:**
- Red/green alone (common color blindness)
- Blue/purple alone (hard to distinguish)
- Low contrast combinations

### Screen Readers

**HTML Structure:**
- Use semantic tags: `<section>`, `<article>`, `<header>`, `<footer>`
- Proper heading hierarchy: h1 → h2 → h3
- Descriptive text around SVG diagrams

**ARIA (if needed):**
```html
<svg aria-labelledby="chart-title" role="img">
    <title id="chart-title">Process Flow Diagram</title>
    <!-- SVG content -->
</svg>
```

### Keyboard Navigation

- Ensure all interactive elements are focusable
- Visible focus indicators
- Logical tab order

## Animation (Optional)

### Subtle Transitions

**Hover Effects:**
```css
.metric-card {
    transition: transform 0.2s, box-shadow 0.2s;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}
```

**Fade In:**
```css
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.section {
    animation: fadeIn 0.5s ease-in;
}
```

**Note:** Keep animations subtle and optional - avoid distracting from content.
