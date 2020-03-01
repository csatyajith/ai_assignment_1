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
        self.heap_co_ords = set()
        self.closed = set()

    def get_best_node_from_open_list(self):
        # An alias for pop for better readability
        return self.pop()

    def push(self, g_n, h_n, cell: Cell, parent: Optional[Cell]):
        co_ordinates = cell.get_co_ordinates()
        if (co_ordinates not in self.closed) and (co_ordinates not in self.heap_co_ords):
            self.heap.append(Element(g_n, h_n, cell, parent))
            self.heap_co_ords.add(cell.get_co_ordinates())
            self.heapsort()

    def swap(self, i, j):
        obj1 = self.heap[i]
        obj2 = self.heap[j]
        temp_g = obj1.g_val
        temp_h = obj1.h_val
        temp_f = obj1.f_val
        temp_cell = obj1.cell
        temp_parent = obj1.cell.parent

        obj1.g_val = obj2.g_val
        obj1.h_val = obj2.h_val
        obj1.f_val = obj2.f_val
        obj1.cell = obj2.cell
        obj1.cell.parent = obj2.cell.parent

        obj2.g_val = temp_g
        obj2.h_val = temp_h
        obj2.f_val = temp_f
        obj2.cell = temp_cell
        obj2.cell.parent = temp_parent

    def heapify(self, index):
        left = 2 * index + 1
        right = 2 * index + 2
        child = [left, right]
        min_index = index
        n = self.__len__()
        for i in child:
            if i < n and self.heap[min_index].f_val == self.heap[i].f_val:
                if self.heap[min_index].g_val < self.heap[i].g_val:
                    min_index = i
            elif i < n and self.heap[min_index].f_val > self.heap[i].f_val:
                min_index = i
        # print('Minimun index ', index)
        self.print()
        if min_index is not index:
            self.swap(min_index, index)
            # print('call recur', min_index)
            self.heapify(min_index)

    def heapsort(self):
        for i in range(int(len(self.heap) / 2 - 1), -1, -1):
            self.heapify(i)
        # print("Heap length: ", len(self.heap))

    def pop(self):
        # print('call heapsort')
        min_ele = self.heap[0]
        # print('final min ele', self.heap[0].f_val)
        self.closed.add(self.heap[0].cell.get_co_ordinates())
        self.heap_co_ords.remove(min_ele.cell.get_co_ordinates())
        del self.heap[0]
        return min_ele

    def __len__(self):
        return len(self.heap)

    def print(self):
        pass
        # for i in range(len(self.heap)):
        # print(self.heap[i].f_val)
