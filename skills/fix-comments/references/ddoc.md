# Ddoc Handling for D Code

Ddoc is D's embedded documentation system. Ddoc comments are extracted at compile
time and formatted into HTML documentation pages. They are **not** regular
comments — they feed the documentation generator.

## Ddoc Comment Forms

Three forms are recognized as ddoc:

| Form | Example | Notes |
|------|---------|-------|
| `/** ... */` | `/** Multi-line ddoc. */` | Two asterisks after opening `/` |
| `/+ ... +/` | `/+ Plus-delimited ddoc. +/` | Two plus signs after opening `/` |
| `///` | `/// One-line ddoc.` | Three slashes |

Regular comments (`//`, `/* */`, `/+ +/`) are **not** ddoc.

## Association Rules

- Ddoc comments are associated with the **next declaration**.
- Multiple ddoc comments for the same declaration are **concatenated**.
- Ddoc comments **not** associated with a declaration are **ignored** by the compiler.
- Comments preceding the `ModuleDeclaration` apply to the **entire module**.
- Comments on the same line as a declaration apply to **that declaration**.

## Special Sections (ALWAYS KEEP)

Ddoc special sections start with a keyword followed by a colon. These are
**functional** — they affect compilation and documentation:

| Section | Purpose | Keep? |
|---------|---------|-------|
| `Example:` | Code compiled and run as a test | **ALWAYS** |
| `Examples:` | Multiple code examples/tests | **ALWAYS** |
| `Deprecated:` | Marks entity as deprecated | **ALWAYS** |
| `Authors:` | List of authors | **KEEP** |
| `Copyright:` | Legal information | **KEEP** |
| `License:` | Legal information | **KEEP** |
| `Debug:` | Debug-level docs (excluded from release) | **KEEP** |
| `Macros:` | Define documentation macros | **ALWAYS** |

## Formatting Elements

Ddoc supports markdown-like formatting:

- `_text_` — italic
- `__text__` — bold
- `` `code` `` or `{{code}}` — inline code
- `----` — code block delimiters
- `[[link text](URL)]` — external link
- `[[symbol]]` — internal link to symbol
- `[[module.symbol]]` — link to symbol in module
- `# Heading` — headings (H1-H6)

## Macros

Macros enable reusable documentation patterns:

```d
/**
Macros:
    $(SCALAR int)
*/
/**
Returns a $(SCALAR) value.
*/
int getValue();
```

## Ddoc vs Regular Comments

| Aspect | Ddoc (`/** */`, `///`, `/+ +/`) | Regular (`/* */`, `//`, `/+ +/`) |
|--------|--------------------------------|----------------------------------|
| Extracted by compiler | Yes | No |
| Generates HTML docs | Yes | No |
| `Example:` sections compiled | Yes | N/A |
| Associated with declarations | Yes | No |
| Can be removed freely | **NO** — feeds docs | Yes, if redundant |

## Rules for Fix-Comments Skill

When cleaning up D code comments:

1. **Never remove ddoc blocks** (`/** */`, `///`, `/+ +/`) unless explicitly asked. They feed documentation generators.
2. **Always keep special sections**: `Example:`, `Examples:`, `Deprecated:`, `Macros:`, `Authors:`, `Copyright:`, `License:`.
3. **Ddoc `Example:` sections are tests**: Removing them removes compiled tests.
4. **Regular comments** (`//`, `/* */`) follow normal remove/keep/rewrite rules.
5. **Orphaned ddoc** (not attached to a declaration) is ignored by the compiler — these can be safely removed.
6. **Module-level ddoc** (preceding module declaration) documents the entire module — keep it.

## Detection

A comment is ddoc if it uses:
- `/**` (not `/*`)
- `///` (not `//`)
- `/+` (not `/++` or plain `/+ +/` — note: `/+ +/` with two plus signs IS ddoc)

When in doubt, check if the comment form matches the three ddoc patterns above.
