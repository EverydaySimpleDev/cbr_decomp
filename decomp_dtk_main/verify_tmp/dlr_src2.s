.include "macros.inc"
.file "dvdlowreset_8016d5e0.c"

# 0x00000000 - 0x000000BC
.text
.balign 4

.fn DVDLowReset, global
/* 00000000 00000034  7C 08 02 A6 */	mflr r0
/* 00000004 00000038  3C 80 CC 00 */	lis r4, 0xcc00
/* 00000008 0000003C  90 01 00 04 */	stw r0, 0x4(r1)
/* 0000000C 00000040  38 00 00 02 */	li r0, 0x2
/* 00000010 00000044  94 21 FF E0 */	stwu r1, -0x20(r1)
/* 00000014 00000048  BF 41 00 08 */	stmw r26, 0x8(r1)
/* 00000018 0000004C  3B E4 30 00 */	addi r31, r4, 0x3000
/* 0000001C 00000050  90 04 60 04 */	stw r0, 0x6004(r4)
/* 00000020 00000054  83 C4 30 24 */	lwz r30, 0x3024(r4)
/* 00000024 00000058  57 C0 07 B8 */	rlwinm r0, r30, 0, 30, 28
/* 00000028 0000005C  60 00 00 01 */	ori r0, r0, 0x1
/* 0000002C 00000060  94 1F 00 24 */	stwu r0, 0x24(r31)
/* 00000030 00000064  48 00 00 01 */	bl __OSGetSystemTime
/* 00000034 00000068  3C A0 80 00 */	lis r5, 0x8000
/* 00000038 0000006C  80 05 00 F8 */	lwz r0, 0xf8(r5)
/* 0000003C 00000070  3C A0 43 1C */	lis r5, 0x431c
/* 00000040 00000074  38 A5 DE 83 */	subi r5, r5, 0x217d
/* 00000044 00000078  54 00 F0 BE */	srwi r0, r0, 2
/* 00000048 0000007C  7C 05 00 16 */	mulhwu r0, r5, r0
/* 0000004C 00000080  54 00 8B FE */	srwi r0, r0, 15
/* 00000050 00000084  1C 00 00 0C */	mulli r0, r0, 0xc
/* 00000054 00000088  3B 44 00 00 */	addi r26, r4, 0x0
/* 00000058 0000008C  3B 63 00 00 */	addi r27, r3, 0x0
/* 0000005C 00000090  54 1C E8 FE */	srwi r28, r0, 3
/* 00000060 00000094  3B A0 00 00 */	li r29, 0x0
.L_00000064:
/* 00000064 00000098  48 00 00 01 */	bl __OSGetSystemTime
/* 00000068 0000009C  7C BA 20 10 */	subfc r5, r26, r4
/* 0000006C 000000A0  7C 1B 19 10 */	subfe r0, r27, r3
/* 00000070 000000A4  6C 04 80 00 */	xoris r4, r0, 0x8000
/* 00000074 000000A8  6F A3 80 00 */	xoris r3, r29, 0x8000
/* 00000078 000000AC  7C 1C 28 10 */	subfc r0, r28, r5
/* 0000007C 000000B0  7C 63 21 10 */	subfe r3, r3, r4
/* 00000080 000000B4  7C 64 21 10 */	subfe r3, r4, r4
/* 00000084 000000B8  7C 63 00 D1 */	neg. r3, r3
/* 00000088 000000BC  40 82 FF DC */	bne .L_00000064
/* 0000008C 000000C0  63 C0 00 05 */	ori r0, r30, 0x5
/* 00000090 000000C4  90 1F 00 00 */	stw r0, 0x0(r31)
/* 00000094 000000C8  38 00 00 01 */	li r0, 0x1
/* 00000098 000000CC  90 00 00 00 */	stw r0, ResetOccurred@sda21(r0)
/* 0000009C 000000D0  48 00 00 01 */	bl __OSGetSystemTime
/* 000000A0 000000D4  90 80 00 00 */	stw r4, LastResetEnd+0x4@sda21(r0)
/* 000000A4 000000D8  90 60 00 00 */	stw r3, LastResetEnd@sda21(r0)
/* 000000A8 000000DC  BB 41 00 08 */	lmw r26, 0x8(r1)
/* 000000AC 000000E0  80 01 00 24 */	lwz r0, 0x24(r1)
/* 000000B0 000000E4  38 21 00 20 */	addi r1, r1, 0x20
/* 000000B4 000000E8  7C 08 03 A6 */	mtlr r0
/* 000000B8 000000EC  4E 80 00 20 */	blr
.endfn DVDLowReset

# 0x00000000 - 0x0000000C
.section .sbss, "wa", @nobits
.balign 8

.obj LastResetEnd, global
	.skip 0x8
.endobj LastResetEnd

.obj ResetOccurred, global
	.skip 0x4
.endobj ResetOccurred
