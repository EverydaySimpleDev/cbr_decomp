#include <types.h>

extern "C" void __dl__FPv(void* ptr);
extern "C" char lbl_80210134[];

#define VTABLE(base) (*(void**)((char*)(base) + 0x94))

//80008344
extern "C" void* fn_80008344(void* self, s16 flag)
{
    if (self != 0)
    {
        VTABLE(self) = lbl_80210134;
        if (flag > 0)
        {
            __dl__FPv(self);
        }
    }
    return self;
}
