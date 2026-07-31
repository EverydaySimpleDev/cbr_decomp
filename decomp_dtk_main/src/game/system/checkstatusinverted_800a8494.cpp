#include <types.h>

extern "C" char MainGame[];
extern "C" int checkTaskStatusForParam(void* ctx, int param);

// DEFERRED: not byte-exact -- 2-instruction scheduling residual
// (unfixable via source restructuring). See project memory.
//800A8494
extern "C" int fn_800A8494(void* unused, char* a, char* b)
{
    char* ctx = MainGame + 0xE7E24;
    int b14 = *(int*)(b + 0x14);
    int r = checkTaskStatusForParam(ctx, b14);
    return r == 0 ? 1 : 0;
}
