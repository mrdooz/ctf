# http://ringzer0team.com/challenges/wu/130
from pwn import *

prompt = 'number>'
too_small = 'Nah! Your number is too small.'
too_large = 'Nah! Your number is too big.'
correct = 'You got the right number.'

server = ssh("number", "ringzer0team.com", 12643, "Z7IwIMRC2dc764L")
sh = server.shell()

r = 1e4
upper = r
lower = -r
num_games = 0
while True:
    sh.recvuntil(prompt)
    guess = 0.5 * (upper + lower)
    s = '%d' % guess
    sh.sendline(s)
    sh.recvline()
    input = sh.recvline().strip()
    if input.find(correct) != -1:
        upper = r
        lower = -r
        num_games += 1
        print 'correct guess: %d' % num_games
        if num_games == 10:
            try:
                while True:
                    print sh.recvline()
            except:
                exit(1)
    elif input.find(too_small) != -1:
        lower = guess
    else:
        upper = guess
