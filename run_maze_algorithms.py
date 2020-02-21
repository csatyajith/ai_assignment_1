import priority_queue as pq
from maze import MazeVisualizer, Maze, Cell


class AStar:
    @staticmethod
    def compute_heuristic(maze: Maze):
        rows, cols = (maze.n_rows, maze.n_cols)
        goal = maze.end
        heuristic_arr = [[(abs(goal.col - i) + abs(goal.row - j)) for i in range(cols)] for j in range(rows)]
        print(heuristic_arr)
        return heuristic_arr

    @staticmethod
    def compute_path(queue, maze: Maze, heuristic):
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

    def print_path(self, maze_1, path: Cell, mazevis: MazeVisualizer):
        if path != maze_1.start:
            self.print_path(maze_1, path.parent, mazevis)
            # print('Row', path.row, 'Col', path.col)
            mazevis.fill_cell(path.row, path.col)

    def run_a_star(self, n_rows, n_cols):
        n_rows = 10  # 10 is better for visualization Change to 51 for project
        n_cols = 10
        maze_1 = Maze(n_rows, n_cols)
        maze_1.reset_visited()
        # print on console
        for r in maze_1.maze:
            print([0 if cell.blocked else 1 for cell in r])

        # plot on matplotlib
        maze_vis = MazeVisualizer(maze_1)
        # maze_vis.show_maze()

        manhattan_heuristic = self.compute_heuristic(maze_1)
        start_row = maze_1.start.row
        start_col = maze_1.start.col
        my_queue = pq.PriorityQueue()
        my_queue.push(0, manhattan_heuristic[start_row][start_col], maze_1.get_cell(start_row, start_col), None)
        target = self.computePath(my_queue, maze_1, manhattan_heuristic)
        if target is not None:
            target = target.parent
            print("Path exists")
            self.print_path(maze_1, target, maze_vis)
        else:
            print("Path does not exists")
        maze_vis.show_maze()
        # my_queue.print()


class ReverseAStar:

    def compute_heuristic(self, maze):
        raise NotImplementedError

    @staticmethod
    def compute_path(queue, maze, heuristic):
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

    def print_path(self, maze, target, maze_vis):
        raise NotImplementedError

    def reverse_a_star(self):
        maze_1 = Maze(10, 10)
        maze_1.reset_visited()

        maze_vis = MazeVisualizer(maze_1)

        manhattan_heuristic = self.compute_heuristic(maze_1)
        start_row = maze_1.end.row
        start_col = maze_1.end.col
        my_queue = pq.PriorityQueue()
        my_queue.push(0, manhattan_heuristic[start_row][start_col], maze_1.get_cell(start_row, start_col), None)
        target = self.compute_path(my_queue, maze_1, manhattan_heuristic)
        if target is not None:
            target = target.parent
            print("Path exists")
            self.print_path(maze_1, target, maze_vis)
        else:
            print("Path does not exists")
        maze_vis.show_maze()


if __name__ == '__main__':
    my_a_star = AStar()
    my_a_star.run_a_star(10, 10)
