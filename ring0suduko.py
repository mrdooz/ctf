from itertools import *
from copy import *


def parse_suduko(s):
    board = []
    for r in s.split('\n'):
        r = r.strip()
        if not r:
            continue
        if r[0] != '|':
            continue
        r = r[1:-1]
        # at a row that contains numbers
        r = r.replace(' ', '')
        r = r.split('|')
        board.append([int(x) if x else 0 for x in r])
    return board


def determine_holes(board):
    res = []
    for i in range(9):
        for j in range(9):
            if not board[i][j]:
                res.append((i, j))
    return res


def candidates(row, col, board):
    nums = set(range(1, 10))
    rows = set([board[row][i] for i in range(9)])
    cols = set([board[i][col] for i in range(9)])
    rr = row // 3 * 3
    cc = col // 3 * 3
    square = set([board[i+rr][j+cc] for i in range(3) for j in range(3)])
    return nums.difference(rows | cols | square)


def is_solution(board):
    nums = set(range(1, 10))
    # check each row
    for i in range(9):
        vals = set([board[i][j] for j in range(9)])
        if nums.difference(vals):
            return False

    for i in range(9):
        vals = set([board[j][i] for j in range(9)])
        if nums.difference(vals):
            return False

    for i in range(3):
        for j in range(3):
            vals = set([board[i*3+ii][j*3+jj] for ii in range(3) for jj in range(3)])
            if nums.difference(vals):
                return False

    return True


def solve(board):
    holes = determine_holes(board)
    if not holes:
        return board

    org = deepcopy(board)

    for hole in holes:
        row, col = hole
        cands = candidates(row, col, board)
        if not cands:
            board = org
            return False
        for c in cands:
            tmp = deepcopy(board)
            board[row][col] = c
            b = solve(board)
            if b:
                return b
            board = tmp

board = parse_suduko(open('suduko.txt').read())
s = solve(board)
# print s
print ','.join([str(x) for x in chain.from_iterable(s)])
