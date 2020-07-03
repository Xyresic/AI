#! /usr/bin/python3

import sys
from time import time

class Node:
    def __init__(self):
        self.left = self
        self.right = self
        self.up = self
        self.down = self
        self.name = None

    def set_down(self, node):
        node.up = self
        self.down = node

    def set_right(self, node):
        node.left = self
        self.right = node

    def __repr__(self):
        return str(self.name)

class Cell(Node):
    def __init__(self, header):
        super().__init__()
        self.header = header

class Column(Node):
    def __init__(self):
        super().__init__()
        self.size = 0

    def append(self, cell):
        cell.set_down(self)
        iterator = self
        while iterator.down != self:
            iterator = iterator.down
        iterator.set_down(cell)
        self.size += 1

coverGrid = [[False for x in range(324)] for y in range(729)]
for row in range(729):
    for col in range(324):
        if col < 81:
            if row//9 == col:
                coverGrid[row][col] = True
        elif col < 162:
            if row//81 == (col-81)//9 and row%9 == col%9:
                coverGrid[row][col] = True
        elif col < 243:
            if row//9%9 == (col-162)//9 and row%9 == col%9:
                coverGrid[row][col] = True
        elif col < 324:
            if row//243 == (col-243)//27 and row//27%3 == (col-243)//9%3 and row%9 == col%9:
                coverGrid[row][col] = True

root = Column()
iterator = root
for i in range(324):
    header = Column()
    header.name = i
    iterator.set_right(header)
    iterator = iterator.right
iterator.set_right(root)

iterator = root.right
for i in range(729):
    previous = None
    first = None
    for j in range(324):
        if coverGrid[i][j]:
            cell = Cell(iterator)
            cell.name = i
            iterator.append(cell)
            if previous is None:
                previous = cell
                first = cell
            else:
                previous.set_right(cell)
                previous = previous.right
        iterator = iterator.right
    previous.set_right(first)
    iterator = root.right

def print_cover():
    cover = []
    iterator = root.right
    for i in range(729):
        row =''
        j = 0
        while iterator.right != root:
            if iterator.name == j:
                cell = iterator.down
                while cell.name < i and cell.down.name > cell.name:
                    cell = cell.down
                if cell.name != i:
                    row += '.'
                else:
                    row += '1'
            else:
                row += '.'
            if iterator.right.name == j+1:
                iterator = iterator.right
            j += 1
        iterator = root.right
        cover.append(row)
    for row in cover:
        print(row)

def cover(column):
    column.right.left = column.left
    column.left.right = column.right
    row_iterator = column.down
    while row_iterator != column:
        cell_iterator = row_iterator.right
        while cell_iterator != row_iterator:
            cell_iterator.down.up = cell_iterator.up
            cell_iterator.up.down = cell_iterator.down
            cell_iterator.header.size -= 1
            cell_iterator = cell_iterator.right
        row_iterator = row_iterator.down

def uncover(column):
    row_iterator = column.up
    while row_iterator != column:
        cell_iterator = row_iterator.left
        while cell_iterator != row_iterator:
            cell_iterator.header.size += 1
            cell_iterator.down.up = cell_iterator
            cell_iterator.up.down = cell_iterator
            cell_iterator = cell_iterator.left
        row_iterator = row_iterator.up
    column.right.left = column
    column.left.right = column

def select_option(column,option):
    cover(column)
    row = column.down
    while row.name < option:
        row = row.down
    col_iterator = row.right
    while col_iterator != row:
        cover(col_iterator.header)
        col_iterator = col_iterator.right

def select_min():
    col = root.right
    min = col.size
    col_iterator = root.right
    while col_iterator != root:
        if col_iterator.size < min:
            col = col_iterator
            min = col_iterator.size
        col_iterator = col_iterator.right
    return col

def dance():
    global puzzle
    if root.right == root:
        puzzle = [c.name % 9 + 1 for c in puzzle]
        file = open(sys.argv[2], 'w')
        output = ''
        row = ''
        for i in range(81):
            row += str(puzzle[i]) + ','
            if i % 9 == 8:
                output += row[:-1] + '\n'
                row = ''
        file.write(output)
        file.close()
        return True
    col = select_min()
    cover(col)
    row = col.down
    while row != col:
        puzzle[row.name//9] = row
        col_iterator = row.right
        while col_iterator != row:
            cover(col_iterator.header)
            col_iterator = col_iterator.right
        if dance():
            break
        col_iterator = row.left
        while col_iterator != row:
            uncover(col_iterator.header)
            col_iterator = col_iterator.left
        row = row.down
        global backtracks
        backtracks += 1
    uncover(col)
    return False

puzzle = [r.strip() for r in open(sys.argv[1], 'r').readlines()]
p_index = 0
for i in range(len(puzzle)):
    if sys.argv[3] in puzzle[i]:
        name = puzzle[i]
        p_index = i + 1
        break
puzzle = sum([r.split(',') for r in puzzle[p_index:p_index + 9]],[])
puzzle = [0 if v == '_' else int(v) for v in puzzle]

for i in range(81):
    if puzzle[i] != 0:
        node = Node()
        node.name = i*9+puzzle[i]-1
        puzzle[i] = node
        select_option(iterator,node.name)
    iterator = iterator.right

backtracks = 0
start = time()
dance()
time = time()-start

print(backtracks)
print(time)