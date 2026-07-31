.include "macros.inc"
.file "vigettvformat_80172a8c.c"

# 0x00000000 - 0x00000068
.text
.balign 4

.fn VIGetTvFormat, global
/* 00000000 00000034  7C 08 02 A6 */	mflr r0
/* 00000004 00000038  90 01 00 04 */	stw r0, 0x4(r1)
/* 00000008 0000003C  94 21 FF F0 */	stwu r1, -0x10(r1)
/* 0000000C 00000040  93 E1 00 0C */	stw r31, 0xc(r1)
/* 00000010 00000044  48 00 00 01 */	bl OSDisableInterrupts
/* 00000014 00000048  80 A0 00 00 */	lwz r5, CurrTvMode@sda21(r0)
/* 00000018 0000004C  28 05 00 07 */	cmplwi r5, 0x7
/* 0000001C 00000050  41 81 00 30 */	bgt .L_0000004C
/* 00000020 00000054  3C 80 80 23 */	lis r4, 0x8023
/* 00000024 00000058  38 84 1E 74 */	addi r4, r4, 0x1e74
/* 00000028 0000005C  54 A0 10 3A */	slwi r0, r5, 2
/* 0000002C 00000060  7C 04 00 2E */	lwzx r0, r4, r0
/* 00000030 00000064  7C 09 03 A6 */	mtctr r0
/* 00000034 00000068  4E 80 04 20 */	bctr
/* 00000038 0000006C  3B E0 00 00 */	li r31, 0x0
/* 0000003C 00000070  48 00 00 10 */	b .L_0000004C
/* 00000040 00000074  3B E0 00 01 */	li r31, 0x1
/* 00000044 00000078  48 00 00 08 */	b .L_0000004C
/* 00000048 0000007C  7C BF 2B 78 */	mr r31, r5
.L_0000004C:
/* 0000004C 00000080  48 00 00 01 */	bl OSRestoreInterrupts
/* 00000050 00000084  7F E3 FB 78 */	mr r3, r31
/* 00000054 00000088  80 01 00 14 */	lwz r0, 0x14(r1)
/* 00000058 0000008C  83 E1 00 0C */	lwz r31, 0xc(r1)
/* 0000005C 00000090  38 21 00 10 */	addi r1, r1, 0x10
/* 00000060 00000094  7C 08 03 A6 */	mtlr r0
/* 00000064 00000098  4E 80 00 20 */	blr
.endfn VIGetTvFormat

# 0x00000000 - 0x00000004
.section .sbss, "wa", @nobits
.balign 8

.obj CurrTvMode, global
	.skip 0x4
.endobj CurrTvMode
