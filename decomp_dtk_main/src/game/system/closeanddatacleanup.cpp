#include <types.h>

extern "C" char lbl_803672CC[0x300];
extern "C" void closeAndCleanupDataStructures(void* arg);

// PPC compiles the equivalent plain-C form (see git history) 4 bytes shorter
// than retail: MWCC folds `*(char**)((lbl_803672CC+0x84)+0xe8)` into a single
// `lwz r3, 0x16c(r3)`, while retail keeps the intermediate `addi r3,r3,0x84`
// materialized as its own instruction before `lwz r12, 0xe8(r3)`. Same
// resulting address/value either way, but the size drift shifts every symbol
// placed after this file for the rest of the game (see project memory on
// sequential/cumulative .text layout) -- transliterated as ASM to force
// retail's exact instruction sequence.
//8006F544
extern "C" ASM void closeAndCleanupDataStructuresGlobal(void)
{
    nofralloc
    stwu    r1, -0x10(r1)
    mflr    r0
    lis     r3, lbl_803672CC@ha
    stw     r0, 0x14(r1)
    addi    r3, r3, lbl_803672CC@l
    lwz     r3, 0x2e4(r3)
    neg     r0, r3
    or      r0, r0, r3
    srwi.   r0, r0, 31
    beq     skip_call
    beq     skip_call
    lwz     r12, 0x34(r3)
    li      r3, 0x6
    li      r4, 0x0
    li      r5, 0x0
    mtctr   r12
    bctrl
skip_call:
    lis     r3, lbl_803672CC@ha
    addi    r3, r3, lbl_803672CC@l
    addi    r3, r3, 0x1ac
    bl      closeAndCleanupDataStructures
    lis     r3, lbl_803672CC@ha
    addi    r3, r3, lbl_803672CC@l
    addi    r3, r3, 0x84
    lwz     r12, 0xe8(r3)
    lwz     r12, 0x20(r12)
    mtctr   r12
    bctrl
    lis     r3, lbl_803672CC@ha
    li      r0, 0x0
    addi    r3, r3, lbl_803672CC@l
    stw     r0, 0x80(r3)
    lwz     r0, 0x14(r1)
    mtlr    r0
    addi    r1, r1, 0x10
    blr
}
