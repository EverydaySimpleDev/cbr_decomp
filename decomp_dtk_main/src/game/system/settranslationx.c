#include <types.h>

//801BA40C
ASM void setTranslationX(void* obj, register f32 x)
{
    nofralloc
    cmplwi  r3, 0x0
    beqlr
    lwz     r3, 0xc(r3)
    cmplwi  r3, 0x0
    bne     main
    opword  0x4E800020
main:
    stfs    f1, 0xc(r3)
    blr
}
