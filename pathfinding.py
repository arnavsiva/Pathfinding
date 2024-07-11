import tkinter as tk
import time

def create_grid(event=None):
    canvas.delete('grid_line')

    grid_size = 12
    cell_size = 50

    for i in range(0, grid_size * cell_size, cell_size):
        canvas.create_line([(i, 0), (i, grid_size * cell_size)], tag='grid_line')
        canvas.create_line([(0, i), (grid_size * cell_size, i)], tag='grid_line')

def mouse_click(event):
    global start, end, setting_obstacles, status_label, pathfinding_started

    grid_size = 12

    if pathfinding_started:
        return

    x, y = event.x // 50, event.y // 50

    if x >= grid_size or y >= grid_size:
        return

    if (x, y) == start or (x, y) == end or (x, y) in obstacles:
        return

    if not start:
        start = (x, y)
        canvas.create_rectangle(x*50, y*50, x*50+50, y*50+50, fill='blue')
        status_label.config(text="Select End Point")
    elif not end:
        end = (x, y)
        canvas.create_rectangle(x*50, y*50, x*50+50, y*50+50, fill='purple')
        status_label.config(text="Click to place obstacles, then press space to start pathfinding")
        setting_obstacles = True
    elif setting_obstacles:
        obstacles.add((x, y))
        canvas.create_rectangle(x*50, y*50, x*50+50, y*50+50, fill='black')

def start_pathfinding(event):
    global start, end, obstacles, status_label, pathfinding_started

    if not pathfinding_started and start and end:
        pathfinding_started = True
        status_label.config(text="Pathfinding in progress...")
        path = find_path(start, end, obstacles)
        
        pathfinding_started = False
        if path:
            for cell in path:
                canvas.create_rectangle(cell[0]*50, cell[1]*50, cell[0]*50+50, cell[1]*50+50, fill='green')
            status_label.config(text=f"Found best path. Length: {len(path)} squares. Press 'r' to reset.")
        else:
            status_label.config(text="No path found. Press 'r' to reset.")

def reset_grid():
    global start, end, setting_obstacles, obstacles, status_label, pathfinding_started

    start = None
    end = None
    setting_obstacles = False
    pathfinding_started = False
    obstacles.clear()
    canvas.delete('all')
    create_grid()
    status_label.config(text="Select Start Point")

def find_path(start, end, obstacles):
    queue = [(start, [start])]
    seen = set(start)

    while queue:
        (x, y), path = queue.pop(0)
        canvas.create_rectangle(x*50, y*50, x*50+50, y*50+50, fill='orange')
        root.update()
        time.sleep(0.01)

        if (x, y) == end:
            return path
        for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if 0 <= nx < 12 and 0 <= ny < 12 and (nx, ny) not in obstacles and (nx, ny) not in seen:
                seen.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))

start, end = None, None
setting_obstacles = False
obstacles = set()
pathfinding_started = False

root = tk.Tk()
root.title("Pathfinding")

status_label = tk.Label(root, text="Select Start Point", font=("Helvetica", 12))
status_label.pack()

canvas = tk.Canvas(root, height=600, width=600, bg='white')
canvas.pack(fill=tk.BOTH, expand=True)

canvas.bind('<Configure>', create_grid)
canvas.bind('<Button-1>', mouse_click)
root.bind('<space>', start_pathfinding)
root.bind('<r>', lambda event: reset_grid())

root.mainloop()