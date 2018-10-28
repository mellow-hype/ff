#include <stdio.h>
#include <stdlib.h>

int main()
{
    char tinybuf[1000];
    strcpy(tinybuf, getenv("DUMMY"));	// vulnerable to overflow
    return 0;
}
