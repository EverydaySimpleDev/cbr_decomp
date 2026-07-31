#include <types.h>

void* RingGetNext(void* node)
{
    if (node == 0)
    {
        return 0;
    }
    return *(void**)((char*)node + 8);
}
