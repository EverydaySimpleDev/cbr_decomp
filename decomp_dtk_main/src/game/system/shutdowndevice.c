#include <types.h>

extern int fn_8018D3FC(void* buf);
extern int DVDClose(void);

// DEFERRED: not byte-exact -- branchless bit-trick optimization residual
// (unfixable via source restructuring). See project memory.
int ShutDownDevice(void* obj)
{
    if (*(s32*)((char*)obj + 0xc0) < 0)
    {
        return 0;
    }
    *(s32*)((char*)obj + 0xc0) = -1;
    if (*(u32*)((char*)obj + 0xd4) != 0)
    {
        return (fn_8018D3FC((char*)obj + 0xd8) != 0) ? 0 : -5;
    }
    return (DVDClose() != 0) ? 0 : -5;
}
