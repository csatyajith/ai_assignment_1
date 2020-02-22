from maze import MazeVisualizer, Maze, Cell, Agent
from priority_queue import PriorityQueue


class AStar:

    def __init__(self, n_rows, n_cols):
        self.maze = Maze(n_rows, n_cols)

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
            valid_neighbors = maze.get_unblocked_unvisited_neighbors(c.cell)
            if c.cell == maze.end:
                return c.cell
            for item in valid_neighbors:
                queue.push(count, heuristic[item.row][item.col], item, c.cell)
            count = count + 1
        return None

    def print_path(self, path: Cell, mazevis: MazeVisualizer):
        if path != self.maze.start:
            self.print_path(path.parent, mazevis)
            # print('Row', path.row, 'Col', path.col)
            mazevis.fill_cell(path.row, path.col)

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


class AStarWithAgent:

    def __init__(self, n_rows, n_cols):
        self.maze = Maze(n_rows, n_cols)
        self.agent = Agent(n_rows, n_cols, self.maze.start, self.maze.end, self.maze)

    def compute_heuristic(self, maze):
        rows, cols = (maze.n_rows, maze.n_cols)
        goal = self.maze.end
        heuristic_arr = [[(abs(goal.col - i) + abs(goal.row - j)) for i in range(cols)] for j in range(rows)]
        return heuristic_arr

    @staticmethod
    def get_path(target: Cell):
        path = list()
        path_cell = target
        while path_cell.parent is not None:
            path.append(path_cell)
            path_cell = path_cell.parent
        path.append(path_cell)
        path.reverse()
        return path

    def compute_path(self, queue, heuristic):
        count = 1
        while 0 != len(queue):
            c = queue.pop()
            c.cell.visited = True
            valid_neighbors = self.agent.agent_maze.get_unblocked_unvisited_neighbors(c.cell)
            if c.cell.get_co_ordinates() == self.agent.agent_maze.end.get_co_ordinates():
                self.agent.agent_maze.reset_visited()
                return self.get_path(c.cell)
            for item in valid_neighbors:
                queue.push(count, heuristic[item.row][item.col], item, c.cell)
            count = count + 1
        return None

    def print_path(self, path, mazevis):
        for i, cell in enumerate(path):
            if cell.get_co_ordinates() not in [self.agent.agent_maze.start.get_co_ordinates(),
                                               self.agent.agent_maze.end.get_co_ordinates()]:
                mazevis.plot(cell.row, cell.col, label=str(i))

    def run_a_star_with_agent(self):
        maze_vis = MazeVisualizer(self.maze)
        re_compute = True
        traversed_path = list()
        manhattan_heuristic = self.compute_heuristic(self.maze)
        while re_compute:
            start_row = self.agent.current_loc.row
            start_col = self.agent.current_loc.col
            my_queue = PriorityQueue()
            my_queue.push(0, manhattan_heuristic[start_row][start_col],
                          self.agent.agent_maze.get_cell(start_row, start_col), None)
            path = self.compute_path(my_queue, manhattan_heuristic)
            if path is None:
                print("Path does not exist")
                return
            traversed_path.extend(self.agent.traverse_path(path))
            if self.agent.current_loc.get_co_ordinates() == self.maze.end.get_co_ordinates():
                re_compute = False
        self.print_path(traversed_path, maze_vis)
        maze_vis.show_maze()


class ReverseAStar:

    def __init__(self, n_rows, n_cols):
        self.maze = Maze(n_rows, n_cols)
        self.agent = Agent(n_rows, n_cols, self.maze.start, self.maze.end, self.maze)

    def compute_heuristic(self, maze):
        rows, cols = (maze.n_rows, maze.n_cols)
        goal = self.agent.current_loc
        heuristic_arr = [[(abs(goal.col - i) + abs(goal.row - j)) for i in range(cols)] for j in range(rows)]
        return heuristic_arr

    def get_path(self, target: Cell):
        path = list()
        path_cell = target
        while path_cell.parent is not None:
            path.append(path_cell)
            path_cell = path_cell.parent
        path.append(path_cell)
        return path

    def compute_path(self, queue, heuristic):
        count = 1
        while 0 != len(queue):
            c = queue.pop()
            c.cell.visited = True
            valid_neighbors = self.agent.agent_maze.get_unblocked_unvisited_neighbors(c.cell)
            if c.cell.get_co_ordinates() == self.agent.current_loc.get_co_ordinates():
                self.agent.agent_maze.reset_visited()
                return self.get_path(c.cell)
            for item in valid_neighbors:
                queue.push(count, heuristic[item.row][item.col], item, c.cell)
            count = count + 1
        return None

    def print_path(self, path, mazevis):
        for cell in path:
            if cell.get_co_ordinates() not in [self.agent.agent_maze.start.get_co_ordinates(),
                                               self.agent.agent_maze.end.get_co_ordinates()]:
                mazevis.fill_cell(cell.row, cell.col)

    def reverse_a_star(self):
        maze_vis = MazeVisualizer(self.maze)
        re_compute = True
        traversed_path = list()
        while re_compute:
            manhattan_heuristic = self.compute_heuristic(self.maze)
            start_row = self.maze.end.row
            start_col = self.maze.end.col
            my_queue = PriorityQueue()
            my_queue.push(0, manhattan_heuristic[start_row][start_col],
                          self.agent.agent_maze.get_cell(start_row, start_col), None)
            path = self.compute_path(my_queue, manhattan_heuristic)
            if path is None:
                print("Path does not exist")
                return
            traversed_path.extend(self.agent.traverse_path(path))
            if self.agent.current_loc.get_co_ordinates() == self.maze.end.get_co_ordinates():
                re_compute = False
        self.print_path(traversed_path, maze_vis)
        maze_vis.show_maze()


if __name__ == '__main__':
    # my_a_star = AStar(10, 10)
    # my_a_star.run_a_star()
    # my_reverse = ReverseAStar(10, 10)
    # my_reverse.reverse_a_star()
    my_agent_a_star = AStarWithAgent(10, 10)
    my_agent_a_star.run_a_star_with_agent()
