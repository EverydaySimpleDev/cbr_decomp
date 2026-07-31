#include <types.h>

extern "C" void fn_8000877C(void* self, int mode);
extern "C" void __dl__FPv(void* ptr);
extern "C" char lbl_8022A0E8[];

#define VTABLE(base) (*(void**)((char*)(base) + 0x34))

//800E25AC
extern "C" void* XObjLeticker__dt(void* self, s16 flag)
{
    if (self != 0)
    {
        VTABLE(self) = lbl_8022A0E8;
        fn_8000877C(self, 0);
        if (flag > 0)
        {
            __dl__FPv(self);
        }
    }
    return self;
}
