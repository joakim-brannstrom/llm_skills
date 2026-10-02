# Decision Rules — Concrete Criteria

## Scope

What may be edited is defined in `SKILL.md` (Scope): all comment forms —
including ddoc, which is **not protected** — comments inside unittests,
descriptive string literals (UDA description strings on unittests, strings
used inside unittests), and markdown docs. Identifiers and non-descriptive
string literals are out of scope: leave them and list them in the report.
Plan-artifact references in scope are never kept — see
`references/plan-artifacts.md`.

## Comment Style Rules

When rewriting or evaluating comments, enforce these style guidelines:

- **Concise**: 1-2 lines max. Break longer explanations into separate short comments.
- **No hard-wrapping**: Do not wrap to a fixed column width. Let lines flow naturally.
- **No mid-sentence breaks**: Each line should be a complete thought, not a sentence split across lines.
- **Simple language**: ASD-STE100 Simplified Technical English. Short words, short sentences.
- **Code first, comments later**: Write code first. Add comments only where genuinely needed.

## Always Remove

| Pattern | Example | Reason |
|---------|---------|--------|
| Task references | `// --- Task 15: Configurable buffer ---` | Process artifact, not implementation |
| Obvious variable descriptions | `// Token array` before `tokens = new T[n]` | Name + type + code = full info |
| Obvious method descriptions | `/// Access the raw pointer.` before `ptr() { return _ptr; }` | Signature says it all |
| Obvious control flow | `// First pass: query size` before size query code | Code structure shows it |
| Duplicate parameter docs | `// func(a, b, c)` before `func(a, b, c)` | Redundant listing |
| Obvious null/error checks | `// Null check prevents crash` before `if (x is null)` | Defensive pattern is evident |
| Section markers | `// --- Unit tests ---` | Visual noise, no semantic value |
| Wrong/outdated content | Comment describes behavior code doesn't implement | Misleading |
| Line-number reference | `// actual logic is on line 42` | Brittle: any edit above shifts lines, the reference silently rots |

Task references into a plan or requirements document are a distinct case — the referenced documents are ephemeral and the references are never kept: see `references/plan-artifacts.md` for scope rules (comments, test strings, docs vs. code) and rephrasing patterns.

## Line-Number References

Comments that locate code **within the same file** by line number are brittle:
any insertion or deletion above them shifts lines, and the reference silently
goes stale. Always remove or rewrite:

- **Rewrite** to a stable anchor: a symbol, function, type, or section name.
- **Remove** the comment if the line reference is all it says.
- **Never** put a line number into a comment, even if it is currently correct.

| Before | After |
|--------|-------|
| `// actual logic is on line 42` | `// actual logic in validate()` |
| `// flag is set at line 120` | `// flag is set in the constructor` |
| `// TODO: fix line 300` | `// TODO: fix the resize bug` (remove if nothing else to say) |

Line numbers of *external* artifacts (a parser's error output, another tool's
input) are data, not navigation — judge them with the normal rules.

## Always Keep

| Pattern | Example | Reason |
|---------|---------|--------|
| Architecture explanation | "Uses facade pattern because..." | Not visible in code |
| Non-obvious edge cases | "Zero-token batch causes undefined behavior in C lib" | Critical gotcha |
| External API behavior | "llama_encode doesn't use KV cache unlike llama_decode" | External knowledge |
| Thread-safety notes | "NOT thread-safe: data race on _destroyed flag" | Critical contract |
| Lifecycle guarantees | "Idempotent — safe to call multiple times" | Behavioral contract |
| Specific init values | "Pre-allocated with all 1s (one per token)" | Value not in name |
| Field relationships | "Each entry points to corresponding _storage entry" | Relationship not obvious |
| Module/class docs | Purpose, design rationale, interface explanation | Context for readers |
| License info | `License: MPL-2.0` | Legal requirement |

## Keep in Unit Tests

- Test purpose descriptions (what scenario is being tested)
- Test limitation notes (why full testing isn't possible)
- Integration test instructions (how to enable with real data)

Also in scope inside unittests (see `SKILL.md` Scope):
- UDA description strings: `@("...")` on the line above `unittest {`.
- Strings used inside unittests: assert messages, expected-output strings.

These commonly carry plan-artifact references, which must be removed or
rephrased. A minimal rewrite of the test itself is allowed when the string
change requires it; the test must verify exactly the same thing afterwards.

## UNSURE — Keep and Flag

When uncertain, keep the comment and note in the summary:
- Location (file:line)
- Comment text
- Why it might be removable
- Why you're uncertain
