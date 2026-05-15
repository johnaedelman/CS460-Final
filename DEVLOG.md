# Development Log – The Torchbearer

**Student Name:** John Edelman
**Student ID:** 131418570

> Instructions: Write at least four dated entries. Required entry types are marked below.
> Two to five sentences per entry is sufficient. Write entries as you go, not all in one
> sitting. Graders check that entries reflect genuine work across multiple sessions.
> Delete all blockquotes before submitting.

---

## Entry 1 – [5/14/26]: Initial Plan

> Required. Write this before writing any code. Describe your plan: what you will
> implement first, what parts you expect to be difficult, and how you plan to test.

I will implement my functions in the order that is recommended in the assignment description, beginning by implementing Dijkstra's algorithm to find the shortest paths between chambers. My expectation is that I will have some trouble figuring out how to put together the pieces of the complete solution to the problem, particularly with incorporating pruning. I will test with the provided test cases, as well as creating some of my own edge cases to ensure correctness.

---

## Entry 2 – [5/14/26]: Minor bug fix
> Required. At least one entry must describe a bug, wrong assumption, or design change
> you encountered. Describe what went wrong and how you resolved it.

While implementing precompute_distances(), I was having an odd issue with the source selection wherein it would only return None, which was bugging me for a few minutes. Unfortunately, it turned out to be one of those bugs that is embarassingly obvious once you figure it out, and I am including it here as a testament to the fact that one should remember to get up and take a breather every once in a while when programming: I was returning "relics.insert(0, spawn)", which, as you may realize, is a function that does not return anything.

---

## Entry 3 – [5/14/26]: Finished parts 5 and 6

Implemented the find_optimal_route function, its _explore() helper, and subsequently the final solve() function after writing the relevant readme entries to get my thoughts in order. I also made a few bug fixes, like changing the way select_sources works one more time. Kind of funny that I've had to make multiple corrections to it, given how simple it is, but I guess I was a little bit rusty on my Python list behaviors. I'm very close to submission at this point, I'm just going to do another once-over for comments in the code and issues in the readme and then finish the last bits of the devlog.

---

## Entry 4 – [5/14/26]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

I'm pretty happy with the implementation, but I would definitely write some more test cases if I had extra time. I'd like to make sure that I haven't overlooked anything or introduced any weird bugs inadvertently, and I find that a good way to do that is by throwing a bunch of test cases (particularly edge cases) at the problem. As it is, it passes all the given tests plus a couple that I made up but didn't include in my final submission, and I don't see any reason why it would fail further tests, but I suppose the graders will decide my fate in that regard.

---

## Final Entry – [5/14/26]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | 30 minutes |
| Part 2: Precomputation Design | 60 minutes |
| Part 3: Algorithm Correctness | 45 minutes |
| Part 4: Search Design | 60 minutes |
| Part 5: State and Search Space | 30 minutes |
| Part 6: Pruning | 55 minutes |
| Part 7: Implementation | 180 minutes |
| README and DEVLOG writing | 50 minutes |
| **Total** | 510 minutes |
