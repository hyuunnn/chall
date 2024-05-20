from pwn import *

p = process(['python3', 'typing_game.py'])

for _ in range(200):
  stage = p.recvline()
  print(stage)
  p.recvuntil(b'answer: ')
  answer = p.recvline()[:-1]
  print(answer.decode())
  p.sendlineafter(b'Input:', answer)
  
print(p.recvline())
