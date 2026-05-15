# The Torchbearer

**Student Name:** John Edelman
**Student ID:** 131418570
**Course:** CS 460 – Algorithms | Spring 2026

---

## Part 1: Problem Analysis

- **Why a single shortest-path run from S is not enough:**
  We are not simply finding the shortest path from S to T. Our path must route through every relic chamber, and in particular it must be the cheapest route which does so.

- **What decision remains after all inter-location costs are known:**
  The shortest choice of route which visits every relic room as well as the exit.

- **Why this requires a search over orders (one sentence):**
  Even routes that go through the same chambers may have different costs if the order is different, and therefore committing to a next step without searching over orders leaves the possibility of a better future route being opened by a path that a simple greedy algorithm would not have found yet.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

| Source Node Type | Why it is a source |
|---|---|
| Entrance node | The Torchbearer always begins at the entrance node. |
| Relic chamber | Each relic must be visited in our final path, so we need to know the outward costs from each relic.|

### Part 2b: Distance Storage

| Property | Your answer |
|---|---|
| Data structure name | 2D dictionary |
| What the keys represent | With a source and destination key, one can look up the distance between the source and the destination. |
| What the values represent | The minimum fuel cost between the two nodes |
| Lookup time complexity | O(1) |
| Why O(1) lookup is possible | Dictionaries offer O(1) lookup time regardless of size through hashing. |

### Part 2c: Precomputation Complexity

- **Number of Dijkstra runs:** Since the set of relic chambers is of size k, we will have k + 1 Dijkstra runs (one extra for the entrance node S).
- **Cost per run:** O(m log n), where m is the number of edges in the graph and n is the number of nodes.
- **Total complexity:** O((k+1)*(m log n)).
- **Justification (one line):** We must run Dijkstra's once for each of the k + 1 source nodes, and each run has complexity O(m log n).

---

## Part 3: Algorithm Correctness

### Part 3a: What the Invariant Means

- **For nodes already finalized (in S):**
  For every node v which has been finalized, the current estimate of the distance from the source x to v is the actual shortest possible path between x and v.

- **For nodes not yet finalized (not in S):**
  For every node u which has not yet been finalized, the current estimate of the distance from the source x to u is the length of the shortest path between x and u which is entirely composed of nodes that have been finalized.

### Part 3b: Why Each Phase Holds

- **Initialization : why the invariant holds before iteration 1:**
  At the beginning, there are no nodes in S, the set of finalized nodes, so the invariant holds vacuously for the nodes in S. 
  The only node which has an estimate for its distance is the source node s, for which dist[s] will be 0. For each other node v, dist[v] is equal to infinity, as there is no path that has been discovered between s and v, so the invariant holds.

- **Maintenance : why finalizing the min-dist node is always correct:**
  The algorithm dequeues a node v from the priority queue, which is guaranteed to have the shortest distance among nodes not in S by the properties of a priority queue. 
  Because the edge weights are nonnegative, no future path going through an unfinalized node could reduce dist[v]; any detour of this nature would only add cost and produce a longer path. Therefore, dist[v] must be optimal, and the invariant holds after moving v into S.

- **Termination : what the invariant guarantees when the algorithm ends:**
  The invariant guarantees that for all nodes in S, the current estimate of the distance from the source to that node is the shortest possible path. Therefore, once all nodes are in S, all paths found will be the shortest ones possible.

### Part 3c: Why This Matters for the Route Planner

If the shortest paths found by Dijkstra's are not correct and the routes are longer than the algorithm predicts, the Torchbearer may either waste fuel by taking an unnecessarily long route or fail to reach the exit at all by running out of fuel.

---

## Part 4: Search Design

### Why Greedy Fails

