from typing import Optional

from maze import Cell


class Element:
    def __init__(self, g_n, h_n, cell: Cell, parent: Cell):
        self.g_val = g_n
        self.h_val = h_n
        self.f_val = g_n + h_n
        self.cell = cell
        self.cell.parent = parent

    def get_hval(self):
        return self.h_val


class PriorityQueue:
    def __init__(self):
        self.heap = []

    def get_best_node_from_open_list(self):
        # An alias for pop for better readability
        return self.pop()

    def push(self, g_n, h_n, cell: Cell, parent: Optional[Cell]):
        self.heap.append(Element(g_n, h_n, cell, parent))

    def pop(self):
        min_dist = 0
        for i in range(len(self.heap)):
            if self.heap[i].f_val == self.heap[min_dist].f_val:
                if self.heap[i].g_val > self.heap[min_dist].g_val:
                    min_dist = i
            elif self.heap[i].f_val < self.heap[min_dist].f_val:
                min_dist = i
        item = self.heap[min_dist]
        del self.heap[min_dist]
        return item

    def __len__(self):
        return len(self.heap)

    def print(self):
        for i in range(len(self.heap)):
            print(self.heap[i].h_val)
