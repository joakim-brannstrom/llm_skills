# Section Writing Guide

How to write each AGENTS.md section for maximum agent utility.

## Overview
- One or two sentences maximum
- State what the project does and its domain
- Example: "Internal dashboard for monitoring CI/CD pipeline health across 200+ repositories."

## Tech Stack
- List language, framework, and key libraries with versions
- Include database, cache, queue if applicable
- Use a bullet list — agents parse lists reliably

## Directory Layout
- Show only key directories and their purpose
- Use a tree snippet with comments, not a full listing
- Omit `node_modules/`, `dist/`, `.git/` — agents know these

## Commands
- Show the actual command prefix (`pnpm`, `npm`, `cargo`, `make`, etc.)
- Include only commands the agent will actually run
- Add a brief comment after each explaining what it does
- Verify commands exist in the project's config before writing

## Code Conventions
- Be specific: "camelCase for variables, PascalCase for components"
- Reference actual config files: "ESLint config in `.eslintrc.cjs`"
- State what to avoid: "No class components", "No inline styles"
- Include import ordering if the project enforces it

## Architecture & Patterns
- Explain the "why" behind architectural decisions
- List patterns: "Repository pattern for data access", "CQRS for commands"
- Note state management: "Redux Toolkit with RTK Query"
- Document error handling strategy

## Testing
- Specify test file naming: `*.test.ts` or `*_test.rs`
- State co-location policy: "Tests beside source" vs "tests/ directory"
- Note testing libraries and their query preferences
- Include coverage targets if any

## Git Workflow
- Branch naming convention: `feature/slug`, `fix/slug`
- Commit message format: conventional commits, scope rules
- PR requirements: checklist items, review rules

## Environment & Services
- List env var names (not values): `DATABASE_URL`, `API_KEY`
- Link to external API documentation
- Note feature flag system and config location

## Agent Rules
- Write as imperative commands: "Always...", "Never...", "Prefer..."
- Make them specific to this project — not generic advice
- Include file-level constraints: "Do not modify `legacy/`"
- Include behavioral rules: "Run tests before suggesting changes"
- This section is the most important — agents follow it literally
