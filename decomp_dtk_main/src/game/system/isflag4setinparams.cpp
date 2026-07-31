#include <types.h>

//800B1D50
extern "C" int IsFlag4SetInParams(char* obj)
{
    int mask2 = 0;
    int a = *(int*)(obj + 0x228) & 4;
    int b = *(int*)(obj + 0x22c) & mask2;
    b = b ^ mask2;
    a = a ^ mask2;
    return (b | a) != 0;
}
