import json
import pickle
import random
from typing import List, Optional

from maze import Maze, Cell, Agent, MazeVisualizer
from priority_queue import PriorityQueue


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def load_mazes():
        with open("mazes", "rb") as mazes_file:
            return pickle.load(mazes_file)

    @staticmethod
    def load_random_maze():
        with open("mazes", "rb") as mazes_file:
            mazes = pickle.load(mazes_file)
        return random.choice(mazes)

    @staticmethod
    def compute_heuristic(maze, target: Cell):
        rows, cols = (maze.n_rows, maze.n_cols)
        goal = target
        heuristic_arr = [[(abs(goal.col - i) + abs(goal.row - j)) for i in range(cols)] for j in range(rows)]
        return heuristic_arr

    @staticmethod
    def print_path(path, mazevis, algo_name, start: Cell, end: Cell):
        count = 0
        for cell in path[:-1]:
            if cell.get_co_ordinates() not in [start.get_co_ordinates(), end.get_co_ordinates()]:
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


class AStarWithAgent:

    def __init__(self, maze=Optional[Maze], n_rows=None, n_cols=None):
        if not maze:
            self.maze = Maze(n_rows, n_cols)
        else:
            self.maze = maze
        self.agent = Agent(self.maze.n_rows, self.maze.n_cols, self.maze.start, self.maze.end, self.maze)
        self.pop_counter = 0

    def compute_path(self, queue, heuristic):
        count = 1
        while 0 != len(queue):
            c = queue.pop()
            self.pop_counter += 1
            c.cell.visited = True
            valid_neighbors = self.agent.agent_maze.get_unblocked_unvisited_neighbors(c.cell)
            if c.cell.get_co_ordinates() == self.agent.agent_maze.end.get_co_ordinates():
                self.agent.agent_maze.reset_visited()
                return Utils.get_traversal_path(c.cell)
            for item in valid_neighbors:
                queue.push(count, heuristic[item.row][item.col], item, c.cell)
            count = count + 1
        return None

    def reset_agent(self):
        self.agent = Agent(self.maze.n_rows, self.maze.n_cols, self.maze.start, self.maze.end, self.maze)

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
                return None, None
            traversed_path.extend(self.agent.traverse_path(path))
            if self.agent.current_loc.get_co_ordinates() == self.maze.end.get_co_ordinates():
                re_compute = False
        Utils.print_path(traversed_path, maze_vis, "A*", self.maze.start, self.maze.end)
        print("\nTotal popped nodes are: ", self.pop_counter)
        maze_vis.show_maze()
        return self.pop_counter, len(traversed_path)


class AdaptiveAStarWithAgent:

    def __init__(self, maze=Optional[Maze], n_rows=None, n_cols=None):
        if not maze:
            self.maze = Maze(n_rows, n_cols)
        else:
            self.maze = maze
        self.agent = Agent(self.maze.n_rows, self.maze.n_cols, self.maze.start, self.maze.end, self.maze)
        self.heuristics = Utils.compute_heuristic(self.maze, self.maze.end)
        self.pop_counter = 0

    def update_heuristics(self, traversal_path: List[Cell]):
        count = 0
        traversal_path.reverse()
        print("\n")
        for path_cell in traversal_path[1:]:
            for i in path_cell.children:
                self.heuristics[i.row][i.col] = count
                print("New heuristic for ({}, {}) is {}".format(i.row, i.col, count))
            count += 1
        print("Adaptive A star moves", count, "\n")

    def compute_path(self, queue):
        moves = 1
        while 0 != len(queue):
            c = queue.pop()
            self.pop_counter += 1
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
                return None, None
            traversed_path.extend(self.agent.traverse_path(path))
            if self.agent.current_loc.get_co_ordinates() == self.maze.end.get_co_ordinates():
                re_compute = False

        print("Adaptive * path exists\n")
        self.update_heuristics(traversed_path)
        Utils.print_path(traversed_path, maze_vis, "Adaptive A*", self.maze.start, self.maze.end)
        maze_vis.show_maze()
        return self.pop_counter, len(traversed_path)

    def reset_agent(self):
        self.agent = Agent(self.maze.n_rows, self.maze.n_cols, self.maze.start, self.maze.end, self.maze)

    def demo_adaptive_a_star(self, n_times=10):
        self.maze.start = self.maze.get_random_cell()
        for _ in range(n_times):
            if self.maze.start == self.maze.end:
                continue
            self.reset_agent()
            self.run_adaptive_a_star()