- **The failure mode:** Greedy will always select the immediate closest node at each step. However, in this problem, it may be necessary to make a less optimal immediate choice to get a better global solution.
- **Counter-example setup:** Consider the following graph:
###
| From \ To | B   | C   | D   | T   | 
| S         | 2   | 1   | 2   | --  |
| B         | --  | 1   | 1   | 1   |
| C         | 100 | --  | 100 | 1   | 
| D         | 1   | 1   | --  | 100 |
###
- **What greedy picks:** The greedy algorithm will go from S to C, as that is the closest node, incurring a cost of 1. However, it is then forced to go to D, with a cost of 100, and then to B, with a cost of 1, and finally to T. This yields a path S -> C -> D -> B -> T, with a cost of 103.
- **What optimal picks:** The optimal algorithm goes to B first (cost 2), then to D (cost 1), then to C (cost 1), and finally to T (cost 1), creating a path S -> B -> D -> C -> T with a total cost of just 5.
- **Why greedy loses:** At each step, it commits to the immediate cheapest edge without considering future possibilities, which can lead to severe trouble in the future.

### What the Algorithm Must Explore

- The algorithm must explore every possible order in which the relics can be visited, as the best global solution cannot be determined without knowledge of all future possibilities.

---

## Part 5: State and Search Space

### Part 5a: State Representation

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | current_loc | node | The node the Torchbearer is currently at. |
| Relics already collected | relics_visited_order | list | An ordered list of the relics which have been visited to reach the current node. |
| Fuel cost so far | cost_so_far | float | The total amount of torch fuel which has been spent to reach the current node. |

### Part 5b: Data Structure for Visited Relics

| Property | Your answer |
|---|---|
| Data structure chosen | set |
| Operation: check if relic already collected | Time complexity: O(1) |
| Operation: mark a relic as collected | Time complexity: O(1) |
| Operation: unmark a relic (backtrack) | Time complexity: O(1) |
| Why this structure fits | We need a structure with fast lookup, insertion, and deletion. Thanks to hashing, set operations can be treated as O(1) time for our purposes (let's leave hash collisions for the Python devs to worry about). |

### Part 5c: Worst-Case Search Space

- **Worst-case number of orders considered:** k!
- **Why:** There are k relics, and therefore k! possible orderings of those relics.

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

- **What is tracked:** A variable best, which is the total fuel cost of the cheapest route which has been discovered in the search so far.
- **When it is used:** In every recursive call to _explore(), before making any more recursive calls, the current accumulated cost plus a lower bound for the remaining cost of the route is compared against best.
- **What it allows the algorithm to skip:** Any branch of the recursion where the pruning algorithm determines that it's impossible to do better than best will terminate early.

### Part 6b: Lower Bound Estimation

- **What information is available at the current state:** The current node, the precomputed distances from each node to every other node, the set of unvisited relics, the order which was taken to reach the current node, the fuel cost of the current route, and the cost of the current best route.
- **What the lower bound accounts for:** It is the cheapest possible cost to finish from the current node. If the cost of the current route plus the minimum amount of fuel it will take to finish it is greater than the cost of the current best route, then the current route is clearly worse.
- **Why it never overestimates:** It uses the precomputed shortest-path distances, which are absolute floors for the cost of traversal. The actual cost of going through the dungeon will, by definition, either be the same or more than the shortest path.

### Part 6c: Pruning Correctness

- Because the lower bound is absolute and will never overestimate thanks to Dijkstra's algorithm, we know that by adding the lower bound to the cost of the route up to current, we get the minimum possible fuel which could conceivably be used to finish the route.
- If this minimum is greater than the fuel cost of the best route, we know that is is impossible to generate a solution better than the current best on this branch of recursion, and thus we can safely prune it.

---

## References

- My own lecture notes, primarily written from the 12:30 PM section of CS 460
- Canvas resources, particularly previous CS 460 assignments, lecture slides, and videos (in particular, my Dijkstra implementation was closely based on the one in the Graphs Practice Quiz)
- Python documentation for the heapq module (https://docs.python.org/3/library/heapq.html)
