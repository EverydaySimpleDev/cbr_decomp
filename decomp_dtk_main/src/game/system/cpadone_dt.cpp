#include <types.h>

extern "C" void __dl__FPv(void* ptr);
extern "C" char __vt__7CPadOne[];

#define VTABLE(base) (*(void**)((char*)(base) + 0x50))

//800083D4
extern "C" void* CPadOne__dt(void* self, s16 flag)
{
    if (self != 0)
    {
        VTABLE(self) = __vt__7CPadOne;
        if (flag > 0)
        {
            __dl__FPv(self);
        }
    }
    return self;
}
