.include "macros.inc"
.file "osdisableinterrupts_80166e50.c"

# 0x00000000 - 0x00000068
.text
.balign 4

.fn OSDisableInterrupts, global
/* 00000000 00000034  7C 60 00 A6 */	mfmsr r3
/* 00000004 00000038  54 64 04 5E */	rlwinm r4, r3, 0, 17, 15
/* 00000008 0000003C  7C 80 01 24 */	mtmsr r4
/* 0000000C 00000040  54 63 8F FE */	extrwi r3, r3, 1, 16
/* 00000010 00000044  4E 80 00 20 */	blr
.endfn OSDisableInterrupts

.fn OSEnableInterrupts, global
/* 00000014 00000048  7C 60 00 A6 */	mfmsr r3
/* 00000018 0000004C  60 64 80 00 */	ori r4, r3, 0x8000
/* 0000001C 00000050  7C 80 01 24 */	mtmsr r4
/* 00000020 00000054  54 63 8F FE */	extrwi r3, r3, 1, 16
/* 00000024 00000058  4E 80 00 20 */	blr
.endfn OSEnableInterrupts

.fn OSRestoreInterrupts, global
/* 00000028 0000005C  2C 03 00 00 */	cmpwi r3, 0x0
/* 0000002C 00000060  7C 80 00 A6 */	mfmsr r4
/* 00000030 00000064  41 82 00 0C */	beq .L_0000003C
/* 00000034 00000068  60 85 80 00 */	ori r5, r4, 0x8000
/* 00000038 0000006C  48 00 00 08 */	b .L_00000040
.L_0000003C:
/* 0000003C 00000070  54 85 04 5E */	rlwinm r5, r4, 0, 17, 15
.L_00000040:
/* 00000040 00000074  7C A0 01 24 */	mtmsr r5
/* 00000044 00000078  54 83 8F FE */	extrwi r3, r4, 1, 16
/* 00000048 0000007C  4E 80 00 20 */	blr
.endfn OSRestoreInterrupts

.fn __OSSetInterruptHandler, global
/* 0000004C 00000080  7C 60 07 34 */	extsh r0, r3
/* 00000050 00000084  80 60 00 00 */	lwz r3, InterruptHandlerTable@sda21(r0)
/* 00000054 00000088  54 00 10 3A */	slwi r0, r0, 2
/* 00000058 0000008C  7C A3 02 14 */	add r5, r3, r0
/* 0000005C 00000090  80 65 00 00 */	lwz r3, 0x0(r5)
/* 00000060 00000094  90 85 00 00 */	stw r4, 0x0(r5)
/* 00000064 00000098  4E 80 00 20 */	blr
.endfn __OSSetInterruptHandler
