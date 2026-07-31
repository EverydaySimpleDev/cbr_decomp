.include "macros.inc"
.file "vigetdtvstatus_80172af4.c"

# 0x00000000 - 0x0000003C
.text
.balign 4

.fn VIGetDTVStatus, global
/* 00000000 00000040  7C 08 02 A6 */	mflr r0
/* 00000004 00000044  90 01 00 04 */	stw r0, 0x4(r1)
/* 00000008 00000048  94 21 FF F0 */	stwu r1, -0x10(r1)
/* 0000000C 0000004C  93 E1 00 0C */	stw r31, 0xc(r1)
/* 00000010 00000050  48 00 00 01 */	bl OSDisableInterrupts
/* 00000014 00000054  3C 80 CC 00 */	lis r4, 0xcc00
/* 00000018 00000058  A0 04 20 6E */	lhz r0, 0x206e(r4)
/* 0000001C 0000005C  54 1F 07 BE */	clrlwi r31, r0, 30
/* 00000020 00000060  48 00 00 01 */	bl OSRestoreInterrupts
/* 00000024 00000064  57 E3 07 FE */	clrlwi r3, r31, 31
/* 00000028 00000068  80 01 00 14 */	lwz r0, 0x14(r1)
/* 0000002C 0000006C  83 E1 00 0C */	lwz r31, 0xc(r1)
/* 00000030 00000070  38 21 00 10 */	addi r1, r1, 0x10
/* 00000034 00000074  7C 08 03 A6 */	mtlr r0
/* 00000038 00000078  4E 80 00 20 */	blr
.endfn VIGetDTVStatus
