# Ddoc Handling for D Code

Ddoc is D's embedded documentation system. Ddoc comments are extracted at compile
time and formatted into HTML documentation pages. For this skill, ddoc comments
are **not protected**: they are judged by the same remove / keep / rewrite rules
as regular comments. "Feeds a documentation generator" is not a keep-reason.

## Ddoc Comment Forms

Three forms are recognized as ddoc:

| Form | Example | Notes |
|------|---------|-------|
| `/** ... */` | `/** Multi-line ddoc. */` | Two asterisks after opening `/` |
| `/++ ... +/` | `/++ Plus-delimited ddoc. +/` | Two plus signs after opening `/`; closing may be `+/` or `++/` |
| `///` | `/// One-line ddoc.` | Three slashes |

Regular comments (`//`, `/* */`, `/+ +/`) are **not** ddoc. In particular, a
single-plus `/+ ... +/` (including nested `/+ /+ ... +/ +/`) is a regular
comment, not ddoc — verified empirically against LDC 1.42 (`ldc2 -D` output
omits it, includes `/++ ... +/`).

## Association Rules

- Ddoc comments are associated with the **next declaration**.
- Multiple ddoc comments for the same declaration are **concatenated**.
- Ddoc comments **not** associated with a declaration are **ignored** by the compiler.
- Comments preceding the `ModuleDeclaration` apply to the **entire module**.
- Comments on the same line as a declaration apply to **that declaration**.

## Special Sections (functional, not just documentation)

Ddoc special sections start with a keyword followed by a colon. Several are
**functional** — they affect compilation or documentation output:

| Section | Purpose | Handling |
|---------|---------|----------|
| `Example:` | Code compiled and run as a test | In scope — but it IS a test: a change must not alter what the example verifies. Report every touched section. |
| `Examples:` | Multiple code examples/tests | Same as `Example:` |
| `Deprecated:` | Marks entity as deprecated | In scope; report changes (affects compilation deprecation warnings) |
| `Macros:` | Define documentation macros | In scope; report changes (affects other ddoc blocks using the macro) |
| `Authors:` | List of authors | Keep |
| `Copyright:` | Legal information | Keep |
| `License:` | Legal information | Keep |
| `Debug:` | Debug-level docs (excluded from release) | In scope like other prose |

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

| Aspect | Ddoc (`/** */`, `/++ ... +/`, `///`) | Regular (`/* */`, `//`, `/+ +/`) |
|--------|--------------------------------|----------------------------------|
| Extracted by compiler | Yes | No |
| Generates HTML docs | Yes | No |
| `Example:` sections compiled | Yes | N/A |
| Associated with declarations | Yes | No |
| Fix-comments scope | In scope — same rules as regular comments | In scope |

## Rules for Fix-Comments Skill

When cleaning up D code comments:

1. **Ddoc is not protected.** `/** */`, `/++ ... +/`, and `///` blocks are
   judged by the normal decision rules (KEEP/REMOVE/REWRITE/UNSURE) exactly
   like regular comments. Obvious ddoc is removed; valuable ddoc is kept;
   outdated ddoc is updated to match the code.
2. **`Example:`/`Examples:` sections are compiled and run as tests.** They
   are in scope (they are tests, and test code may be rewritten when needed),
   but a change must not alter what the example verifies. Prefer removing or
   rewording only the surrounding prose; report every touched section in the
   run report.
3. **Legal/attribution sections** (`Copyright:`, `License:`, `Authors:`) are
   kept.
4. **Orphaned ddoc** (not attached to a declaration) is ignored by the
   compiler — remove it when it fails the normal rules.
5. **Module-level ddoc** (preceding the module declaration) documents the
   entire module — keep it when it carries real content; clean it like any
   other comment when it doesn't.

## Detection

A comment is ddoc if it uses:
- `/**` (not `/*`)
- `///` (not `//`)
- `/++` (two plus signs after the opening `/`; a single `/+` is a regular
  nested comment — verified against LDC 1.42)

When in doubt, check if the comment form matches the three ddoc patterns above.
