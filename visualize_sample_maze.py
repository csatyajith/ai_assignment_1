from maze import MazeVisualizer, Maze, Cell
import priority_queue as pq


def compute_heuristic(maze: Maze):
    rows, cols = (maze.n_rows, maze.n_cols)
    goal = maze.end
    heuristic_arr = [[(abs(goal.col - i) + abs(goal.row - j)) for i in range(cols)] for j in range(rows)]
    print(heuristic_arr)
    return heuristic_arr


def computePath(queue, maze: Maze, heuristic):
    count = 1
    while 0 != len(queue):
        c = queue.pop()
        c.cell.visited = True
        valid_neighbors = maze.get_neighbors(c.cell)
        if c.cell == maze.end:
            return c.cell
        for item in valid_neighbors:
            queue.push(count, heuristic[item.row][item.col], item, c.cell)
        count = count + 1
    return None


def printPath(path: Cell, mazevis: MazeVisualizer):
    if path != maze_1.start:
        printPath(path.parent,mazevis)
        # print('Row', path.row, 'Col', path.col)
        mazevis.fill_cell(path.row, path.col)


if __name__ == '__main__':
    n_rows = 10  # 10 is better for visualization Change to 51 for project
    n_cols = 10
    maze_1 = Maze(n_rows, n_cols)
    maze_1.reset_visited()
    # print on console
    for r in maze_1.maze:
        print([0 if cell.blocked else 1 for cell in r])

    # plot on matplotlib
    maze_vis = MazeVisualizer(maze_1)
    #maze_vis.show_maze()

    heuristic = compute_heuristic(maze_1)
    start_row = maze_1.start.row
    start_col = maze_1.start.col
    myQueue = pq.Priority_Queue()
    myQueue.push(0, heuristic[start_row][start_col], maze_1.get_cell(start_row, start_col), None)
    target = computePath(myQueue, maze_1, heuristic)
    if target is not None:
        target = target.parent
        print("Path exists")
        printPath(target, maze_vis)
    else:
        print("Path does not exists")
    maze_vis.show_maze()
    # myQueue.print()
