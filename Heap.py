from collections import deque

class Node(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Heap(object):
    def __init__(self):
        self.pos = 0
        self.heap = deque()

    def __str__(self):
        pos = self.pos
        depth = 0
        s = ''
        for i, v in enumerate(self.heap):
            self.set_pos(i)
            if self.depth() != depth:
                depth = self.depth()
                s += '\n'
            s += '%s:%s\t' % (v.name, v.value)
        self.pos = pos
        return s

    def depth(self):
        pos = self.pos
        parent = pos
        i = 0
        while parent > 0:
            parent = self.parent()
            self.set_pos(parent)
            i += 1
        self.pos = pos
        return i


    def left(self):
        return self.pos * 2 + 1

    def right(self):
        return self.pos * 2 + 2

    def parent(self):
        return (self.pos - 1) / 2

    def is_root(self):
        return self.pos == 0

    def is_leaf(self):
        return self.right() >= len(self.heap) and self.left() >= len(self.heap)

    def one_child(self):
        return self.right() == len(self.heap)

    def set_pos(self, i):
        self.pos = i

    def get_current(self):
        return self.heap[self.pos]

    def get_left(self):
        i = self.left()
        return self.heap[i]

    def get_right(self):
        i = self.right()
        return self.heap[i]

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def down_heapify(self, pos):
        self.set_pos(pos)
        self._down_heapify()

    def _down_heapify(self):
        if self.is_leaf(): return

        # only need to check one child
        if self.one_child():
            # parent > left child, need to swap
            if self.get_current().value > self.get_left().value:
                self.swap(self.pos, self.left())
            return

        # two children
        # if both children are greater than parent, heap property is maintained for current
        if min(self.get_left().value, self.get_right().value) >= self.get_current().value:
            return

        # heap property not maintained
        # swap minimum of children
        if self.get_right().value < self.get_left().value:
            self.swap(self.pos, self.right())
            self.set_pos(self.right())
        else:
            self.swap(self.pos, self.left())
            self.set_pos(self.left())

        self._down_heapify()

    def build_heap(self, i):
        self.set_pos(len(self.heap)-1)
        self._build_heap(i)

    def _build_heap(self, i):
        if self.pos == i-1: return

        if self.is_leaf():
            self.set_pos(self.pos - 1)
            self._build_heap(i)
            return

        pos = self.pos
        self._down_heapify()
        self.set_pos(pos - 1)
        self._build_heap(i)

    def up_heapify(self, pos):
        self.set_pos(pos)
        self._up_heapify()

    def _up_heapify(self):
        parent = self.parent()
        if parent < 0: return

        if self.heap[parent].value > self.get_current().value:
            self.swap(parent, self.pos)
            self.set_pos(parent)
            self._up_heapify()
            return

    def insert(self, name, value):
        n = Node(name, value)
        self.heap.append(n)
        self.up_heapify(len(self.heap)-1)


    def in_heap(self, name):
        for i, node in enumerate(self.heap):
            if node.name == name:
                return i

        return -1

    def get(self, index):
        return self.heap[index]

    def remove_min(self):
        n = self.heap.popleft()
        self.down_heapify(0)
        return n

    def to_dict(self):
        d = {}
        for node in self.heap:
            d[node.name] = node.value
        return d

if __name__ == "__main__":
    # quick, basic test
    heap = Heap()
    heap.insert('a', 0)
    heap.insert('b', 8)
    heap.insert('c', 2)
    heap.insert('d', 4)
    heap.build_heap(0)
    print heap
