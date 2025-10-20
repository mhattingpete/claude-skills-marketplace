# SVG Component Library

Comprehensive reference for SVG shapes, patterns, and techniques for creating stunning diagrams.

## SVG Fundamentals

### Basic Structure

```xml
<svg viewBox="0 0 1200 800" style="width: 100%; height: auto;">
    <defs>
        <!-- Reusable definitions (markers, gradients, patterns) -->
    </defs>

    <g id="group-name">
        <!-- Grouped elements -->
    </g>

    <!-- Direct elements -->
</svg>
```

### ViewBox Explained

**Format:** `viewBox="min-x min-y width height"`
**Example:** `viewBox="0 0 1200 800"`

- **min-x, min-y:** Usually `0 0` (top-left origin)
- **width, height:** Virtual coordinate system dimensions
- SVG scales to fit container while maintaining aspect ratio
- Larger viewBox = more space for content

**Common Sizes:**
```xml
<!-- Wide flowchart -->
<svg viewBox="0 0 1200 400">

<!-- Standard diagram -->
<svg viewBox="0 0 1200 600">

<!-- Detailed flowchart -->
<svg viewBox="0 0 1200 800">

<!-- Square chart -->
<svg viewBox="0 0 600 600">

<!-- Vertical timeline -->
<svg viewBox="0 0 800 1000">
```

### Coordinate System

- **X-axis:** Left (0) to right (positive)
- **Y-axis:** Top (0) to bottom (positive)
- **Center of 1200×800 viewBox:** `(600, 400)`
- **Units:** Relative to viewBox (not pixels)

## Basic Shapes

### Rectangle

**Standard Rectangle:**
```xml
<rect x="100" y="100" width="200" height="100"
      fill="#4299e1" stroke="#2b6cb0" stroke-width="3"/>
```

**Rounded Rectangle:**
```xml
<rect x="100" y="100" width="200" height="100" rx="10"
      fill="#4299e1" stroke="#2b6cb0" stroke-width="3"/>
```
- `rx`: Horizontal corner radius
- `ry`: Vertical corner radius (defaults to `rx` if omitted)

**Process Box with Text:**
```xml
<rect x="50" y="50" width="200" height="100" rx="10"
      fill="#4299e1" stroke="#2b6cb0" stroke-width="3"/>
<text x="150" y="95" text-anchor="middle" fill="white"
      font-size="16" font-weight="bold">
    Process Name
</text>
<text x="150" y="115" text-anchor="middle" fill="white" font-size="12">
    Subtitle
</text>
```

**Position Calculation:**
- Text X: `rect.x + (rect.width / 2)` for center
- Text Y: `rect.y + (rect.height / 2)` for vertical center (approximately)
- Baseline adjustment: Add `5-10px` to Y for visual centering

### Circle

**Basic Circle:**
```xml
<circle cx="300" cy="200" r="50"
        fill="#48bb78" stroke="#2f855a" stroke-width="3"/>
```
- `cx, cy`: Center coordinates
- `r`: Radius

**Circle with Text (Start/End Node):**
```xml
<circle cx="300" cy="200" r="50"
        fill="#48bb78" stroke="#2f855a" stroke-width="3"/>
<text x="300" y="205" text-anchor="middle" fill="white"
      font-size="16" font-weight="bold">
    START
</text>
```

**Small Marker Circle:**
```xml
<circle cx="300" cy="200" r="15"
        fill="#4299e1" stroke="#2b6cb0" stroke-width="3"/>
```

### Ellipse

```xml
<ellipse cx="400" cy="200" rx="120" ry="60"
         fill="#9f7aea" stroke="#6b46c1" stroke-width="3"/>
```
- `rx`: Horizontal radius
- `ry`: Vertical radius

## Path Shapes

### Diamond (Decision Node)

**Diamond Formula:**
```
Top:    (center-x, top-y)
Right:  (right-x, center-y)
Bottom: (center-x, bottom-y)
Left:   (left-x, center-y)
```

**Example (100px wide, 100px tall, centered at 600, 150):**
```xml
<path d="M 600 100 L 650 150 L 600 200 L 550 150 Z"
      fill="#fbbf24" stroke="#d97706" stroke-width="3"/>
<text x="600" y="155" text-anchor="middle" font-size="14" font-weight="bold">
    Decision?
</text>
```

