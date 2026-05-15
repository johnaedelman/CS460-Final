# Development Log – The Torchbearer

**Student Name:** John Edelman
**Student ID:** 131418570

> Instructions: Write at least four dated entries. Required entry types are marked below.
> Two to five sentences per entry is sufficient. Write entries as you go, not all in one
> sitting. Graders check that entries reflect genuine work across multiple sessions.
> Delete all blockquotes before submitting.

---

## Entry 1 – 5/14/26: Initial Plan

> Required. Write this before writing any code. Describe your plan: what you will
> implement first, what parts you expect to be difficult, and how you plan to test.

I will implement my functions in the order that is recommended in the assignment description, beginning by implementing Dijkstra's algorithm to find the shortest paths between chambers. My expectation is that I will have some trouble figuring out how to put together the pieces of the complete solution to the problem, particularly with incorporating pruning. I will test with the provided test cases, as well as creating some of my own edge cases to ensure correctness.

---

## Entry 2 – 5/14/26: Minor bug fix
> Required. At least one entry must describe a bug, wrong assumption, or design change
> you encountered. Describe what went wrong and how you resolved it.

While implementing precompute_distances(), I was having an odd issue with the source selection wherein it would only return None, which was bugging me for a few minutes. Unfortunately, it turned out to be one of those bugs that is embarassingly obvious once you figure it out, and I am including it here as a testament to the fact that one should remember to get up and take a breather every once in a while when programming: I was returning "relics.insert(0, spawn)", which, as you may realize, is a function that does not return anything.

---

## Entry 3 – [Date]: [Short description]

_Your entry here._

---

## Entry 4 – [Date]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

_Your entry here._

---

## Final Entry – [Date]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | |
| Part 2: Precomputation Design | |
| Part 3: Algorithm Correctness | |
| Part 4: Search Design | |
| Part 5: State and Search Space | |
| Part 6: Pruning | |
| Part 7: Implementation | |
| README and DEVLOG writing | |
| **Total** | |