class ReverseAStar:

    def __init__(self, maze=Optional[Maze], n_rows=None, n_cols=None):
        if not maze:
            self.maze = Maze(n_rows, n_cols)
        else:
            self.maze = maze
        self.agent = Agent(self.maze.n_rows, self.maze.n_cols, self.maze.start, self.maze.end, self.maze)
        self.pop_counter = 0

    def compute_path(self, queue, heuristic):
        count = 1
        while 0 != len(queue):
            c = queue.pop()
            self.pop_counter += 1
            c.cell.visited = True
            valid_neighbors = self.agent.agent_maze.get_unblocked_unvisited_neighbors(c.cell)
            if c.cell.get_co_ordinates() == self.agent.current_loc.get_co_ordinates():
                self.agent.agent_maze.reset_visited()
                path = Utils.get_traversal_path(c.cell, reverse_a_star=True)
                path.append(self.agent.agent_maze.end)
                return path
            for item in valid_neighbors:
                queue.push(count, heuristic[item.row][item.col], item, c.cell)
            count = count + 1
        return None

    def run_reverse_a_star(self):
        maze_vis = MazeVisualizer(self.maze)
        re_compute = True
        print("Agent's destination is - row: {}, col: {}".format(self.maze.end.row, self.maze.end.col))
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
                return None, None
            traversed_path.extend(self.agent.traverse_path(path))
            if self.agent.current_loc.get_co_ordinates() == self.maze.end.get_co_ordinates():
                re_compute = False
        Utils.print_path(traversed_path, maze_vis, "Reverse A*", self.maze.start, self.maze.end)
        print("\nTotal popped nodes are: ", self.pop_counter)
        maze_vis.show_maze()
        return self.pop_counter, len(traversed_path)


if __name__ == '__main__':
    def_mazes = Utils.load_mazes()

    # A star algorithm
    my_a_star = AStarWithAgent(def_mazes[0])
    my_a_star.run_a_star_with_agent()

    # Reverse A star algorithm
    my_reverse = ReverseAStar(def_mazes[0])
    my_reverse.run_reverse_a_star()

    # Adaptive A star algorithm
    my_agent_a_star = AdaptiveAStarWithAgent(def_mazes[0])
    my_agent_a_star.run_adaptive_a_star()


def aws_function():
    differences = list()
    n_times = 500
    adaptive = AdaptiveAStarWithAgent(maze=def_mazes[0])
    a_star = AStarWithAgent(maze=def_mazes[0])
    all_a_star_moves = []
    all_adaptive_moves = []
    for _ in range(n_times):
        new_start = a_star.maze.get_random_cell()
        a_star.maze.start = new_start

        a_star.reset_agent()
        a_star_pops, a_star_moves = a_star.run_a_star_with_agent()
        all_a_star_moves.append({"start": a_star.maze.start.get_co_ordinates(),
                                 "end": a_star.maze.end.get_co_ordinates(),
                                 "moves": a_star_moves,
                                 })

        adaptive.maze.start = adaptive.maze.maze[new_start.row][new_start.col]
        adaptive.reset_agent()
        adaptive_pops, adaptive_moves = adaptive.run_adaptive_a_star()
        all_adaptive_moves.append({"start": a_star.maze.start.get_co_ordinates(),
                                   "end": a_star.maze.end.get_co_ordinates(),
                                   "moves": adaptive_moves,
                                   })
        if adaptive_pops is not None and a_star_pops is not None:
            differences.append({"start": a_star.maze.start.get_co_ordinates(),
                                "end": a_star.maze.end.get_co_ordinates(),
                                "difference": adaptive_pops - a_star_pops,
                                })

    moves_obj = {
        "adaptive_moves": all_adaptive_moves,
        "a_star_moves": all_a_star_moves
    }
    with open("differences_adaptive.json", "w") as diff_file:
        json.dump(differences, diff_file)

    with open("moves.json", "w") as moves_file:
        json.dump(moves_obj, moves_file)

    print("The differences array is: ", differences)
    print("Average difference is: ", (sum(differences) / len(differences)))
