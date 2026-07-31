#include <types.h>

//801A4EC8
extern "C" void* fn_801A4EC8(void* table, u8* indexPtr)
{
    return (char*)table + (*indexPtr) * 6;
}
