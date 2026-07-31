#include <types.h>

//80169D84
extern "C" ASM void fn_80169D84(register void* self)
{
#ifdef __MWERKS__ // clang-format off
    nofralloc
    li      r4, 0
    stw     r4, 0xc(self)
    li      r0, -1
    stw     r4, 0x8(self)
    stw     r4, 0x4(self)
    stw     r0, 0x14(self)
    stw     r4, 0x10(self)
    stw     r4, 0x1c(self)
    stw     r4, 0x18(self)
    blr
#endif // clang-format on
}
