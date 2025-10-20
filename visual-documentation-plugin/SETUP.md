# Visual Documentation Plugin Setup

Quick setup guide for the Visual Documentation Plugin.

## Installation Methods

### Method 1: From Marketplace (Recommended)

```bash
# In Claude Code terminal
/plugin marketplace add mhattingpete/claude-skills-marketplace/visual-documentation-plugin
```

### Method 2: Manual Installation

1. Clone or download this repository:
```bash
git clone https://github.com/mhattingpete/claude-skills-marketplace.git
cd claude-skills-marketplace/visual-documentation-plugin
```

2. Copy to Claude plugins directory:
```bash
# macOS/Linux
cp -r visual-documentation-plugin ~/.claude/plugins/

# Windows
copy visual-documentation-plugin %USERPROFILE%\.claude\plugins\
```

3. Reload Claude Code

## Verification

To verify the plugin is installed correctly:

1. In Claude Code, type: `/skills list`
2. You should see `visual-html-creator` in the list
3. Test with: "Create a simple visual HTML with a flowchart showing: Start → Process → End"

## Quick Test

Try this example request:

```
Create a visual HTML dashboard showing these metrics:
- Total Users: 1,234
- Active Today: 456
- New Signups: 89
- Conversion Rate: 23%

Include a bar chart comparing these values.
```

Claude should generate a complete HTML file with metric cards and a bar chart.

## File Structure

After installation, the plugin structure is:

```
visual-documentation-plugin/
├── .claude-plugin/
│   └── plugin.json                          # Plugin manifest
├── skills/
│   └── visual-html-creator/
│       ├── SKILL.md                          # Main skill instructions
│       ├── assets/
│       │   └── templates/
│       │       ├── base_template.html        # Base HTML/CSS framework
│       │       ├── flowchart_components.html # Process flow patterns
│       │       ├── dashboard_components.html # Metric and chart patterns
│       │       └── timeline_components.html  # Timeline and roadmap patterns
│       └── references/
│           ├── design_patterns.md            # Design system reference
│           └── svg_library.md                # SVG component library
├── README.md                                 # Plugin documentation
└── SETUP.md                                  # This file
```

## Usage Patterns

### Basic Usage

Simply ask Claude to create visual documentation:

```
"Create a visual HTML for [your content]"
```

### Specific Visualization Types

**Flowchart:**
```
"Generate a visual flowchart showing our order processing workflow"
```

**Dashboard:**
```
"Make a dashboard showing our Q1 performance metrics"
```

**Timeline:**
```
"Build a timeline for our 2025 product roadmap"
```

**Technical Docs:**
```
"Create visual HTML documenting our authentication API"
```

### Advanced Usage

**Multiple Sections:**
```
"Create a comprehensive visual guide that includes:
1. Overview metrics at the top
2. A process flowchart showing our deployment pipeline
3. A timeline of upcoming milestones
4. Code examples for the API"
```

**Custom Styling:**
```
"Create a visual HTML with a flowchart, but use green for success states
and red for error states. Include a legend."
```

## Configuration

No configuration required! The skill works out of the box with:
- Default design system (purple/blue gradient theme)
- Semantic color palette
- Responsive layout
- Accessibility compliance

## Customization

To customize the design system:

1. Edit `assets/templates/base_template.html` for CSS changes
2. Edit `references/design_patterns.md` for color/typography updates
3. Edit `references/svg_library.md` for new SVG patterns
4. Reload Claude Code to apply changes

## Common Tasks

### Change Default Colors

Edit `references/design_patterns.md` and update the color definitions:

```markdown
**Primary gradient:**
- Background: `linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%)`
```

### Add New SVG Components

Add patterns to `references/svg_library.md` under the appropriate section.

### Modify HTML Template

Edit `assets/templates/base_template.html` to change the default structure or CSS.

## Troubleshooting

### Skill not activating

**Issue:** Claude doesn't use the skill when requested

**Solutions:**
1. Be explicit: "Create a visual HTML..." or "Generate visual documentation..."
2. Check skill is installed: `/skills list`
3. Reload Claude Code

### Generated HTML looks broken

**Issue:** HTML displays incorrectly in browser

**Solutions:**
1. Ensure file is saved with `.html` extension
2. Open in a modern browser (Chrome, Firefox, Safari, Edge)
3. Check browser console for errors

### SVG diagrams not showing

**Issue:** SVG elements don't render

**Solutions:**
1. Verify viewBox dimensions in SVG are appropriate
2. Check that `<svg>` tags have `width: 100%; height: auto;`
3. Ensure no syntax errors in SVG paths

### Colors look washed out

**Issue:** Colors appear faded or incorrect

**Solutions:**
1. Check monitor color profile
2. Verify hex color codes are correct (start with `#`)
3. Ensure opacity is set to `1` (or omitted) for solid colors

## Updating

### Update from Marketplace

```bash
/plugin marketplace update visual-documentation-skills
```

### Manual Update

1. Pull latest changes:
```bash
cd claude-skills-marketplace
git pull origin main
```

2. Reinstall plugin following installation steps above

## Uninstalling

### Remove from Claude Code

```bash
/plugin remove visual-documentation-skills
```

### Manual Removal

Delete the plugin directory:
```bash
# macOS/Linux
rm -rf ~/.claude/plugins/visual-documentation-plugin

# Windows
rmdir /s %USERPROFILE%\.claude\plugins\visual-documentation-plugin
```

## Getting Help

- **Issues:** [Open an issue](https://github.com/mhattingpete/claude-skills-marketplace/issues)
- **Documentation:** [Claude Code Skills Guide](https://docs.claude.com/en/docs/claude-code/skills)
- **Examples:** Check the `examples/` directory (if present) for sample outputs

## Next Steps

1. ✅ Install the plugin
2. ✅ Run verification test
3. ✅ Try example requests
4. 🚀 Create your first visual documentation!

Try these starter prompts:
- "Create a simple flowchart showing a login process"
- "Make a dashboard with 4 metric cards"
- "Generate a timeline for a 3-month project"
- "Build a visual guide for an API endpoint"

---

**Need more examples?** Check the main README.md for detailed use cases and output examples.
