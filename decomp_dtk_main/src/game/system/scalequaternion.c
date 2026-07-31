#include <types.h>

extern void PSQUATScale(register const void* src, register f32 scale, register void* dst);
extern char lbl_80210314[12];

//8000F9C0
ASM void scale_quaternion(void* dst, void* a, register f32 scale)
{
    nofralloc
    stwu    r1, -0x20(r1)
    mflr    r0
    lis     r5, lbl_80210314@ha
    lwz     r7, 0x0(r4)
    stw     r0, 0x24(r1)
    addi    r0, r5, lbl_80210314@l
    lwz     r6, 0x4(r4)
    stw     r31, 0x1c(r1)
    mr      r31, r3
    lwz     r5, 0x8(r4)
    addi    r3, r1, 0x8
    stw     r7, 0x8(r1)
    mr      r4, r3
    stw     r6, 0xc(r1)
    stw     r5, 0x10(r1)
    stw     r0, 0x14(r1)
    bl      PSQUATScale
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
