from pwn import *
from z3 import *

p = process(['python3', 'math_master.py'])
a = Int('a')

for i in range(250):
    s = Solver()
    stage = p.recvline()
    print(stage)

    expression = p.recvline()[:-1]
    print(expression)
    s.add(eval(expression.replace(b"?", b"a").replace(b"=", b"==")))
    s.check()
    answer = s.model()[a].as_string()
    print(answer)
    
    p.sendlineafter('Input:', answer)

print(p.recvline())
