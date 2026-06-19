// test_memory_lint.mjs — node mirror of test_memory_lint.py.
// Same fixtures, same expectations: this is the cross-runtime contract that
// keeps memory-lint.mjs at parity with memory-lint.py. Run: node --test <file>
import { test } from "node:test";
import assert from "node:assert/strict";
import { pinned_open_threads } from "./memory-lint.mjs";

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
