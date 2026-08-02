# AGENTS.md Template

Copy and adapt this template. Remove sections that don't apply.

```markdown
# Project Name

## Overview
Brief description of the project's purpose and domain.

## Tech Stack
- **Language:** [language, version]
- **Framework:** [framework, version]
- **Database:** [database]
- **Testing:** [test framework]
- **Build:** [build tool]

## Directory Layout
```
src/
  components/   – shared UI components
  pages/        – route handlers
  lib/          – utilities and shared logic
  ...
```

## Commands
```bash
install          # install dependencies
dev              # start development server
build            # production build
test             # run unit tests
test:e2e         # run end-to-end tests
lint             # lint code
```

## Code Conventions
- **Formatting:** [tool and config location]
- **Naming:** [conventions for variables, functions, components, files]
- **Imports:** [grouping and ordering rules]
- **Language specifics:** [strict mode, features to use/avoid]

## Architecture & Patterns
- [State management approach]
- [API/data layer pattern]
- [Error handling strategy]
- [Key design patterns in use]

## Testing
- **Unit tests:** [location, naming convention]
- **Integration tests:** [location, how to run]
- **E2E tests:** [location, how to run]
- **Conventions:** [what to test, coverage expectations]

## Git Workflow
- **Branch naming:** [convention]
- **Commit style:** [conventional commits, format]
- **PR process:** [requirements, review expectations]

## Environment & Services
- **Auth:** [provider, config location]
- **External APIs:** [base URLs, doc links]
- **Feature flags:** [management approach]
- **Env vars:** [list of required variable names]

## Agent Rules
- [Rule 1: specific, imperative directive]
- [Rule 2: specific, imperative directive]
- [Rule 3: specific, imperative directive]
```

## Adaptation Notes

- **Minimal projects**: Overview + Commands + Agent Rules may be enough
- **Monorepos**: Add a workspace structure section
- **Library packages**: Emphasize API surface and export conventions
- **Services**: Add deployment and health check details
