.include "macros.inc"
.file "dvdFatal.c"

# 0x00000000 - 0x00000030
.text
.balign 4

.fn __DVDPrintFatalMessage, global
/* 00000000 00000040  7C 08 02 A6 */	mflr r0
/* 00000004 00000044  90 01 00 04 */	stw r0, 0x4(r1)
/* 00000008 00000048  94 21 FF F8 */	stwu r1, -0x8(r1)
/* 0000000C 0000004C  81 80 00 00 */	lwz r12, lbl_8065B5A8@sda21(r0)
/* 00000010 00000050  28 0C 00 00 */	cmplwi r12, 0x0
/* 00000014 00000054  41 82 00 0C */	beq .L_00000020
/* 00000018 00000058  7D 88 03 A6 */	mtlr r12
/* 0000001C 0000005C  4E 80 00 21 */	blrl
.L_00000020:
/* 00000020 00000060  80 01 00 0C */	lwz r0, 0xc(r1)
/* 00000024 00000064  38 21 00 08 */	addi r1, r1, 0x8
/* 00000028 00000068  7C 08 03 A6 */	mtlr r0
/* 0000002C 0000006C  4E 80 00 20 */	blr
.endfn __DVDPrintFatalMessage
