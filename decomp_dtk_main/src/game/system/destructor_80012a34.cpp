#include <types.h>

extern "C" void __dl__FPv(void* ptr);
extern "C" char lbl_802100A4[];

#define VTABLE(base) (*(void**)((char*)(base) + 0x4))

//80012A34
extern "C" void* fn_80012A34(void* self, s16 flag)
{
    if (self != 0)
    {
        VTABLE(self) = lbl_802100A4;
        if (flag > 0)
        {
            __dl__FPv(self);
        }
    }
    return self;
}
