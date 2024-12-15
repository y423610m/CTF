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
```
gdb a.out
b getval(char const*)

(gdb) info frame
Stack level 0, frame at 0x7ffdc08de910:
 rip = 0x5636a9570276 in getval (main.c:11); saved rip = 0x5636a9570337
 called by frame at 0x7ffdc08de920
 source language c++.
 Arglist at 0x7ffdc08de900, args: msg=0x5636a9571017 "value: "
 Locals at 0x7ffdc08de900, Previous frame's sp is 0x7ffdc08de910
 Saved registers:
  rbp at 0x7ffdc08de900, rip at 0x7ffdc08de908

(gdb) x/20xw $rsp
0x7ffdc08de8c0: 0x00000000      0x00000000      0xa9571017      0x00005636
0x7ffdc08de8d0: 0x00000000      0x00000000      0x00000000      0x00000000 <-buf
0x7ffdc08de8e0: 0x00000000      0x00000000      0x00000000      0x00000000
0x7ffdc08de8f0: 0x00000000      0x00000000      0xa058baf0      0x00007f15
0x7ffdc08de900: 0xc08de910      0x00007ffd      0xa9570337      0x00005636 <-rip

(gdb) p &buf
$2 = (char (*)[32]) 0x7ffdc08de8d0
```

# distance is 56 bytes.
11111111111111111111111111111111111111111111111111111111
