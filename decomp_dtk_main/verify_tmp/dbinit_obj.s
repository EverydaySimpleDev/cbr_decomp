.include "macros.inc"
.file "dbinit_80161264.c"

# 0x00000000 - 0x00000070
.text
.balign 4

.fn DBInit, global
/* 00000000 00000040  3C 80 80 00 */	lis r4, 0x8000
/* 00000004 00000044  38 04 00 40 */	addi r0, r4, 0x40
/* 00000008 00000048  3C 60 00 00 */	lis r3, __DBExceptionDestination@ha
/* 0000000C 0000004C  90 00 00 00 */	stw r0, __DBInterface@sda21(r0)
/* 00000010 00000050  38 63 00 00 */	addi r3, r3, __DBExceptionDestination@l
/* 00000014 00000054  3C 03 80 00 */	addis r0, r3, 0x8000
/* 00000018 00000058  90 04 00 48 */	stw r0, 0x48(r4)
/* 0000001C 0000005C  38 00 00 01 */	li r0, 0x1
/* 00000020 00000060  90 00 00 00 */	stw r0, DBVerbose@sda21(r0)
/* 00000024 00000064  4E 80 00 20 */	blr
.endfn DBInit

.fn __DBExceptionDestinationAux, global
/* 00000028 00000068  7C 08 02 A6 */	mflr r0
/* 0000002C 0000006C  3C 60 00 00 */	lis r3, lbl_8022FA00@ha
/* 00000030 00000070  90 01 00 04 */	stw r0, 0x4(r1)
/* 00000034 00000074  38 63 00 00 */	addi r3, r3, lbl_8022FA00@l
/* 00000038 00000078  4C C6 31 82 */	crclr cr1eq
/* 0000003C 0000007C  94 21 FF E8 */	stwu r1, -0x18(r1)
/* 00000040 00000080  93 E1 00 14 */	stw r31, 0x14(r1)
/* 00000044 00000084  80 80 00 C0 */	lwz r4, 0xc0(r0)
/* 00000048 00000088  3F E4 80 00 */	addis r31, r4, 0x8000
/* 0000004C 0000008C  48 00 00 01 */	bl OSReport
/* 00000050 00000090  7F E3 FB 78 */	mr r3, r31
/* 00000054 00000094  48 00 00 01 */	bl OSDumpContext
/* 00000058 00000098  48 00 00 01 */	bl PPCHalt
/* 0000005C 0000009C  80 01 00 1C */	lwz r0, 0x1c(r1)
/* 00000060 000000A0  83 E1 00 14 */	lwz r31, 0x14(r1)
/* 00000064 000000A4  38 21 00 18 */	addi r1, r1, 0x18
/* 00000068 000000A8  7C 08 03 A6 */	mtlr r0
/* 0000006C 000000AC  4E 80 00 20 */	blr
.endfn __DBExceptionDestinationAux
