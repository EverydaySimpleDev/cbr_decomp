#include <types.h>

//801C7014
ASM void* getValueIfBitSetInMask(void* obj)
{
    nofralloc
    cmplwi  r3, 0
    beq     retZero
    lwz     r0, 0x14(r3)
    andi.   r0, r0, 0x4020
    cntlzw  r0, r0
    srwi.   r0, r0, 5
    bne     retField
retZero:
    li      r3, 0
    blr
retField:
    lwz     r3, 0x18(r3)
    blr
}
