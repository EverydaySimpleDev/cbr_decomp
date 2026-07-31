.include "macros.inc"
.file "dvdlowsetwatype_8016d6cc.c"

# 0x00000000 - 0x00000044
.text
.balign 4

.fn __DVDLowSetWAType, global
/* 00000000 00000040  7C 08 02 A6 */	mflr r0
/* 00000004 00000044  90 01 00 04 */	stw r0, 0x4(r1)
/* 00000008 00000048  94 21 FF E8 */	stwu r1, -0x18(r1)
/* 0000000C 0000004C  93 E1 00 14 */	stw r31, 0x14(r1)
/* 00000010 00000050  3B E4 00 00 */	addi r31, r4, 0x0
/* 00000014 00000054  93 C1 00 10 */	stw r30, 0x10(r1)
/* 00000018 00000058  3B C3 00 00 */	addi r30, r3, 0x0
/* 0000001C 0000005C  48 00 00 01 */	bl OSDisableInterrupts
/* 00000020 00000060  93 C0 00 00 */	stw r30, WorkAroundType_8065B514@sda21(r0)
/* 00000024 00000064  93 E0 00 00 */	stw r31, WorkAroundSeekLocation_8065B518@sda21(r0)
/* 00000028 00000068  48 00 00 01 */	bl OSRestoreInterrupts
/* 0000002C 0000006C  80 01 00 1C */	lwz r0, 0x1c(r1)
/* 00000030 00000070  83 E1 00 14 */	lwz r31, 0x14(r1)
/* 00000034 00000074  83 C1 00 10 */	lwz r30, 0x10(r1)
/* 00000038 00000078  38 21 00 18 */	addi r1, r1, 0x18
/* 0000003C 0000007C  7C 08 03 A6 */	mtlr r0
/* 00000040 00000080  4E 80 00 20 */	blr
.endfn __DVDLowSetWAType
