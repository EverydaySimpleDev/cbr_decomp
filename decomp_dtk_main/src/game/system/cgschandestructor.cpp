#include <types.h>

extern "C" void __dl__FPv(void* ptr);
extern "C" char HSD_CGsChannel__14HSD_CGsChannel[];

#define VTABLE(base) (*(void**)((char*)(base) + 0x34))

extern "C" void* CGSChan_Destructor(void* self, s16 flag)
{
    if (self != 0)
    {
        VTABLE(self) = HSD_CGsChannel__14HSD_CGsChannel;
        if (flag > 0)
        {
            __dl__FPv(self);
        }
    }
    return self;
}
