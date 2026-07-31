#include <types.h>

void updateFlagState(void* obj, u32 value, u32 mask)
{
    if (obj != 0)
    {
        *(u32*)((char*)obj + 0x14) = (*(u32*)((char*)obj + 0x14) & ~mask) | (value & mask);
    }
}
