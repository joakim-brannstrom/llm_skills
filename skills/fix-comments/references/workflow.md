# Fix Comments Workflow — Detailed Steps

The run is a **checkpointed per-file loop**. The only state that reliably
survives context compression is what is on disk: the todo list, the edited
files, and the report. Keep in context only the current file and its terse
classification; never hold the whole file set's classification in context.

## Phase 1: Discovery (list only — do not read file contents)

- **List target files**: Identify all files in the specified directory/path.
- **Change-set scoping**: If the target is "files changed since commit X", scope the set with `git diff --name-only X..HEAD`.
- **Reference-removal jobs** (plan artifacts, requirement IDs): pattern-grep the target set to find every occurrence — IDs hide in code-block comments, doc prose, and descriptive strings (unittest UDA descriptions, assert messages) too. Eyeball each hit for false positives. In-scope references are never kept. See `references/plan-artifacts.md`.
- **Write the todo list to disk** (e.g. `scratch/fix-comments/todo.md`), one line per file:
  `- [PENDING] path/to/file`
  The list is the run's checkpoint. It must exist on disk, not only in context —
  compression can summarize or lose an in-context list; the file on disk survives.

## Phase 2: Per-File Loop (one file at a time)

For each file in the todo list, in order:

1. **Read exactly one file** (chunked reads for large files). Do not load the
   other target files into context.
2. **Classify its comments** using `references/decision-rules.md`. Keep the
   classification terse — one line per comment: line, KEEP/REMOVE/REWRITE/
   UNSURE, reason. Classify only the current file.
3. **Reason, then edit** the file:
   - One or few edits: `editFile`.
   - Many edits in one file: prefer one atomic multi-hunk `applyDiff` — a
     failed hunk writes nothing, so no partial state is ever left behind.
   - Cross-reference exception: if another file must be consulted (e.g. an
     anchor link, a shared definition), read only the needed line range
     (`readFile` with startLine/count, or grep) — never the whole file — and
     discard it from working context afterwards.
4. **Verify before marking done**: re-read the edited regions; confirm no code
   was removed (in a repo: `git diff -- <file>` shows comment lines and
   in-scope string literal lines only). If a unittest was touched, confirm
   the rewrite changed no assertion, no expected value, and no coverage, and
   record it under "Tests touched" in the per-file section.
5. **Record progress on disk**:
   - Todo list: change the line to `- [DONE] path (N removed, K kept)`, or
     `- [SKIPPED] path — reason`.
   - Append the per-file report section (Phase 4 format) to
     `scratch/fix-comments/report.md`. Append immediately — never try to
     reconstruct the report from context at the end of the run.
6. **Drop the file**: treat its content as out of scope for the remaining
   files. Do not re-read done files except to fix a verified defect.

If the context has been compressed mid-run: re-read `todo.md` and continue at
the first `[PENDING]`. Done files are already on disk; the report so far is in
`report.md`.

### Exception: pure mechanical bulk replacement

Only when the change needs **no per-comment judgment** (e.g. renaming a
comment banner across many identical files) may a script be used instead of
the loop. Drive it from grep output — do not read the files into context
first — then verify each file with `git diff` and record each in the todo list
and report as above.

### Edit Safety Rules

- **Never edit based on assumed line numbers** — always verify current state.
- **If edits corrupt a file**, stop, assess, and reverse (`git checkout -- <file>`); retry that file alone before continuing.
- **Preserve code structure**: don't remove blank lines that separate logical sections (keep max 1 blank line between sections).

## Phase 3: Final Verification

For files not already verified in the loop:
- [ ] No code was accidentally removed.
- [ ] Indentation matches file conventions; no extra blank lines introduced.
- [ ] Doc comment blocks (`/** */`) properly closed.

## Phase 4: Report

The report is the accumulated `report.md` — one section appended per file as
it was completed. Read it and present it. Per-file section format:

```markdown
### [filename] ([new_line_count] lines, was [old_line_count])
**Removed (N comments):**
- Line X: `[comment text]` — [reason: obvious from code / task ref / wrong]
**Rewritten (N):**
- Line Y: `[old text]` → `[new text]` — [reason: outdated / plan-artifact ref / string cleanup]
**Kept (notable):**
- Line A: `[comment text]` — [reason: explains non-obvious behavior]
**Tests touched:** (None, or file:line — what was rewritten; confirm test behavior unchanged)
**Left in place (out of scope):** (None, or file:line — identifier / non-descriptive string)
**Unsure:** (None, or list with location, text, and reasoning)
```

Close out: delete the scratch files (`scratch/fix-comments/`).

## Error Recovery

1. **Stop immediately**. Don't compound errors.
2. **Assess damage**: Read the affected file to understand what's broken.
3. **Reverse if possible**: `git checkout -- <file>`, then retry that file alone.
4. **If no backup**: Reconstruct from context, or rewrite carefully.
5. **After context compression**: re-read `todo.md` / `report.md` and resume
   at the first `[PENDING]` — do not re-do done files.
