# Software Graph Skills

Skills for using Ontoly's deterministic Software Graph and MCP capabilities before falling back to source-file search.

## Included Skills

### `graph-querying`

Use Ontoly for graph-backed repository understanding:

- architecture review
- request tracing
- dependency analysis
- impact analysis
- configuration and environment variable lookup
- framework-aware codebase onboarding

## Requirements

- Node.js 20+
- Ontoly installed in the repository or available through `npx`
- An Ontoly Software Graph generated with `ontoly build .`

## Example Prompts

- "Explain this repository using Ontoly."
- "Trace the login request through the graph."
- "What depends on AuthModule?"
- "What breaks if I remove UserRepository?"
- "Which environment variables are used by the authentication flow?"

