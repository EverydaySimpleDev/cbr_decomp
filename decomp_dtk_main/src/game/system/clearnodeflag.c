#include <types.h>

void clearNodeFlag(void* node, u32 mask)
{
    if (node != 0)
    {
        *(u32*)((char*)node + 4) &= ~mask;
    }
}
