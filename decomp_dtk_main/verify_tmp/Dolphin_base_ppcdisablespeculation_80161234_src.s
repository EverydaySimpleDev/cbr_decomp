.include "macros.inc"
.file "ppcdisablespeculation_80161234.c"

# 0x00000000 - 0x00000028
.text
.balign 4

.fn PPCDisableSpeculation, global
/* 00000000 00000034  7C 08 02 A6 */	mflr r0
/* 00000004 00000038  90 01 00 04 */	stw r0, 0x4(r1)
/* 00000008 0000003C  94 21 FF F8 */	stwu r1, -0x8(r1)
/* 0000000C 00000040  48 00 00 01 */	bl PPCMfhid0
/* 00000010 00000044  60 63 02 00 */	ori r3, r3, 0x200
/* 00000014 00000048  48 00 00 01 */	bl PPCMtHID0
/* 00000018 0000004C  80 01 00 0C */	lwz r0, 0xc(r1)
/* 0000001C 00000050  38 21 00 08 */	addi r1, r1, 0x8
/* 00000020 00000054  7C 08 03 A6 */	mtlr r0
/* 00000024 00000058  4E 80 00 20 */	blr
.endfn PPCDisableSpeculation
