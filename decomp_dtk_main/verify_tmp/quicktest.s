.include "macros.inc"
.file "checkstatusinverted_800a8494.cpp"

# 0x00000000 - 0x0000003C
.text
.balign 4

.fn fn_800A8494, global
/* 00000000 00000034  94 21 FF F0 */	stwu r1, -0x10(r1)
/* 00000004 00000038  7C 08 02 A6 */	mflr r0
/* 00000008 0000003C  3C 60 00 00 */	lis r3, MainGame@ha
/* 0000000C 00000040  90 01 00 14 */	stw r0, 0x14(r1)
/* 00000010 00000044  38 63 00 00 */	addi r3, r3, MainGame@l
/* 00000014 00000048  3C 63 00 0E */	addis r3, r3, 0xe
/* 00000018 0000004C  80 85 00 14 */	lwz r4, 0x14(r5)
/* 0000001C 00000050  38 63 7E 24 */	addi r3, r3, 0x7e24
/* 00000020 00000054  48 00 00 01 */	bl checkTaskStatusForParam
/* 00000024 00000058  7C 60 00 34 */	cntlzw r0, r3
/* 00000028 0000005C  54 03 D9 7E */	srwi r3, r0, 5
/* 0000002C 00000060  80 01 00 14 */	lwz r0, 0x14(r1)
/* 00000030 00000064  7C 08 03 A6 */	mtlr r0
/* 00000034 00000068  38 21 00 10 */	addi r1, r1, 0x10
/* 00000038 0000006C  4E 80 00 20 */	blr
.endfn fn_800A8494
