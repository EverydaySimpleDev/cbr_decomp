.include "macros.inc"
.file "ppcdisablespeculation_80161234.c"

# 0x00000000 - 0x00000028
.text
.balign 4

.fn PPCDisableSpeculation, global
/* 00000000 00000040  7C 08 02 A6 */	mflr r0
/* 00000004 00000044  90 01 00 04 */	stw r0, 0x4(r1)
/* 00000008 00000048  94 21 FF F8 */	stwu r1, -0x8(r1)
/* 0000000C 0000004C  48 00 00 01 */	bl PPCMfhid0
/* 00000010 00000050  60 63 02 00 */	ori r3, r3, 0x200
/* 00000014 00000054  48 00 00 01 */	bl PPCMtHID0
/* 00000018 00000058  80 01 00 0C */	lwz r0, 0xc(r1)
/* 0000001C 0000005C  38 21 00 08 */	addi r1, r1, 0x8
/* 00000020 00000060  7C 08 03 A6 */	mtlr r0
/* 00000024 00000064  4E 80 00 20 */	blr
.endfn PPCDisableSpeculation
