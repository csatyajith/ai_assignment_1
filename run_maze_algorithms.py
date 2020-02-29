from typing import List

from maze import MazeVisualizer, Maze, Cell, Agent
from priority_queue import PriorityQueue


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def compute_heuristic(maze, target: Cell):
        rows, cols = (maze.n_rows, maze.n_cols)
        goal = target
        heuristic_arr = [[(abs(goal.col - i) + abs(goal.row - j)) for i in range(cols)] for j in range(rows)]
        return heuristic_arr

    @staticmethod
    def print_path(path, mazevis, algo_name):
        count = 0
        for cell in path[:-1]:
            mazevis.fill_cell(cell.row, cell.col)
            count += 1
        print("Total {} moves are: {} \n".format(algo_name, count))

    @staticmethod
    def get_traversal_path(target: Cell, reverse_a_star=False):
        path = list()
        path_cell = target
        while path_cell.parent is not None:
            path.append(path_cell)
            path_cell = path_cell.parent
        if not reverse_a_star:
            path.reverse()
        return path


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


class AStarWithAgent:

    def __init__(self, n_rows, n_cols):
        self.maze = Maze(n_rows, n_cols)
        self.agent = Agent(n_rows, n_cols, self.maze.start, self.maze.end, self.maze)

    def compute_path(self, queue, heuristic):
        count = 1
        while 0 != len(queue):
            c = queue.pop()
            c.cell.visited = True
            valid_neighbors = self.agent.agent_maze.get_unblocked_unvisited_neighbors(c.cell)
            if c.cell.get_co_ordinates() == self.agent.agent_maze.end.get_co_ordinates():
                self.agent.agent_maze.reset_visited()
                return Utils.get_traversal_path(c.cell)
            for item in valid_neighbors:
                queue.push(count, heuristic[item.row][item.col], item, c.cell)
            count = count + 1
        return None

    def run_a_star_with_agent(self):
        maze_vis = MazeVisualizer(self.maze)
        re_compute = True
        traversed_path = list()
        manhattan_heuristic = Utils.compute_heuristic(self.maze, self.maze.end)
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
        Utils.print_path(traversed_path, maze_vis, "A*")
        maze_vis.show_maze()


class AdaptiveAStarWithAgent:

    def __init__(self, n_rows, n_cols):
        self.maze = Maze(n_rows, n_cols)
        self.agent = Agent(n_rows, n_cols, self.maze.start, self.maze.end, self.maze)
        self.heuristics = Utils.compute_heuristic(self.maze, self.maze.end)

    def update_heuristics(self, traversal_path: List[Cell], mazevis: MazeVisualizer):
        count = 0
        traversal_path.reverse()
        print("\n")
        for path_cell in traversal_path[1:]:
            for i in path_cell.children:
                self.heuristics[i.row][i.col] = count
                print("New heuristic for ({}, {}) is {}".format(i.row, i.col, count))
            mazevis.fill_cell(path_cell.row, path_cell.col)
            count += 1
        print("Adaptive A star moves", count, "\n")

    def compute_path(self, queue):
        moves = 1
        while 0 != len(queue):
            c = queue.pop()
            if c.cell.parent is not None:
                if c.cell not in c.cell.parent.children:
                    c.cell.parent.children.append(c.cell)
            c.cell.visited = True
            valid_neighbors = self.agent.agent_maze.get_unblocked_unvisited_neighbors(c.cell)
            if c.cell.get_co_ordinates() == self.agent.agent_maze.end.get_co_ordinates():
                self.agent.agent_maze.reset_visited()
                return Utils.get_traversal_path(c.cell)
            for item in valid_neighbors:
                queue.push(moves, self.heuristics[item.row][item.col], item, c.cell)
            moves = moves + 1
        return None

    def run_adaptive_a_star(self):
        maze_vis = MazeVisualizer(self.maze)
        traversed_path = [self.agent.current_loc]
        re_compute = True
        print("Agent's destination is - row: {}, col: {}".format(self.maze.end.row, self.maze.end.col))
        while re_compute:
            start_row = self.agent.current_loc.row
            start_col = self.agent.current_loc.col
            my_queue = PriorityQueue()
            my_queue.push(0, self.heuristics[start_row][start_col],
                          self.agent.agent_maze.get_cell(start_row, start_col),
                          None)
            path = self.compute_path(my_queue)
            if path is None:
                print("Path does not exists\n")
                return
            traversed_path.extend(self.agent.traverse_path(path))
            if self.agent.current_loc.get_co_ordinates() == self.maze.end.get_co_ordinates():
                re_compute = False

        print("Adaptive * path exists\n")
        self.update_heuristics(traversed_path, maze_vis)
        Utils.print_path(traversed_path, maze_vis, "Adaptive A*")
        # maze_vis.show_maze()

    def demo_adaptive_a_star(self, n_times=10):
        self.maze.start = self.maze.get_random_cell()
        for _ in range(n_times):
            if self.maze.start == self.maze.end:
                continue
            self.agent = Agent(self.maze.n_rows, self.maze.n_cols, self.maze.start, self.maze.end, self.maze)
            self.run_adaptive_a_star()


class ReverseAStar:

    def __init__(self, n_rows, n_cols):
        self.maze = Maze(n_rows, n_cols)
        self.agent = Agent(n_rows, n_cols, self.maze.start, self.maze.end, self.maze)

    def compute_path(self, queue, heuristic):
        count = 1
        while 0 != len(queue):
            c = queue.pop()
            c.cell.visited = True
            valid_neighbors = self.agent.agent_maze.get_unblocked_unvisited_neighbors(c.cell)
            if c.cell.get_co_ordinates() == self.agent.current_loc.get_co_ordinates():
                self.agent.agent_maze.reset_visited()
                return Utils.get_traversal_path(c.cell, reverse_a_star=True)
            for item in valid_neighbors:
                queue.push(count, heuristic[item.row][item.col], item, c.cell)
            count = count + 1
        return None

    def run_reverse_a_star(self):
        maze_vis = MazeVisualizer(self.maze)
        re_compute = True
        traversed_path = list()
        while re_compute:
            manhattan_heuristic = Utils.compute_heuristic(self.maze, self.agent.current_loc)
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
        Utils.print_path(traversed_path, maze_vis, "Reverse A*")
        maze_vis.show_maze()


if __name__ == '__main__':
    # my_a_star = AStar(10, 10)
    # my_a_star.run_a_star()
    # my_reverse = ReverseAStar(10, 10)
    # my_reverse.reverse_a_star()
    # my_agent_a_star = AStarWithAgent(10, 10)
    # my_agent_a_star.run_a_star_with_agent()
    adaptive = AStarWithAgent(50, 50)
    adaptive.run_a_star_with_agent()
