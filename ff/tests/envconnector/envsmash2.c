#include <stdio.h>
#include <stdlib.h>

int main()
{
    char tinybuf[400];
    strcpy(tinybuf, getenv("DUMMY"));	// vulnerable to overflow
    printf(tinybuf);  			// vulnerable to format string
    return 0;
}
