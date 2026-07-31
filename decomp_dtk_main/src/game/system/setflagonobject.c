#include <types.h>

void setFlagOnObject(void* obj, u32 mask)
{
    if (obj != 0)
    {
        *(u32*)((char*)obj + 4) |= mask;
    }
}
