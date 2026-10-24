"""Educational grid-based autonomous navigation simulator (not for real vehicles)."""
import heapq
import tkinter as tk
from time import perf_counter

ROWS = COLS = 15
START = (1, 1)
GOAL = (13, 13)
INITIAL_OBSTACLES = {(r, 5) for r in range(2, 12)} | {(r, 10) for r in range(3, 13)}
CELL = 34


def astar(start, goal, obstacles, rows=ROWS, cols=COLS):
    """Return a shortest 4-direction grid path, or [] if unreachable."""
    if not (0 <= start[0] < rows and 0 <= start[1] < cols):
        return []
    if not (0 <= goal[0] < rows and 0 <= goal[1] < cols):
        return []
    if start in obstacles or goal in obstacles:
        return []
    def h(pos):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
    frontier = [(h(start), 0, start)]
    came_from = {}
    best_cost = {start: 0}
    while frontier:
        _, cost, current = heapq.heappop(frontier)
        if cost != best_cost.get(current):
            continue
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]
        r, c = current
        for nxt in ((r+1,c),(r-1,c),(r,c+1),(r,c-1)):
            if not (0 <= nxt[0] < rows and 0 <= nxt[1] < cols) or nxt in obstacles:
                continue
            new_cost = cost + 1
            if new_cost < best_cost.get(nxt, float('inf')):
                best_cost[nxt] = new_cost
                came_from[nxt] = current
                heapq.heappush(frontier, (new_cost + h(nxt), new_cost, nxt))
    return []


class Simulator:
    def __init__(self, root):
        self.root = root
        root.title('Autonomous Vehicle Navigation Simulator | A*')
        self.canvas = tk.Canvas(root, width=COLS*CELL, height=ROWS*CELL, bg='white')
        self.canvas.pack(padx=12, pady=10)
        self.canvas.bind('<Button-1>', self.toggle_obstacle)
        controls = tk.Frame(root)
        controls.pack(pady=4)
        tk.Button(controls, text='Start / Resume', command=self.start).pack(side='left', padx=5)
        tk.Button(controls, text='Pause', command=self.pause).pack(side='left', padx=5)
        tk.Button(controls, text='Reset', command=self.reset).pack(side='left', padx=5)
        self.status = tk.StringVar()
        tk.Label(root, textvariable=self.status, font=('Segoe UI', 10)).pack(pady=6)
        tk.Label(root, text='Click a cell to add/remove an obstacle. Blue = car, Green = goal, Yellow = planned route.', font=('Segoe UI', 9)).pack(pady=(0, 12))
        self.reset()

    def reset(self):
        self.pause()
        self.car = START
        self.obstacles = set(INITIAL_OBSTACLES)
        self.steps = 0
        self.replans = 0
        self.plan()

    def plan(self):
        start_time = perf_counter()
        self.path = astar(self.car, GOAL, self.obstacles)
        elapsed = (perf_counter() - start_time)*1000
        self.replans += 1
        if self.car == GOAL:
            message = 'Destination reached!'
        elif not self.path:
            message = 'No route available. Remove some obstacles.'
            self.pause()
        else:
            message = f'Route: {len(self.path)-1} moves | Steps traveled: {self.steps} | Plans: {self.replans} | Planning: {elapsed:.2f} ms'
        self.status.set(message)
        self.draw()

    def toggle_obstacle(self, event):
        pos = (event.y // CELL, event.x // CELL)
        if not (0 <= pos[0] < ROWS and 0 <= pos[1] < COLS) or pos in (self.car, GOAL, START):
            return
        if pos in self.obstacles:
            self.obstacles.remove(pos)
        else:
            self.obstacles.add(pos)
        self.plan()

    def draw(self):
        self.canvas.delete('all')
        route = set(self.path)
        for r in range(ROWS):
            for c in range(COLS):
                pos = (r,c)
                fill = '#f1f5f9'
                if pos in route: fill = '#fde68a'
                if pos in self.obstacles: fill = '#475569'
                if pos == GOAL: fill = '#22c55e'
                if pos == self.car: fill = '#2563eb'
                x, y = c*CELL, r*CELL
                self.canvas.create_rectangle(x,y,x+CELL,y+CELL,fill=fill,outline='#cbd5e1')
                if pos == self.car: self.canvas.create_text(x+CELL/2,y+CELL/2,text='C',fill='white',font=('Segoe UI',12,'bold'))
                elif pos == GOAL: self.canvas.create_text(x+CELL/2,y+CELL/2,text='G',fill='white',font=('Segoe UI',12,'bold'))

    def start(self):
        if not self.running and self.car != GOAL and self.path:
            self.running = True
            self.tick()

    def tick(self):
        if not self.running:
            return
        if len(self.path) <= 1:
            self.pause()
            self.plan()
            return
        nxt = self.path[1]
        if nxt in self.obstacles:
            self.plan()
            if not self.path: return
            nxt = self.path[1]
        self.car = nxt
        self.steps += 1
        self.path = self.path[1:]
        self.draw()
        if self.car == GOAL:
            self.pause()
            self.status.set(f'Destination reached in {self.steps} moves! Plans: {self.replans}')
        else:
            self.status.set(f'Moving | Steps: {self.steps} | Remaining: {len(self.path)-1} | Plans: {self.replans}')
            self.job = self.root.after(220, self.tick)

    def pause(self):
        self.running = False
        if getattr(self, 'job', None) is not None:
            self.root.after_cancel(self.job)
            self.job = None


if __name__ == '__main__':
    root = tk.Tk()
    Simulator(root)
    root.mainloop()
