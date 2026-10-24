# Autonomous Vehicle Navigation Simulator

A **Python/Tkinter educational simulation** demonstrating A* pathfinding, obstacle avoidance, and route replanning on a 15×15 grid. This is a discrete grid navigation demo, **not real vehicle control software**.

## Windows setup

1. Install Python 3 from https://www.python.org/downloads/windows/ (with Tcl/Tk support, included in the standard installer).
2. Open this folder in VS Code.
3. In the VS Code terminal (PowerShell), run:
   ```powershell
   py main.py
   ```
   If `py` is unavailable, use `python main.py`.

## Controls

- **Start / Resume:** Animate the car along the current shortest path.
- **Pause:** Stop movement.
- **Reset:** Restore the starting map and counters.
- **Click grid cells:** Add or remove obstacles. The car replans immediately.
- **Colors:** Blue car, green goal, dark obstacles, yellow planned path.

## Run tests

```powershell
py -m unittest discover -v
```

## How it works

A* uses a priority queue, a movement cost of 1 per cell, and Manhattan distance as its heuristic. The resulting shortest route is animated one cell at a time. Clicking a cell triggers a new route search. If no route exists, movement stops safely.

## Next improvements

- Add randomly generated maps with a seed.
- Export route metrics to CSV.
- Compare A* against Dijkstra's algorithm.
- Add a more realistic continuous vehicle model.

## Reference and credit

Inspired by the learning topics in [ShisatoYano/AutonomousVehicleControlBeginnersGuide](https://github.com/ShisatoYano/AutonomousVehicleControlBeginnersGuide). This implementation is standalone and does not copy that repository's code.
