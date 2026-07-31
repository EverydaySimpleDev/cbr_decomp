#include <types.h>

typedef int (*Callback4)(void*, void*, int, int);
typedef void (*Callback3)(int, int, int);

extern int fn_8019FC50(void* arg);
extern int ShutDownDevice(void* obj);
extern void* fn_80191E04(u32 size, void* heap);
extern void fn_80167C60(void* obj, void* buf);
extern char lbl_8065F854[0xc];

//801A92C4
int LoadModuleAndExecute(void* self, void* param2)
{
    void* obj;
    void* buf;
    u32 size;

    if (fn_8019FC50((char*)self + 0x4c) < 0)
    {
        return 1;
    }

    {
        Callback4 callback = *(Callback4*)((char*)*(void**)((char*)self + 0x134) + 0x24);
        if (callback((char*)self + 0x4c, param2, 0, 0) == 0)
        {
            return 0;
        }
    }

    ShutDownDevice((char*)self + 0x4c);

    obj = *(void**)((char*)self + 0x118);
    buf = 0;
    size = *(u32*)((char*)obj + 0x20);
    if (size != 0)
    {
        u32 aligned = (size + 0x1f) & ~0x1f;
        buf = fn_80191E04(aligned, lbl_8065F854);
    }
    fn_80167C60(obj, buf);

    *(void**)((char*)self + 0x138) = obj;
    *(void**)((char*)self + 0x13c) = buf;

    if (*(void**)((char*)self + 0x138) != 0)
    {
        Callback3 callback2 = *(Callback3*)((char*)*(void**)((char*)self + 0x138) + 0x34);
        callback2(-1, 0, 0);
    }

    return 1;
}
