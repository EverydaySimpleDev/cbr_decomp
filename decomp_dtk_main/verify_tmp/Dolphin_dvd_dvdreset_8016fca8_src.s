.include "macros.inc"
.file "dvdreset_8016fca8.c"

# 0x00000000 - 0x00000044
.text
.balign 4

.fn DVDReset, global
/* 00000000 00000034  7C 08 02 A6 */	mflr r0
/* 00000004 00000038  90 01 00 04 */	stw r0, 0x4(r1)
/* 00000008 0000003C  94 21 FF F8 */	stwu r1, -0x8(r1)
/* 0000000C 00000040  48 00 00 01 */	bl DVDLowReset
/* 00000010 00000044  3C 60 CC 00 */	lis r3, 0xcc00
/* 00000014 00000048  38 00 00 2A */	li r0, 0x2a
/* 00000018 0000004C  90 03 60 00 */	stw r0, 0x6000(r3)
/* 0000001C 00000050  38 83 60 00 */	addi r4, r3, 0x6000
/* 00000020 00000054  38 00 00 00 */	li r0, 0x0
/* 00000024 00000058  80 63 60 04 */	lwz r3, 0x6004(r3)
/* 00000028 0000005C  90 64 00 04 */	stw r3, 0x4(r4)
/* 0000002C 00000060  90 00 00 00 */	stw r0, ResetRequired@sda21(r0)
/* 00000030 00000064  90 00 00 00 */	stw r0, ResumeFromHere@sda21(r0)
/* 00000034 00000068  80 01 00 0C */	lwz r0, 0xc(r1)
/* 00000038 0000006C  38 21 00 08 */	addi r1, r1, 0x8
/* 0000003C 00000070  7C 08 03 A6 */	mtlr r0
/* 00000040 00000074  4E 80 00 20 */	blr
.endfn DVDReset

# 0x00000000 - 0x00000008
.section .sbss, "wa", @nobits
.balign 8

.obj ResetRequired, global
	.skip 0x4
.endobj ResetRequired

.obj ResumeFromHere, global
	.skip 0x4
.endobj ResumeFromHere
