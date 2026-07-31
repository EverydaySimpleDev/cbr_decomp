#include <types.h>

void* RingGetStart(void* ring)
{
    if (ring == 0)
    {
        return 0;
    }
    return *(void**)((char*)ring + 8);
}
