# Emergency Rescue Route Planner

A rescue robot finds a path from the Entrance (`A`) to the Patient (`L`)
in a hospital graph using **BFS**, **UCS**, and **IDS**.

## Run
```bash
python3 rescue_route_planner.py
```
Requires Python 3.7+, no external libraries.

## Algorithms
- **BFS** — fewest hops from A to L
- **UCS** — minimum cost path (edge costs defined in `weighted_graph`)
- **IDS** — depth-first search with increasing depth limit

## Sample Output
```
BFS: A -> B -> D -> H -> K -> L   (5 hops)
UCS: A -> C -> G -> J -> K -> L   (cost 8)
IDS: A -> B -> D -> H -> K -> L   (depth 5)
```
