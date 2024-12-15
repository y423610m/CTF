#include <bits/stdc++.h>
using namespace std;

int main(){
    char buf[10];
    int N = 12;
    char* p = buf;
    for(int i=0; i<N;i++){
        // buf[i] = char('a'+i);
        *(p++) = char('a'+i);
    }
    // buf[N] = '\0';
    *p = '\0';
    printf("%s ||\n", buf);
}