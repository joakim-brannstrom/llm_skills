# Decision Report — Quality Checklist

Defects observed in real decision reports (structure rot, conversion damage,
evaluation drift). Check every item before delivering.

## Structure defects (never ship)

- [ ] Every heading at one level (e.g. all `##`): use real hierarchy — `#`
      title, `##` part, `###` section, `####` subsection. Numbering supports
      hierarchy but never replaces heading levels.
- [ ] List items promoted to headings (e.g. a step rendered as `## 2. Local
      testing`). Steps belong in numbered lists or `Step | Description` tables.
- [ ] Mangled table of contents: page numbers that rot, doubled rows, entries
      not matching body headings. Prefer a plain nested list without page numbers.
- [ ] One logical table split into several tables with repeated header rows.
- [ ] Conversion artifacts in text: stray page numbers, `■` bullets, garbled
      words mid-sentence, a heading that is a mangled word (e.g. `++` from a
      broken "C++" bullet).

## Content defects

- [ ] Criteria invented or redefined during evaluation of a later option.
- [ ] An alternative evaluated against a subset of criteria without a stated
      reason.
- [ ] "Do nothing" alternative missing.
- [ ] Verdict scales mixed within one section (OK/NOK beside Strong/Weak).
- [ ] Unquantified claims where a number exists (sizes, wait times, counts).
- [ ] Open questions silently resolved instead of marked in the text.
- [ ] Background section contains facts no criterion or option depends on.

## Consistency

- [ ] TOC entries == actual headings (names and order).
- [ ] Criterion names identical everywhere (copy the §3 list verbatim).
- [ ] One language throughout; established domain terms may stay in their
      original language but consistently so.
- [ ] Every dated note carries a real date.
- [ ] The summary comparison table covers every alternative described in §4.

## Delivery checks

1. Re-read §3 criteria as a skeptic: are they fair, measurable, and free of
   wording that pre-decides the winner?
2. Re-read the leading alternative: could a team start tomorrow with only what
   is written down?
3. Skim headings + tables only: does the argument survive without the prose?
