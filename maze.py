import random

import matplotlib.pyplot as plt
import numpy as np


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.blocked = False
        self.visited = False
        self.parent = None


class Maze:

    def __init__(self, n_rows, n_cols, create_blockers=True, p_block=0.3):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.p_block = p_block
        self.maze = [[Cell(r, c) for c in range(n_cols)] for r in range(n_rows)]
        if create_blockers:
            self._create_blockers()
        self.start = self.get_random_cell()
        self.end = self.get_random_cell()

    def _create_blockers(self):
        traversal_stack = []
        while not self.all_cells_visited():
            if len(traversal_stack) == 0:
                traversal_stack.append(self.get_random_unvisited_cell())
                self.maze[traversal_stack[-1].row][traversal_stack[-1].col].visited = True
            valid_neighbors = self.get_neighbors(traversal_stack[-1])

            if len(valid_neighbors) == 0:
                traversal_stack.pop()
                continue

            next_step = random.choice(valid_neighbors)
            self.maze[next_step.row][next_step.col].visited = True
            if np.random.random() <= self.p_block:
                self.maze[next_step.row][next_step.col].blocked = True
            else:
                traversal_stack.append(next_step)
        self.reset_visited()

    def get_neighbors(self, cell: Cell):
        neighbors = list()
        accepted_rows = [-1, 1]
        accepted_cols = [-1, 1]
        if cell.row == self.n_rows - 1:
            accepted_rows = [-1]
        elif cell.row == 0:
            accepted_rows = [1]
        if cell.col == self.n_cols - 1:
            accepted_cols = [-1]
        elif cell.col == 0:
            accepted_cols = [1]

        for i in accepted_rows:
            n1 = self.maze[cell.row + i][cell.col]
            if not n1.blocked and not n1.visited:
                neighbors.append(n1)

        for j in accepted_cols:
            n2 = self.maze[cell.row][cell.col + j]
            if not n2.blocked and not n2.visited:
                neighbors.append(n2)

        return neighbors

    def get_random_unvisited_cell(self):
        unvisited = list()
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if not self.maze[i][j].visited:
                    unvisited.append(self.maze[i][j])
        return random.choice(unvisited)

    def all_cells_visited(self):
        for r in self.maze:
            for c in r:
                if not c.visited:
                    return False
        return True

    def get_random_cell(self):
        while True:
            x = np.random.randint(0, self.n_rows - 1)
            y = np.random.randint(0, self.n_cols - 1)
            if not self.maze[x][y].blocked:
                return self.maze[x][y]

    def get_cell(self, i, j):
        return self.maze[i][j]

    def reset_visited(self):
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                self.maze[r][c].visited = False


class Agent:
    def __init__(self, n_rows, n_cols, start_loc, target_loc):
        self.agent_maze = Maze(n_rows, n_cols, create_blockers=False)
        self.agent_maze.start = start_loc
        self.current_loc = start_loc
        self.agent_maze.end = target_loc


class MazeVisualizer:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.ax = None
        self.configure_plot()
        self.fill_maze()

    @staticmethod
    def show_maze():
        plt.show()

    def configure_plot(self):
        fig = plt.figure(figsize=(7, 7 * self.maze.n_rows / self.maze.n_cols))
        self.ax = plt.axes()
        self.ax.set_aspect("equal")

        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)

        return fig

    def fill_maze(self):
        for row in self.maze.maze:
            for cell in row:
                i = cell.row
                j = cell.col
                if i == 0:
                    self.ax.plot([j, (j + 1)], [i, i], color="k")
                if j == self.maze.n_cols - 1:
                    self.ax.plot([(j + 1), (j + 1)], [i, (i + 1)], color="k")
                if i == self.maze.n_rows - 1:
                    self.ax.plot([(j + 1), j], [(i + 1), (i + 1)], color="k")
                if j == 0:
                    self.ax.plot([j, j], [(i + 1), i], color="k")
                if cell.blocked:
                    i = self.maze.n_cols - 1 - i
                    self.ax.fill_between([j, j + 1], i, i + 1, color="k")
                elif cell == self.maze.start:
                    i = self.maze.n_cols - 1 - i
                    self.ax.fill_between([j, j + 1], i, i + 1, color="r")
                elif cell == self.maze.end:
                    i = self.maze.n_cols - 1 - i
                    self.ax.fill_between([j, j + 1], i, i + 1, color="c")

    def fill_cell(self, i, j):
        i = self.maze.n_cols - 1 - i
        self.ax.fill_between([j, j + 1], i, i + 1, color='yellow')