**Larger Diamond (200×100):**
```xml
<path d="M 600 130 L 700 130 L 750 180 L 700 230 L 500 230 L 450 180 Z"
      fill="#fbbf24" stroke="#d97706" stroke-width="3"/>
```

### Hexagon (Preparation)

**Horizontal Hexagon:**
```xml
<path d="M 900 75 L 1050 75 L 1100 100 L 1050 125 L 900 125 L 850 100 Z"
      fill="#9f7aea" stroke="#6b46c1" stroke-width="3"/>
```

**Pattern:**
```
M [left-mid-x] [top-y]          (start left of top edge)
L [right-mid-x] [top-y]         (top edge)
L [right-x] [center-y]          (top-right slope)
L [right-mid-x] [bottom-y]      (bottom edge)
L [left-mid-x] [bottom-y]       (bottom edge)
L [left-x] [center-y]           (top-left slope)
Z                                (close path)
```

### Parallelogram

```xml
<path d="M 100 100 L 280 100 L 250 150 L 70 150 Z"
      fill="#ed8936" stroke="#c05621" stroke-width="3"/>
```

### Custom Polygons

**Triangle:**
```xml
<path d="M 500 100 L 600 200 L 400 200 Z"
      fill="#f56565" stroke="#c53030" stroke-width="3"/>
```

**Pentagon:**
```xml
<path d="M 500 100 L 580 150 L 550 230 L 450 230 L 420 150 Z"
      fill="#4299e1" stroke="#2b6cb0" stroke-width="3"/>
```

## Lines & Arrows

### Straight Lines

**Horizontal:**
```xml
<line x1="100" y1="200" x2="300" y2="200"
      stroke="#2d3748" stroke-width="3"/>
```

**Vertical:**
```xml
<line x1="200" y1="100" x2="200" y2="300"
      stroke="#2d3748" stroke-width="3"/>
```

**Diagonal:**
```xml
<line x1="100" y1="100" x2="300" y2="300"
      stroke="#2d3748" stroke-width="3"/>
```

**Dashed Line:**
```xml
<line x1="100" y1="200" x2="300" y2="200"
      stroke="#cbd5e0" stroke-width="2" stroke-dasharray="5,5"/>
```
- `stroke-dasharray="dash,gap"`: Pattern of dashes and gaps
- Common patterns: `"5,5"` (small), `"10,5"` (medium), `"20,10"` (large)

### Path-based Lines

**Straight line with path:**
```xml
<path d="M 100 200 L 300 200"
      stroke="#2d3748" stroke-width="3" fill="none"/>
```
- `fill="none"`: Prevents filling (required for non-closed paths used as lines)

**L-shaped connector:**
```xml
<path d="M 250 100 L 400 100 L 400 200"
      stroke="#2d3748" stroke-width="3" fill="none"/>
```

**Multi-segment:**
```xml
<path d="M 100 100 L 200 100 L 200 200 L 300 200"
      stroke="#2d3748" stroke-width="3" fill="none"/>
```

### Arrow Markers

**Standard Arrowhead Definition:**
```xml
<defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10"
            refX="9" refY="3" orient="auto">
        <polygon points="0 0, 10 3, 0 6" fill="#2d3748"/>
    </marker>
</defs>
```
- `markerWidth/Height`: Size of marker viewport
- `refX/refY`: Anchor point (where arrow attaches to line)
- `orient="auto"`: Rotates to match line angle

**Colored Arrows:**
```xml
<defs>
    <marker id="arrowhead-success" markerWidth="10" markerHeight="10"
            refX="9" refY="3" orient="auto">
        <polygon points="0 0, 10 3, 0 6" fill="#48bb78"/>
    </marker>

    <marker id="arrowhead-error" markerWidth="10" markerHeight="10"
            refX="9" refY="3" orient="auto">
        <polygon points="0 0, 10 3, 0 6" fill="#f56565"/>
    </marker>
</defs>
```

