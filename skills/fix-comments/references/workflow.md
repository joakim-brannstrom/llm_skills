# Fix Comments Workflow — Detailed Steps

## Phase 1: Discovery

- **List target files**: Identify all files in the specified directory/path.
- **Read files completely**: Load each file in full (use chunked reads if needed). Note line counts and structure.
- **Catalog all comments**: Identify every comment, noting:
  - Line number(s)
  - Comment type (block doc `/** */`, line doc `///`, inline `//`)
  - Content summary
  - Adjacent code (what the comment describes)

## Phase 2: Classification

For each comment, classify using the decision rules in `decision-rules.md`:

1. **KEEP** — Non-obvious information not evident from code alone
2. **REMOVE** — Redundant (restates code) or wrong/outdated
3. **REWRITE** — Verbose but useful; condense to 1-2 lines
4. **UNSURE** — Keep and flag in summary with reasoning

## Phase 3: Execution

### Single-File Changes
1. Read the file completely.
2. Apply edits using `editFile` for targeted removals.
3. Verify immediately by re-reading affected sections.

### Multi-File or Bulk Changes
1. Read all files first. Complete classification before any edits.
2. Write a Python script to perform bulk edits:
   - Track line numbers carefully (adjust for shifts after each removal).
   - Prefer pattern-based removal over line-number-based when possible.
3. Execute the script and verify results.
4. Clean up artifacts: Remove extra blank lines, fix indentation issues.

### Edit Safety Rules
- **Never edit based on assumed line numbers** — always verify current state.
- **After each batch of edits**, re-read the affected area to confirm correctness.
- **If edits corrupt the file**, stop and assess damage before continuing.
- **Preserve code structure**: Don't remove blank lines that separate logical sections (keep max 1 blank line between sections).

## Phase 4: Verification

After all edits:
- [ ] Re-read each modified file to confirm no code was accidentally removed.
- [ ] Verify indentation is consistent with file conventions.
- [ ] Check that no extra blank lines were introduced.
- [ ] Confirm all kept comments are still relevant to adjacent code.
- [ ] Ensure doc comment blocks (`/** */`) are properly closed.

## Phase 5: Report

Produce a summary in this structure:

```markdown
## Files Modified

### [filename] ([new_line_count] lines, was [old_line_count])
**Removed (N comments):**
- Line X: `[comment text]` — [reason: obvious from code / task ref / wrong]
- Line Y: `[comment text]` — [reason]

**Kept (notable):**
- Line A: `[comment text]` — [reason: explains non-obvious behavior]

### [filename] — No changes needed
[Brief reason]

## Comments Flagged as Unsure
(None, or list with location, text, and reasoning)
```

## Error Recovery

If edits go wrong:
1. **Stop immediately**. Don't compound errors.
2. **Assess damage**: Read the file to understand what's broken.
3. **If possible, reverse**: Use git checkout or rewrite from known-good state.
4. **If no backup**: Read remaining content, reconstruct missing parts from context, and rewrite carefully.
5. **Consider script-based approach**: For bulk changes, a Python script with careful line tracking is safer than sequential `editFile` calls.
