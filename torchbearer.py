"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: John Edelman
Student ID:   131418570

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.

    """
    return "Why a single shortest-path run from S is not enough: We are not simply finding the shortest path from S to T. Our path must route through every relic chamber, and in particular it must be the cheapest route which does so.\nWhat decision remains after all inter-location costs are known: The shortest choice of route which visits every relic room as well as the exit.\nWhy this requires a search over orders (one sentence): Even routes that go through the same chambers may have different costs if the order is different, and therefore committing to a next step without searching over orders leaves the possibility of a better future route being opened by a path that a simple greedy algorithm would not have found yet."


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.

    """
    # I decided to change this so that it doesn't mess with the input list relics itself.
    return [spawn] + relics  # The list of source nodes will be the list of relic nodes prepended with the spawn node.


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').

    """
    values = {}
    for node in graph:
        values[node] = float('inf')  # Initialize the distance of each node to infinity
    values[source] = 0

    pq = []  # Priority queue to manage which node is selected next
    heapq.heappush(pq, (0, source))

    while pq:
        curr_dist, u = heapq.heappop(pq)

        if curr_dist > values[u]:  # Eliminate unnecessary checks
            continue

        for v, w in graph[u]:
            if values[u] + w < values[v]:  # If the path between u and v is faster than the current known fastest path to v
                values[v] = values[u] + w  # Update the current fastest known path to v; push v into the priority queue
                heapq.heappush(pq, (values[v], v))
    return values


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.

    """
    dist_table = {}
    sources = select_sources(spawn, relics, exit_node)
    for u in sources:  # Run Dijkstra's from each source node and find the distance to every other node.
        dist_table[u] = run_dijkstra(graph, u)  # Add these distances to dist_table, allowing dist_table[u][v] lookups from every source u.
    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.

    """
    return "For nodes already finalized (in S): \nFor every node v which has been finalized, the current estimate of the distance from the source x to v is the actual shortest possible path between x and v. For nodes not yet finalized (not in S): \nFor every node u which has not yet been finalized, the current estimate of the distance from the source x to u is the length of the shortest path between x and u which is entirely composed of nodes that have been finalized.\n" + \
        "Initialization : why the invariant holds before iteration 1: \nAt the beginning, there are no nodes in S, the set of finalized nodes, so the invariant holds vacuously for the nodes in S. The only node which has an estimate for its distance is the source node s, for which dist[s] will be 0. For each other node v, dist[v] is equal to infinity, as there is no path that has been discovered between s and v, so the invariant holds.\nMaintenance : why finalizing the min-dist node is always correct: \nThe algorithm dequeues a node v from the priority queue, which is guaranteed to have the shortest distance among nodes not in S by the properties of a priority queue. Because the edge weights are nonnegative, no future path going through an unfinalized node could reduce dist[v]; any detour of this nature would only add cost and produce a longer path. Therefore, dist[v] must be optimal, and the invariant holds after moving v into S.\nTermination : what the invariant guarantees when the algorithm ends:\nThe invariant guarantees that for all nodes in S, the current estimate of the distance from the source to that node is the shortest possible path. Therefore, once all nodes are in S, all paths found will be the shortest ones possible.\n" + \
        "If the shortest paths found by Dijkstra's are not correct and the routes are longer than the algorithm predicts, the Torchbearer may either waste fuel by taking an unnecessarily long route or fail to reach the exit at all by running out of fuel."


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.

    """
    return "The failure mode: Greedy will always select the immediate closest node at each step. However, in this problem, it may be necessary to make a less optimal immediate choice to get a better global solution.\n" + \
        "Counter-example setup: Consider the following graph:\n| From \\ To | B   | C   | D   | T   |\n|-----------|-----|-----|-----|-----|\n| S         | 2   | 1   | 2   | --  |\n| B         | --  | 1   | 1   | 1   |\n| C         | 100 | --  | 100 | 1   |\n| D         | 1   | 1   | --  | 100 |\n" + \
        "What greedy picks: The greedy algorithm will go from S to C, as that is the closest node, incurring a cost of 1. However, it is then forced to go to D, with a cost of 100, and then to B, with a cost of 1, and finally to T. This yields a path S -> C -> D -> B -> T, with a cost of 103.\n" + \
        "What optimal picks: The optimal algorithm goes to B first (cost 2), then to D (cost 1), then to C (cost 1), and finally to T (cost 1), creating a path S -> B -> D -> C -> T with a total cost of just 5.\n" + \
        "Why greedy loses: At each step, it commits to the immediate cheapest edge without considering future possibilities, which can lead to severe trouble in the future."


# =============================================================================
# PARTS 5 + 6
# =============================================================================


def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    # Stores the best route as a mutable list instead of a tuple so it can be modified without returning from _explore. If no better route is found, it will return an empty route with infinite distance
    best_route = [float('inf'), []]
    _explore(dist_table, spawn, set(relics), [], 0, exit_node, best_route)  # Begins the recursive call stack
    return tuple(best_route)


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    TODO
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    # The pruning condition. If the cost so far plus the lower bound for the possible remaining cost is greater than the best route,
    # then we know there is no possible way for an optimal solution to crop up in this branch of recursion.
    if relics_remaining:
        lower_bound = min(dist_table[current_loc][relic] for relic in relics_remaining) + min(dist_table[relic][exit_node] for relic in relics_remaining)
    else:
        lower_bound = dist_table[current_loc][exit_node]
    if cost_so_far + lower_bound >= best[0]:
        return

    # Base case: all of the relic rooms have been explored
    if not relics_remaining:
        cost_so_far += dist_table[current_loc][exit_node]
        if cost_so_far < best[0]:
            best[0], best[1] = cost_so_far, relics_visited_order.copy()
        return

    # Continue making recursive calls
    for relic in relics_remaining:
        # Search through routes where we choose the current relic as the next one to visit
        relics_remaining.remove(relic)
        relics_visited_order.append(relic)
        _explore(dist_table, relic, relics_remaining, relics_visited_order, cost_so_far + dist_table[current_loc][relic], exit_node, best)
        # Backtrack: reset the state of relics_remaining and relics_visited_order so that we can search through routes where we do not choose the current relic as the next one to visit
        relics_remaining.add(relic)
        relics_visited_order.pop(-1)


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    # Combines everything else, finding the optimal route based on the precomputed distances
    return find_optimal_route(precompute_distances(graph, spawn, relics, exit_node), spawn, relics, exit_node)


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