**Using Arrows:**
```xml
<!-- Arrow at end -->
<path d="M 100 200 L 300 200" stroke="#2d3748" stroke-width="3"
      fill="none" marker-end="url(#arrowhead)"/>

<!-- Arrow at start -->
<path d="M 100 200 L 300 200" stroke="#2d3748" stroke-width="3"
      fill="none" marker-start="url(#arrowhead)"/>

<!-- Arrows at both ends -->
<path d="M 100 200 L 300 200" stroke="#2d3748" stroke-width="3"
      fill="none" marker-start="url(#arrowhead)" marker-end="url(#arrowhead)"/>
```

### Curved Lines (Bezier Curves)

**Quadratic Bezier (Q):**
```xml
<path d="M 100 200 Q 200 100 300 200"
      stroke="#2d3748" stroke-width="3" fill="none"/>
```
- Format: `Q control-x control-y end-x end-y`
- One control point

**Cubic Bezier (C):**
```xml
<path d="M 100 200 C 150 100, 250 100, 300 200"
      stroke="#2d3748" stroke-width="3" fill="none"/>
```
- Format: `C control1-x control1-y control2-x control2-y end-x end-y`
- Two control points (more control)

**Smooth Curve Through Points:**
```xml
<path d="M 100 200 Q 150 150 200 200 T 300 200"
      stroke="#4299e1" stroke-width="3" fill="none"/>
```
- `T`: Smooth continuation of quadratic curve

## Text Elements

### Basic Text

```xml
<text x="100" y="100" font-size="16" fill="#2d3748">
    Simple Text
</text>
```

### Text Anchoring

**Horizontal Alignment:**
```xml
<!-- Left-aligned (default) -->
<text x="100" y="100" text-anchor="start">Left</text>

<!-- Center-aligned -->
<text x="100" y="100" text-anchor="middle">Center</text>

<!-- Right-aligned -->
<text x="100" y="100" text-anchor="end">Right</text>
```

**Vertical Alignment:**
```xml
<!-- Baseline (default) -->
<text x="100" y="100" dominant-baseline="auto">Baseline</text>

<!-- Middle -->
<text x="100" y="100" dominant-baseline="middle">Middle</text>

<!-- Hanging (top) -->
<text x="100" y="100" dominant-baseline="hanging">Top</text>
```

**Note:** For reliable vertical centering, calculate Y position manually rather than relying on dominant-baseline (browser support varies).

### Text Styling

```xml
<text x="100" y="100"
      font-size="18"
      font-weight="bold"
      font-style="italic"
      fill="#2d3748"
      opacity="0.8">
    Styled Text
</text>
```

**Font Families in SVG:**
```xml
<text x="100" y="100" font-family="'Segoe UI', sans-serif">
    Custom Font
</text>
```

### Multi-line Text

**Using Multiple <text> Elements:**
```xml
<text x="150" y="90" text-anchor="middle" fill="white" font-size="16" font-weight="bold">
    Line 1
</text>
<text x="150" y="110" text-anchor="middle" fill="white" font-size="12">
    Line 2
</text>
<text x="150" y="125" text-anchor="middle" fill="white" font-size="11">
    Line 3
</text>
```

**Line Spacing:** Typically 15-25px between lines depending on font size

### Text on Path

```xml
<defs>
    <path id="curve" d="M 100 200 Q 300 100 500 200" fill="none"/>
</defs>

<text font-size="16" fill="#2d3748">
    <textPath href="#curve">
        Text following the curve
    </textPath>
</text>
```

## Gradients

### Linear Gradient

```xml
<defs>
    <linearGradient id="blueGradient" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:#4299e1;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#2b6cb0;stop-opacity:1" />
    </linearGradient>
</defs>

<rect x="100" y="100" width="200" height="100" fill="url(#blueGradient)"/>
```

**Gradient Directions:**
- Horizontal: `x1="0%" y1="0%" x2="100%" y2="0%"`
- Vertical: `x1="0%" y1="0%" x2="0%" y2="100%"`
- Diagonal: `x1="0%" y1="0%" x2="100%" y2="100%"`

### Radial Gradient

```xml
<defs>
    <radialGradient id="radialGlow">
        <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#764ba2;stop-opacity:0.5" />
    </radialGradient>
</defs>

<circle cx="300" cy="200" r="80" fill="url(#radialGlow)"/>
```

