# Decision Rules — Concrete Criteria

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

## UNSURE — Keep and Flag

When uncertain, keep the comment and note in the summary:
- Location (file:line)
- Comment text
- Why it might be removable
- Why you're uncertain
