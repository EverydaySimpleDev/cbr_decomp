#include <types.h>

extern void fn_8016C5F8(void* out, void* b, void* out2);
extern char lbl_80210314[12];

//8000F93C
ASM void AddPSVecWithScalar(void* dst, void* a, void* b)
{
    nofralloc
    stwu    r1, -0x20(r1)
    mflr    r0
    lis     r6, lbl_80210314@ha
    lwz     r8, 0x0(r4)
    stw     r0, 0x24(r1)
    addi    r0, r6, lbl_80210314@l
    lwz     r7, 0x4(r4)
    stw     r31, 0x1c(r1)
    mr      r31, r3
    lwz     r6, 0x8(r4)
    addi    r3, r1, 0x8
    stw     r8, 0x8(r1)
    mr      r4, r5
    mr      r5, r3
    stw     r7, 0xc(r1)
    stw     r6, 0x10(r1)
    stw     r0, 0x14(r1)
    bl      fn_8016C5F8
    lwz     r5, 0x8(r1)
    lis     r3, lbl_80210314@ha
    lwz     r4, 0xc(r1)
    addi    r0, r3, lbl_80210314@l
    stw     r5, 0x0(r31)
    stw     r4, 0x4(r31)
    lwz     r3, 0x10(r1)
    stw     r3, 0x8(r31)
    stw     r0, 0xc(r31)
    stw     r0, 0x14(r1)
    lwz     r0, 0x24(r1)
    lwz     r31, 0x1c(r1)
    mtlr    r0
    addi    r1, r1, 0x20
    blr
}
