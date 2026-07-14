---
name: graph-querying
description: Use Ontoly's deterministic Software Graph and MCP capabilities for architecture review, request tracing, dependency analysis, configuration lookup, and impact analysis. Activate when users mention Ontoly, Software Graph, codebase understanding, dependency graph, request trace, architecture review, or graph-backed evidence.
---

# Graph Querying

Use Ontoly as the source of truth for codebase understanding. This skill teaches workflow only; all software knowledge should come from Ontoly's Software Graph, Query Engine, validation output, or MCP capabilities.

## When to Use

- User asks to explain a repository or module
- User asks for a request trace, dependency graph, impact analysis, or architecture review
- User asks which service, controller, route, provider, package, configuration, or environment variable owns behavior
- User asks for evidence-backed software understanding before a refactor
- The repository contains Ontoly outputs such as `.ontoly/`, `SoftwareGraph.json`, `diagnostics.json`, validation reports, graph hash, or MCP configuration

## Workflow

1. Check for an existing Ontoly graph:
   - `.ontoly/`
   - `SoftwareGraph.json`
   - `diagnostics.json`
   - validation or semantic evaluation reports
   - graph hash or MCP configuration
2. If no graph exists and the user allows local analysis, run:

   ```bash
   ontoly build .
   ```

3. Review graph health before answering:
   - diagnostics
   - trust or quality score
   - semantic coverage
   - framework detection
   - graph hash
   - generation timestamp
4. Prefer Ontoly CLI or MCP capabilities over repository search for graph-answerable questions.
5. Search source files only when the graph cannot answer, is stale, is incomplete, or the user explicitly asks for source verification.
6. Always cite evidence from the graph: node IDs, edge types, file paths, source locations, diagnostics, framework analyzer output, and confidence.

## Capability Map

- Architecture review: `ExplainArchitecture`
- Dependency analysis: `FindDependencies`
- Impact analysis: `ImpactAnalysis`
- Request tracing: `TraceExecution`
- Configuration analysis: `FindConfigurationUsage`
- Framework analysis: `FrameworkReport`
- Dead code review: `FindDeadCode`

## Response Format

Answer directly, then show evidence:

```text
AuthController handles authentication.

Evidence:
- node: class:src/auth/auth.controller.ts:AuthController
- route edges: HANDLES POST /login and POST /logout
- dependency edges: USES AuthService and JwtService

Confidence: high, because the graph has controller, route, and dependency edges with source locations.
```

## Fallback Rules

- If the graph is missing, build it first when allowed.
- If graph validation fails, report the graph issue and verify only the affected area with source search.
- If multiple nodes match, show candidates with package/module context.
- If nothing matches, return `NOT_FOUND` with the closest graph evidence instead of inventing an answer.

