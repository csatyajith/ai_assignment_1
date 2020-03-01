from maze import Maze, Cell, MazeVisualizer
from priority_queue import PriorityQueue


class AStar:

    def __init__(self, n_rows, n_cols):
        self.maze = Maze(n_rows, n_cols)

    @staticmethod
    def compute_heuristic(maze: Maze):
        rows, cols = (maze.n_rows, maze.n_cols)
        goal = maze.end
        heuristic_arr = [[(abs(goal.col - i) + abs(goal.row - j)) for i in range(cols)] for j in range(rows)]
        return heuristic_arr

    @staticmethod
    def compute_path(queue, maze: Maze, heuristic):
        count = 1
        while 0 != len(queue):
            c = queue.pop()
            c.cell.visited = True
            valid_neighbors = maze.get_unblocked_unvisited_neighbors(c.cell)
            if c.cell == maze.end:
                return c.cell
            for item in valid_neighbors:
                queue.push(count, heuristic[item.row][item.col], item, c.cell)
            count = count + 1
        return None

    def print_path(self, path: Cell, mazevis: MazeVisualizer):
        steps = 1
        while path != self.maze.start:
            steps += 1
            mazevis.fill_cell(path.row, path.col)
            # print('Row', path.row, 'Col', path.col)
            path = path.parent
        print("A star steps", steps)

    def run_a_star(self):
        # print on console
        for r in self.maze.maze:
            print([0 if cell.blocked else 1 for cell in r])

        # plot on matplotlib
        maze_vis = MazeVisualizer(self.maze)
        # maze_vis.show_maze()

        manhattan_heuristic = self.compute_heuristic(self.maze)
        start_row = self.maze.start.row
        start_col = self.maze.start.col
        my_queue = PriorityQueue()
        my_queue.push(0, manhattan_heuristic[start_row][start_col], self.maze.get_cell(start_row, start_col), None)
        target = self.compute_path(my_queue, self.maze, manhattan_heuristic)
        if target is not None:
            target = target.parent
            print("Path exists")
            self.print_path(target, maze_vis)
        else:
            print("Path does not exists")
        maze_vis.show_maze()
        # my_queue.print()


class AdaptiveAStar:

    def __init__(self, n_rows, n_cols):
        self.maze = Maze(n_rows, n_cols)

    def update_path(self, path: Cell, mazevis: MazeVisualizer, new_heuristics, count):
        while path != self.maze.start:
            for i in path.childrenren:
                new_heuristics[i.row][i.col] = count
            mazevis.fill_cell(path.row, path.col)
            # print('Row', path.row, 'Col', path.col)
            count = count + 1
            path = path.parent
        new_heuristics[path.row][path.col] = count  # for start cell
        print("Adaptive A star moves", count)

    @staticmethod
    def compute_heuristic(maze: Maze):
        rows, cols = (maze.n_rows, maze.n_cols)
        goal = maze.end
        heuristic_arr = [[(abs(goal.col - i) + abs(goal.row - j)) for i in range(cols)] for j in range(rows)]
        return heuristic_arr

    @staticmethod
    def compute_path(queue, maze: Maze, heuristic):
        moves = 1
        while 0 != len(queue):
            c = queue.pop()
            if c.cell.parent is not None:
                c.cell.parent.children.append(c.cell)
            c.cell.visited = True
            valid_neighbors = maze.get_unblocked_unvisited_neighbors(c.cell)
            if c.cell == maze.end:
                return c.cell
            for item in valid_neighbors:
                queue.push(moves, heuristic[item.row][item.col], item, c.cell)
            moves = moves + 1
        return None

    def print_path(self, path: Cell, mazevis: MazeVisualizer):
        if path != self.maze.start:
            self.print_path(path.parent, mazevis)
            print('Row', path.row, 'Col', path.col)
            mazevis.fill_cell(path.row, path.col)

    def run_adaptive_a_star(self):

        # plot on matplotlib
        maze_vis = MazeVisualizer(self.maze)
        # maze_vis.show_maze()

        new_heuristics = self.compute_heuristic(self.maze)
        start_row = self.maze.start.row
        start_col = self.maze.start.col
        my_queue = PriorityQueue()
        my_queue.push(0, new_heuristics[start_row][start_col], self.maze.get_cell(start_row, start_col), None)
        target = self.compute_path(my_queue, self.maze, new_heuristics)
        if target is not None:
            target = target.parent
            print("Adaptive * path exists")
            count = 1
            self.update_path(target, maze_vis, new_heuristics, count)
        else:
            print("Path does not exists")

    def demo_adaptive_a_star(self, n_times):
        for _ in range(n_times):
            self.maze.start = self.maze.get_random_cell()
            if self.maze.start == self.maze.end:
                continue
            self.maze.reset_visited()
            self.run_adaptive_a_star()
            self.maze.reset_visited()
            self.run_adaptive_a_star()
