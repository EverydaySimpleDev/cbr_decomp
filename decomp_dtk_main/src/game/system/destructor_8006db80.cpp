#include <types.h>

extern "C" void __dl__FPv(void* ptr);
extern "C" char lbl_80212D78[];

#define VTABLE(base) (*(void**)((char*)(base) + 0x84))

//8006DB80
extern "C" void* fn_8006DB80(void* self, s16 flag)
{
    if (self != 0)
    {
        VTABLE(self) = lbl_80212D78;
        if (flag > 0)
        {
            __dl__FPv(self);
        }
    }
    return self;
}
