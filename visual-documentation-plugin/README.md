# Visual Documentation Plugin

Create stunning, professional visual HTML documentation with modern UI design, SVG diagrams, flowcharts, dashboards, and timelines.

## Skills Included

### `visual-html-creator`

Generate standalone HTML documentation files with embedded CSS and SVG graphics optimized for technical documentation and data visualization.

**Activates when:** User explicitly requests visual HTML documentation, process flow diagrams, metric dashboards, API workflow guides, deployment process visuals, or project roadmaps.

**Example usage:**
- "Create a visual HTML for our deployment process"
- "Make a dashboard showing project metrics"
- "Generate a visual guide for our API workflow"
- "Build a timeline for our product roadmap"

**Capabilities:**
- **Process Flow Diagrams** - Flowcharts with decision trees, arrows, and color-coded stages
- **Metric Dashboards** - KPI cards, bar charts, pie charts, and statistics displays
- **Technical Documentation** - Code blocks, API workflows, and system architecture
- **Project Timelines** - Gantt charts, roadmaps, and milestone visualizations

**Design Features:**
- Modern gradient backgrounds and color schemes
- Semantic color system (success/warning/error/info)
- Responsive mobile-first design
- WCAG AA accessibility compliance
- Self-contained HTML (no external dependencies)

## Installation

### From Marketplace

```bash
# In Claude Code
/plugin marketplace add mhattingpete/claude-skills-marketplace/visual-documentation-plugin
```

### Manual Installation

1. Copy the `visual-documentation-plugin` directory to your Claude plugins folder
2. Reload Claude Code

## Quick Start

Once installed, simply ask Claude to create visual documentation:

```
"Create a visual HTML showing our deployment pipeline with these stages:
- Development (commit to main)
- Build (automated tests)
- Staging deployment
- Production deployment"
```

Claude will generate a complete, standalone HTML file with:
- Professional gradient design
- SVG flowchart diagram
- Color-coded process stages
- Responsive layout
- All styling embedded

## Example Outputs

### Process Flow Example
**Request:** "Create a visual guide for our deployment process"

**Generates:**
- Decision tree showing deployment paths (prod/staging/dev)
- Status indicators for each stage
- Color-coded boxes for different deployment types
- Arrow flow showing sequential and parallel steps
- Legend explaining status colors

### Dashboard Example
**Request:** "Make a dashboard showing project metrics"

**Generates:**
- Metric cards: total tasks, completed, in progress, blocked
- Bar chart showing task distribution by category
- Timeline visualization of milestone completion
- Color-coded status indicators
- Summary statistics in footer

### API Workflow Example
**Request:** "Create visual HTML showing our API workflow"

**Generates:**
- Sequential flow: Client → API Gateway → Services → Database
- Request/response boxes with sample JSON
- Authentication flow decision tree
- Error handling paths
- Code examples with syntax highlighting

### Timeline Example
**Request:** "Build a timeline for our product roadmap"

**Generates:**
- Horizontal timeline with quarters marked
- Milestone markers with descriptions
- Phase groupings (Planning, Development, Testing, Launch)
- Dependency arrows between related items
- Color-coded priorities

## Bundled Resources

### Templates (`assets/templates/`)
- `base_template.html` - Complete CSS framework and document structure
- `flowchart_components.html` - Process flow and decision tree patterns
- `dashboard_components.html` - Metric cards, charts, and visualizations
- `timeline_components.html` - Timeline and roadmap layouts

### References (`references/`)
- `design_patterns.md` - Complete design system with colors, typography, spacing
- `svg_library.md` - Comprehensive SVG component library with shapes and patterns

## Design System

### Color Palette

**Semantic Colors:**
- Success/Confirmed: `#48bb78` (green)
- Warning/Uncertain: `#f59e0b` (amber)
- Info/Primary: `#4299e1` (blue)
- Error/Critical: `#f56565` (red)
- Process/Action: `#ed8936` (orange)
- Special/Highlight: `#9f7aea` (purple)

**Primary Gradient:**
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Typography
- Font: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
- Headings: 2.5em (h1), 1.8em (h2), 1.4em (h3)
- Code: 'Courier New', monospace

### Responsive Design
- Max container width: 1400px
- Desktop padding: 40px
- Mobile padding: 20px
- Breakpoint: 768px

## Technical Details

**Output Format:**
- Standalone HTML5 files
- All CSS embedded in `<style>` tags
- All SVG inline (no external images)
- Responsive viewBox-based SVG scaling
- Cross-browser compatible (modern browsers)

**File Size:**
- Typical output: 50-150 KB
- No external dependencies
- Fast loading and rendering

**Accessibility:**
- WCAG AA compliant color contrast (4.5:1 minimum)
- Semantic HTML structure
- Text labels for all visual elements
- Keyboard navigation support

## Customization

The skill automatically adapts to your content while maintaining:
- Consistent design language
- Professional visual hierarchy
- Responsive layout
- Accessibility standards

Customize by providing:
- Specific data and metrics
- Process steps and relationships
- Color preferences (will map to semantic system)
- Content sections and organization

## Best Practices

1. **Be specific about content** - Provide actual data, process steps, or structure
2. **Request iterative refinement** - Ask for changes to colors, layout, or styling
3. **Combine visualization types** - Mix flowcharts with metrics, timelines with dashboards
4. **Save outputs** - Specify file path to save the generated HTML
5. **Test responsiveness** - View on different screen sizes

## Troubleshooting

**Issue:** SVG not displaying correctly
- Check that the HTML is opened in a modern browser
- Ensure file is saved with `.html` extension

**Issue:** Layout broken on mobile
- The design is responsive by default
- Verify viewport meta tag is present

**Issue:** Colors look different than expected
- All colors use consistent hex values
- Check browser color profile settings

## Contributing

Want to improve this plugin?

1. Fork the repository
2. Create your feature branch
3. Add or modify templates in `assets/templates/`
4. Update references in `references/`
5. Test with various content types
6. Submit a pull request

## License

Apache 2.0 - See LICENSE file for details.

## Support

- [Open an issue](https://github.com/mhattingpete/claude-skills-marketplace/issues)
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/skills)

---

**Version:** 1.0.0
**Author:** mhattingpete
**Plugin Type:** Visual Documentation & Diagramming
