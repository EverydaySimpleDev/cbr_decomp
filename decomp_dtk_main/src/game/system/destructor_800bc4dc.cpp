#include <types.h>

extern "C" void __dl__FPv(void* ptr);
extern "C" char lbl_80227E58[];

#define VTABLE(base) (*(void**)((char*)(base) + 0x27C))

//800BC4DC
extern "C" void* fn_800BC4DC(void* self, s16 flag)
{
    if (self != 0)
    {
        VTABLE(self) = lbl_80227E58;
        if (flag > 0)
        {
            __dl__FPv(self);
        }
    }
    return self;
}