### Multi-stop Gradients

```xml
<linearGradient id="multiColor" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" style="stop-color:#48bb78" />
    <stop offset="50%" style="stop-color:#f59e0b" />
    <stop offset="100%" style="stop-color:#f56565" />
</linearGradient>
```

## Grouping & Reuse

### Groups (<g>)

```xml
<g id="icon-group" transform="translate(100, 100)">
    <circle r="30" fill="#4299e1"/>
    <text y="5" text-anchor="middle" fill="white" font-weight="bold">✓</text>
</g>
```

**Benefits:**
- Apply transformations to multiple elements
- Organize related elements
- Apply styles to all children

### Use Element

**Define once:**
```xml
<defs>
    <g id="status-icon">
        <circle r="15" fill="#48bb78" stroke="#2f855a" stroke-width="2"/>
        <text text-anchor="middle" fill="white" font-size="12" font-weight="bold">✓</text>
    </g>
</defs>
```

**Reuse multiple times:**
```xml
<use href="#status-icon" x="100" y="100"/>
<use href="#status-icon" x="300" y="100"/>
<use href="#status-icon" x="500" y="100"/>
```

### Symbol Element

```xml
<defs>
    <symbol id="check-icon" viewBox="0 0 30 30">
        <circle cx="15" cy="15" r="15" fill="#48bb78"/>
        <path d="M 8 15 L 13 20 L 22 10" stroke="white" stroke-width="3"
              fill="none" stroke-linecap="round"/>
    </symbol>
</defs>

<use href="#check-icon" x="100" y="100" width="30" height="30"/>
<use href="#check-icon" x="200" y="100" width="50" height="50"/>
```

**Symbol vs Group:**
- Symbol has its own viewBox (scalable)
- Symbol not rendered unless used
- Better for reusable icons

## Transformations

### Translate (Move)

```xml
<rect x="0" y="0" width="100" height="50" fill="#4299e1"
      transform="translate(200, 100)"/>
```
- Moves shape to new position
- Original x, y still apply (total position = original + translate)

### Rotate

```xml
<rect x="100" y="100" width="100" height="50" fill="#4299e1"
      transform="rotate(45 150 125)"/>
```
- Format: `rotate(angle center-x center-y)`
- Angle in degrees
- Rotates around specified center point

### Scale

```xml
<circle cx="200" cy="200" r="30" fill="#48bb78"
        transform="scale(1.5)"/>
```
- `scale(factor)`: Uniform scaling
- `scale(x-factor, y-factor)`: Non-uniform scaling

### Combined Transformations

```xml
<rect x="0" y="0" width="100" height="50" fill="#4299e1"
      transform="translate(200, 100) rotate(15) scale(1.2)"/>
```
- Applied right to left: scale → rotate → translate

## Advanced Patterns

### Rounded Progress Bar

```xml
<!-- Background -->
<rect x="150" y="80" width="800" height="40" rx="20" fill="#e2e8f0"/>

<!-- Progress (60%) -->
<rect x="150" y="80" width="480" height="40" rx="20" fill="#48bb78"/>
```

### Donut Chart (Simplified)

```xml
<circle cx="300" cy="300" r="150" fill="none"
        stroke="#4299e1" stroke-width="80"/>
```

**Multi-segment Donut:**
```xml
<!-- Segment 1 (50% of circle = 471 units out of 942 total circumference) -->
<circle cx="300" cy="300" r="150" fill="none"
        stroke="#4299e1" stroke-width="80"
        stroke-dasharray="471 471"
        transform="rotate(-90 300 300)"/>

<!-- Segment 2 (30%) -->
<circle cx="300" cy="300" r="150" fill="none"
        stroke="#48bb78" stroke-width="80"
        stroke-dasharray="283 659"
        stroke-dashoffset="-471"
        transform="rotate(-90 300 300)"/>
```

**Circumference Formula:** `2 × π × radius = 2 × 3.14159 × 150 ≈ 942`

### Drop Shadow Filter

