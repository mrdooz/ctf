from itertools import *
from copy import *
from pwn import *


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
    for i in range(9):
        for j in range(9):
            if not board[i][j]:
                yield (i, j)


def candidates(row, col, board):
    rows = set([board[row][i] for i in range(9)])
    cols = set([board[i][col] for i in range(9)])
    rr = row // 3 * 3
    cc = col // 3 * 3
    square = set([board[i+rr][j+cc] for i in range(3) for j in range(3)])
    total = rows | cols | square
    for i in range(1, 10):
        if i not in total:
            yield i


def solve(board):
    for hole in determine_holes(board):
        row, col = hole
        for c in candidates(row, col, board):
            old = board[row][col]
            board[row][col] = c
            b = solve(board)
            if b:
                return b
            board[row][col] = old
        else:
            return False
    else:
        return ','.join([str(x) for x in chain.from_iterable(board)])

server = ssh("sudoku", "ringzer0team.com", 12643, "dg43zz6R0E")
sh = server.shell()
input = sh.recvuntil('Solution:')
# board = parse_suduko(open('suduko.txt').read())
board = parse_suduko(input)
s = solve(board)
sh.sendline(s)
sh.recvuntil('FLAG-')
print 'FLAG-%s' % sh.recvline().strip()
