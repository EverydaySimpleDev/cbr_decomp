#include <types.h>

//800B2004
extern "C" int GetValueAtOffset_784(char* obj)
{
    return *(int*)(obj + 0x784);
}

//800B200C
extern "C" int gdev_cc_shutdown_7(void)
{
    return 0;
}

//800B2014
extern "C" int IsFlag80Set_(char* obj)
{
    int mask2 = 0;
    int a = *(int*)(obj + 0x228) & 0x80;
    int b = *(int*)(obj + 0x22c) & mask2;
    b = b ^ mask2;
    a = a ^ mask2;
    return (b | a) != 0;
}

//800B2048
extern "C" int IsFlagSetInParameter_228(char* obj)
{
    int mask2 = 0;
    int a = *(int*)(obj + 0x228) & 1;
    int b = *(int*)(obj + 0x22c) & mask2;
    b = b ^ mask2;
    a = a ^ mask2;
    return (b | a) != 0;
}
