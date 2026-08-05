#include <types.h>

extern void __assert(char* file, int line, char* assertion);
extern void fn_801C89A8(void* obj);

// MWCC can't express these lbl_ SDA21 address-ofs directly; hardcoded as the
// linked result instead. Values taken from the true-retail linked DOL bytes,
// not derived by hand (the unlinked .o's relocation names for this form are
// not trustworthy). This assert branch is also dead code at runtime (an
// earlier null-check already guarantees it). See project memory.
#define OPWORD_LI_R3_SDA21 opword 0x386D9020
#define OPWORD_LI_R5_SDA21 opword 0x38AD9028

//801C7744
ASM void UpdateTreeNodeState(register void* self, register u32 value, register u32 mask)
{
    nofralloc
    stwu    r1, -0x20(r1)
    mflr    r0
    stw     r0, 0x24(r1)
    stw     r31, 0x1c(r1)
    mr      r31, mask
    stw     r30, 0x18(r1)
    stw     r29, 0x14(r1)
    mr.     r29, self
    beq     epilogue
    lwz     r0, 0x14(r29)
    and     r30, value, r31
    xor     r0, r0, r30
    rlwinm. r0, r0, 0, 28, 28
    beq     merge
    cmplwi  r29, 0x0
    beq     merge
    bne     skipAssert
    OPWORD_LI_R3_SDA21
    li      r4, 0x25d
    OPWORD_LI_R5_SDA21
    bl      __assert
skipAssert:
    lwz     r4, 0x14(r29)
    li      r3, 0x0
    rlwinm. r0, r4, 0, 8, 8
    bne     checkResult
    rlwinm. r0, r4, 0, 25, 25
    beq     checkResult
    li      r3, 0x1
checkResult:
    cmpwi   r3, 0x0
    bne     merge
    mr      r3, r29
    bl      fn_801C89A8
merge:
    lwz     r0, 0x14(r29)
    andc    r0, r0, r31
    or      r0, r30, r0
    stw     r0, 0x14(r29)
epilogue:
    lwz     r0, 0x24(r1)
    lwz     r31, 0x1c(r1)
    lwz     r30, 0x18(r1)
    lwz     r29, 0x14(r1)
    mtlr    r0
    addi    r1, r1, 0x20
    blr
}
