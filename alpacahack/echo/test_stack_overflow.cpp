#include <bits/stdc++.h>
using namespace std;

int main(){
    char buf[10];
    int N = 12;
    char* p = buf;
    for(int i=0; i<N;i++){
        // buf[i] = char('a'+i);
        *(p++) = char('a'+i);
        printf("%d %d\n", N, i);
    }
    // buf[N] = '\0';
    // *p = '\0';
    printf("%s ||\n", buf);
}


/*

lower address
    │
    ▼
+----------------+
| buf[0]          |
| buf[1]          |
| ...             |
| buf[9]          |
+----------------+
| N               |  ← ここを buf[10] 以降が上書き
+----------------+
| i               |  ← ここも上書き
+----------------+
| p               |
+----------------+
higher address

```
gdb-peda$ p &buf
$1 = (char (*)[10]) 0x7ffc8620bc76
gdb-peda$ p &N
$2 = (int *) 0x7ffc8620bc80
gdb-peda$ p &i
$3 = (int *) 0x7ffc8620bc84
gdb-peda$ p &p
$4 = (char **) 0x7ffc8620bc88
gdb-peda$ p/x &p
$5 = 0x7ffc8620bc88
gdb-peda$ p/x &buf
$6 = 0x7ffc8620bc76
gdb-peda$ x/32bx &buf
0x7ffc8620bc76: 0x61    0x62    0x63    0x64    0x65    0x66    0x67    0x68
0x7ffc8620bc7e: 0x69    0x6a    0x6b    0x6c    0x6d    0x6e    0xa0    0xf4
0x7ffc8620bc86: 0xd2    0xd3    0x01    0xe0    0x20    0x86    0xfc    0x7f
0x7ffc8620bc8e: 0x00    0x00    0x30    0xbd    0x20    0x86    0xfc    0x7f
```

12 0
12 1 
12 2 
12 3 
12 4 
12 5 
12 6 
12 7 
12 8 
12 9 
107 10 
27755 11 
7171179 12
1852664939 13
1852664939 111
1852664939 53616
*/