```xml
<defs>
    <filter id="drop-shadow">
        <feGaussianBlur in="SourceAlpha" stdDeviation="3"/>
        <feOffset dx="2" dy="2" result="offsetblur"/>
        <feMerge>
            <feMergeNode/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>
</defs>

<rect x="100" y="100" width="200" height="100" rx="10"
      fill="#4299e1" filter="url(#drop-shadow)"/>
```

### Clipping Path

```xml
<defs>
    <clipPath id="rounded-clip">
        <rect x="100" y="100" width="200" height="150" rx="15"/>
    </clipPath>
</defs>

<image x="100" y="100" width="200" height="150"
       href="image.jpg" clip-path="url(#rounded-clip)"/>
```

## Chart Components

### Bar Chart Bar

```xml
<rect x="200" y="150" width="150" height="200" rx="5"
      fill="#4299e1" stroke="#2b6cb0" stroke-width="2"/>
<text x="275" y="260" text-anchor="middle" fill="white"
      font-size="24" font-weight="bold">
    456
</text>
```

### Axis Lines

```xml
<!-- X-axis -->
<line x1="100" y1="350" x2="1100" y2="350"
      stroke="#2d3748" stroke-width="2"/>

<!-- Y-axis -->
<line x1="100" y1="350" x2="100" y2="80"
      stroke="#2d3748" stroke-width="2"/>

<!-- Grid lines -->
<line x1="100" y1="280" x2="1100" y2="280"
      stroke="#e2e8f0" stroke-width="1" opacity="0.5"/>
```

### Data Point Marker

```xml
<circle cx="300" cy="200" r="6" fill="#4299e1"
        stroke="white" stroke-width="2"/>
```

## Best Practices

### Coordinate Calculation

**Center Text in Rectangle:**
```javascript
textX = rectX + (rectWidth / 2)
textY = rectY + (rectHeight / 2) + (fontSize * 0.35)
```

**Position Diamond Points:**
```javascript
centerX = 600, centerY = 180
halfWidth = 100, halfHeight = 50

top:    (centerX, centerY - halfHeight)
right:  (centerX + halfWidth, centerY)
bottom: (centerX, centerY + halfHeight)
left:   (centerX - halfWidth, centerY)
```

### Performance Tips

- Limit total SVG elements per diagram to ~500-1000
- Use `<use>` for repeated elements
- Avoid overly complex paths
- Minimize filter usage (shadows, blurs)
- Group related elements

### Readability Guidelines

- Minimum stroke-width: 2px for visibility
- Minimum font-size: 11px for labels, 14px for emphasis
- Minimum touch target: 30×30px for interactive elements
- White space: 20-30px between major elements
- Contrast: Stroke should be darker than fill

### Debugging SVG

**Visible Boundaries:**
```xml
<!-- Temporary: shows viewBox boundary -->
<rect x="0" y="0" width="1200" height="800"
      fill="none" stroke="red" stroke-width="1"/>
```

**Grid Overlay:**
```xml
<!-- Shows 100px grid -->
<line x1="0" y1="100" x2="1200" y2="100" stroke="pink" stroke-width="1"/>
<line x1="0" y1="200" x2="1200" y2="200" stroke="pink" stroke-width="1"/>
<!-- ... repeat for debugging ... -->
```

## Icon Library

### Checkmark

```xml
<path d="M 8 15 L 13 20 L 22 10"
      stroke="#48bb78" stroke-width="3" fill="none"
      stroke-linecap="round" stroke-linejoin="round"/>
```

### X (Close)

```xml
<path d="M 10 10 L 20 20 M 20 10 L 10 20"
      stroke="#f56565" stroke-width="3"
      stroke-linecap="round"/>
```

### Warning Triangle

```xml
<path d="M 15 5 L 25 23 L 5 23 Z"
      fill="#f59e0b" stroke="#d97706" stroke-width="2"/>
<text x="15" y="20" text-anchor="middle" fill="white"
      font-weight="bold" font-size="14">!</text>
```

### Info Circle

```xml
<circle cx="15" cy="15" r="12" fill="#4299e1" stroke="#2b6cb0" stroke-width="2"/>
<text x="15" y="20" text-anchor="middle" fill="white"
      font-weight="bold" font-size="16">i</text>
```
