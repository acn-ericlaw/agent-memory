// test_memory_lint.mjs — node mirror of test_memory_lint.py.
// Same fixtures, same expectations: this is the cross-runtime contract that
// keeps memory-lint.mjs at parity with memory-lint.py. Run: node --test <file>
import { test } from "node:test";
import assert from "node:assert/strict";
import { pinned_open_threads, memref_ids } from "./memory-lint.mjs";

function byCodePoint(a, b) {
  if (a < b) return -1;
  if (a > b) return 1;
  return 0;
}
const sortedArr = (s) => [...s].sort(byCodePoint);
const assertPins = (text, expected) =>
  assert.deepEqual(sortedArr(pinned_open_threads(text)), [...expected].sort(byCodePoint));

test("pinned_open_threads flat", () => {
  assertPins(
    `
- [ ] Parent task
  <!-- id: t1 -->
- [x] Done task
  <!-- id: t2 -->
`,
    ["t1"]
  );
});

test("pinned_open_threads nested", () => {
  // Nested list inside an open thread
  assertPins(
    `
- [ ] Parent task
  - Subtask 1
  - Subtask 2
  <!-- id: t3 -->
`,
    ["t3"]
  );
});

test("pinned_open_threads nested open", () => {
  assertPins(
    `
- [ ] Parent task
  - [ ] Nested open
    <!-- id: t4 -->
`,
    ["t4"]
  );
});

test("pinned_open_threads sibling reset", () => {
  assertPins(
    `
- [ ] Parent task
  <!-- id: t5 -->
- Regular bullet that should reset
  <!-- id: t6 -->
`,
    ["t5"]
  );
});

test("pinned_open_threads mixed", () => {
  assertPins(
    `
- [ ] Open task 1
  - Subtask
  <!-- id: mix-1 -->
- [x] Done task
  <!-- id: mix-2 -->
- [ ] Open task 2
  <!-- id: mix-3 -->
- Regular sub-bullet
  <!-- id: mix-4 -->
`,
    ["mix-1", "mix-3"]
  );
});

test("memref_ids ignores prose and review-summary mentions (ot-review-step6-prose)", () => {
  // A fact named only in prose / a '## Memory Review' summary is NOT a use —
  // only '## Memory References' counts.
  const text = `# Session
## What happened
Archiving \`foo-fact\` because it is overdue.
## Memory Review (2026-06-19)
- Archived: 1 (\`foo-fact\` -> archive, faded)
- Tier changes: foo-fact archive-candidate->archived
## Memory References
- Created: bar-fact
- Referenced: baz-fact
`;
  const ids = memref_ids(text);
  assert.ok(ids.has("bar-fact"));
  assert.ok(ids.has("baz-fact"));
  assert.ok(!ids.has("foo-fact")); // prose / review-summary mention is not a reference
});

test("memref_ids is bounded by the next heading", () => {
  const text = `## Memory References
- Referenced: in-block-id
## Next Section
- not-a-ref-id mentioned here
`;
  const ids = memref_ids(text);
  assert.ok(ids.has("in-block-id"));
  assert.ok(!ids.has("not-a-ref-id"));
});
