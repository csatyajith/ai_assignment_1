from maze import MazeVisualizer, Maze, Cell
import priority_queue as pq
import matplotlib.pyplot as plt

moves = 1

def compute_heuristic(maze: Maze):
    rows, cols = (maze.n_rows, maze.n_cols)
    goal = maze.end
    heuristic_arr = [[(abs(goal.col - i) + abs(goal.row - j)) for i in range(cols)] for j in range(rows)]
    print(heuristic_arr)
    return heuristic_arr


def computePath(queue, maze: Maze, heuristic):
    global moves
    moves = 1
    while 0 != len(queue):
        c = queue.pop()
        if c.cell.parent is not None:
            c.cell.parent.child.append(c.cell)
        c.cell.visited = True
        valid_neighbors = maze.get_neighbors(c.cell)
        if c.cell == maze.end:
            return c.cell
        for item in valid_neighbors:
            queue.push(moves, heuristic[item.row][item.col], item, c.cell)
        moves = moves + 1
    return None


def printPath(path: Cell, mazevis: MazeVisualizer):
    while path != maze_1.start:
        mazevis.fill_cell(path.row, path.col)
        #print('Row', path.row, 'Col', path.col)
        path = path.parent


def updatePath(path: Cell, mazevis: MazeVisualizer, new_heuristics, count):
    while path != maze_1.start:
        for i in path.child:
            new_heuristics[i.row][i.col] = count
        mazevis.fill_cell(path.row, path.col)
        #print('Row', path.row, 'Col', path.col)
        count = count + 1
        path = path.parent
    new_heuristics[path.row][path.col] = count  # for start cell


if __name__ == '__main__':
    t, times = 0, 1
    n_rows = 50  # 10 is better for visualization Change to 51 for project
    n_cols = 50
    maze_1 = Maze(n_rows, n_cols)
    maze_1.end = maze_1.get_endPoint()
    heuristic = compute_heuristic(maze_1)
    new_heuristics = list(heuristic)
    moves_1 = []
    moves_2 = []
    time_x = []

    while t != times:
        maze_1.start = maze_1.get_endPoint()
        if maze_1.start == maze_1.end:
            # retry once if start and end are same
            maze_1.start = maze_1.get_endPoint()
        maze_1.reset_visited()
        # print on console
        # for r in maze_1.maze:
        #    print([0 if cell.blocked else 1 for cell in r])

        # plot on matplotlib
        maze_vis = MazeVisualizer(maze_1)
        # maze_vis.show_maze()

        start_row = maze_1.start.row
        start_col = maze_1.start.col
        myQueue = pq.Priority_Queue()
        myQueue.push(0, heuristic[start_row][start_col], maze_1.get_cell(start_row, start_col), None)

        target = computePath(myQueue, maze_1, heuristic)
        if target is not None:
            target = target.parent
            print("Path exists")
            printPath(target, maze_vis)
            print('a* moves', moves)
        else:
            print("Path does not exists")
        moves_1.append(moves)
        # maze_vis.show_maze()
        '''
        # For adaptive A*
        maze_1.reset_visited()
        myQueue.remove_all()
        myQueue.push(0, new_heuristics[start_row][start_col], maze_1.get_cell(start_row, start_col), None)
        target = computePath(myQueue, maze_1, new_heuristics)
        if target is not None:
            target = target.parent
            print("Adaptive * path exists")
            count = 1
            updatePath(target, maze_vis, new_heuristics, count)
            for h in new_heuristics:
                print(h)
            print('adaptive a* moves', moves)
        else:
            print("Path does not exists")
        moves_2.append(moves)
        '''
        maze_vis.show_maze()
        t = t + 1
        time_x.append(t)
'''
    plt.figure()
    plt.plot(time_x, moves_1, color='g')
    plt.plot(time_x, moves_2, color='orange')
    #print(moves_1)
    #print(moves_2)
    plt.xlabel('Iteration')
    plt.ylabel('Running time of A*')
    plt.title('Running time comparison of A* and Adaptive A*')
    plt.show()
    # myQueue.print()
'''