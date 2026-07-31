.include "macros.inc"
.file "getvalueifbitsetinmask.c"

# 0x00000000 - 0x0000002C
.text
.balign 4

.fn getValueIfBitSetInMask, global
/* 00000000 00000034  28 03 00 00 */	cmplwi r3, 0x0
/* 00000004 00000038  41 82 00 18 */	beq .L_0000001C
/* 00000008 0000003C  80 03 00 14 */	lwz r0, 0x14(r3)
/* 0000000C 00000040  70 00 40 20 */	andi. r0, r0, 0x4020
/* 00000010 00000044  7C 00 00 34 */	cntlzw r0, r0
/* 00000014 00000048  54 00 D9 7F */	srwi. r0, r0, 5
/* 00000018 0000004C  40 82 00 0C */	bne .L_00000024
.L_0000001C:
/* 0000001C 00000050  38 60 00 00 */	li r3, 0x0
/* 00000020 00000054  4E 80 00 20 */	blr
.L_00000024:
/* 00000024 00000058  80 63 00 18 */	lwz r3, 0x18(r3)
/* 00000028 0000005C  4E 80 00 20 */	blr
.endfn getValueIfBitSetInMask
