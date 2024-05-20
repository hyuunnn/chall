from pwn import *

p = process(['python3', 'math_gosu.py'])

for i in range(250):
    stage = p.recvline()
    print(stage)

    expression = p.recvuntil('=')[:-1]
    print(expression)

    answer = str(eval(expression))
    print(answer)

    p.sendlineafter('Input:', answer)

print(p.recvline())
