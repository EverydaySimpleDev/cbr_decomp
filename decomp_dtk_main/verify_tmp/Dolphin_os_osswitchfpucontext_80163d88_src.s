.include "macros.inc"
.file "osswitchfpucontext_80163d88.c"

# 0x00000000 - 0x000000CC
.text
.balign 4

.fn OSSwitchFPUContext, local
/* 00000000 00000034  7C A0 00 A6 */	mfmsr r5
/* 00000004 00000038  60 A5 20 00 */	ori r5, r5, 0x2000
/* 00000008 0000003C  7C A0 01 24 */	mtmsr r5
/* 0000000C 00000040  4C 00 01 2C */	isync
/* 00000010 00000044  80 A4 01 9C */	lwz r5, 0x19c(r4)
/* 00000014 00000048  60 A5 20 00 */	ori r5, r5, 0x2000
/* 00000018 0000004C  7C BB 03 A6 */	mtsrr1 r5
/* 0000001C 00000050  3C 60 80 00 */	lis r3, 0x8000
/* 00000020 00000054  80 A3 00 D8 */	lwz r5, 0xd8(r3)
/* 00000024 00000058  90 83 00 D8 */	stw r4, 0xd8(r3)
/* 00000028 0000005C  7C 05 20 00 */	cmpw r5, r4
/* 0000002C 00000060  41 82 00 14 */	beq .L_00000040
/* 00000030 00000064  2C 05 00 00 */	cmpwi r5, 0x0
/* 00000034 00000068  41 82 00 08 */	beq .L_0000003C
/* 00000038 0000006C  48 00 00 01 */	bl __OSSaveFPUContext
.L_0000003C:
/* 0000003C 00000070  48 00 00 01 */	bl __OSLoadFPUContext
.L_00000040:
/* 00000040 00000074  80 64 00 80 */	lwz r3, 0x80(r4)
/* 00000044 00000078  7C 6F F1 20 */	mtcrf 255, r3
/* 00000048 0000007C  80 64 00 84 */	lwz r3, 0x84(r4)
/* 0000004C 00000080  7C 68 03 A6 */	mtlr r3
/* 00000050 00000084  80 64 01 98 */	lwz r3, 0x198(r4)
/* 00000054 00000088  7C 7A 03 A6 */	mtsrr0 r3
/* 00000058 0000008C  80 64 00 88 */	lwz r3, 0x88(r4)
/* 0000005C 00000090  7C 69 03 A6 */	mtctr r3
/* 00000060 00000094  80 64 00 8C */	lwz r3, 0x8c(r4)
/* 00000064 00000098  7C 61 03 A6 */	mtxer r3
/* 00000068 0000009C  A0 64 01 A2 */	lhz r3, 0x1a2(r4)
/* 0000006C 000000A0  54 63 07 FA */	rlwinm r3, r3, 0, 31, 29
/* 00000070 000000A4  B0 64 01 A2 */	sth r3, 0x1a2(r4)
/* 00000074 000000A8  80 A4 00 14 */	lwz r5, 0x14(r4)
/* 00000078 000000AC  80 64 00 0C */	lwz r3, 0xc(r4)
/* 0000007C 000000B0  80 84 00 10 */	lwz r4, 0x10(r4)
/* 00000080 000000B4  4C 00 00 64 */	rfi
.endfn OSSwitchFPUContext

.fn __OSContextInit, global
/* 00000084 000000B8  7C 08 02 A6 */	mflr r0
/* 00000088 000000BC  90 01 00 04 */	stw r0, 0x4(r1)
/* 0000008C 000000C0  94 21 FF F8 */	stwu r1, -0x8(r1)
/* 00000090 000000C4  3C 60 00 00 */	lis r3, OSSwitchFPUContext@ha
/* 00000094 000000C8  38 83 00 00 */	addi r4, r3, OSSwitchFPUContext@l
/* 00000098 000000CC  38 60 00 07 */	li r3, 0x7
/* 0000009C 000000D0  48 00 00 01 */	bl __OSSetExceptionHandler
/* 000000A0 000000D4  38 00 00 00 */	li r0, 0x0
/* 000000A4 000000D8  4C C6 31 82 */	crclr cr1eq
/* 000000A8 000000DC  3C 80 80 00 */	lis r4, 0x8000
/* 000000AC 000000E0  3C 60 80 23 */	lis r3, 0x8023
/* 000000B0 000000E4  90 04 00 D8 */	stw r0, 0xd8(r4)
/* 000000B4 000000E8  38 63 04 1C */	addi r3, r3, 0x41c
/* 000000B8 000000EC  48 00 00 01 */	bl DBPrintf
/* 000000BC 000000F0  80 01 00 0C */	lwz r0, 0xc(r1)
/* 000000C0 000000F4  38 21 00 08 */	addi r1, r1, 0x8
/* 000000C4 000000F8  7C 08 03 A6 */	mtlr r0
/* 000000C8 000000FC  4E 80 00 20 */	blr
.endfn __OSContextInit

# 0x00000000 - 0x00000008
.section .sbss, "wa", @nobits
.balign 8

.obj DBVerbose, local
	.skip 0x4
.endobj DBVerbose

.obj __DBInterface, local
	.skip 0x4
.endobj __DBInterface
