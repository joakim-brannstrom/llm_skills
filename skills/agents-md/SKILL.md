---
name: agents-md
description: >-
  Create or update an AGENTS.md file - the project-level instruction file that
  AI coding agents read before working on a codebase. Use when the user asks to
  create, update, write, improve, or review an AGENTS.md file. Triggers on:
  agents.md, AGENTS.md, create agents file, update agents file, project
  instructions for AI, agent context file, project brief for agents.
version: 1.0.0
---

# AGENTS.md Skill

Create or update an `AGENTS.md` file that gives AI agents the context and rules they need to work productively on a project.

## When to Use

- User asks to create or update an `AGENTS.md` file
- User wants AI-readable project instructions
- A project lacks agent context and needs one

## Core Principle

AGENTS.md is the **system prompt for a codebase**. It tells any AI agent how to
work on the project — conventions, architecture, commands, and constraints.
Write it for an agent reader: direct, unambiguous, actionable.

## Rules

- **Place at repository root**, named exactly `AGENTS.md`
- **Under 500 lines** — link to dedicated docs for deeper detail
- **No secrets** — never include API keys, passwords, or tokens
- **No duplication** — don't repeat what config files already state
- **Focus on what the agent cannot infer** from code alone
- **Use imperative, specific language** — agents read literally
- **No contradictions** — a rule stated once means it holds everywhere

## Workflow

1. **Assess the project** — scan `package.json`, `dub.sdl`, `Cargo.toml`,
   `pyproject.toml`, or equivalent to determine language, framework, and tooling.
   Check existing configs for linter, formatter, and test runner settings.

2. **Identify what to capture** — determine which sections are needed based on
   project complexity. Minimal projects need Overview, Commands, and Conventions.
   Larger projects need all sections.

3. **Write the file** — follow the section order below. Use the template in
   `references/template.md` as a starting point.

4. **Validate** — verify no secrets, no contradictions, and that commands
   reference actual scripts/targets in the project.

5. **Report** — confirm the file was created/updated and note any sections
   that were skipped or need user input.

## Section Order (top-down)

1. **Overview** — one or two sentences on project purpose and domain
2. **Tech Stack** — languages, frameworks, key libraries
3. **Directory Layout** — key folders and their responsibilities
4. **Commands** — install, build, test, lint, run
5. **Code Conventions** — naming, formatting, import order, language specifics
6. **Architecture & Patterns** — state management, error handling, key patterns
7. **Testing** — test types, locations, how to run, conventions
8. **Git Workflow** — branch naming, commit style, PR process
9. **Environment & Services** — env var names, external APIs, feature flags
10. **Agent Rules** — explicit do/don't directives for AI agents

## Agent Rules Section (critical)

The `## Agent Rules` section is the most important part. It contains explicit
directives the AI must follow. Write them as imperative statements:

- "Always use TypeScript types — never `any`"
- "Do not modify files in `legacy/`"
- "Prefer `async/await` over raw promises"
- "Run `pnpm test` before suggesting changes"

## References

- Full template with examples: `references/template.md`
- Section writing guide: `references/sections.md`
