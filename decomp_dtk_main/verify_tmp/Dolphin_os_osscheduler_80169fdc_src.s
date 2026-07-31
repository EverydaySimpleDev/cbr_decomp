.include "macros.inc"
.file "osscheduler_80169fdc.c"

# 0x00000000 - 0x00000080
.text
.balign 4

.fn OSDisableScheduler, global
/* 00000000 00000034  7C 08 02 A6 */	mflr r0
/* 00000004 00000038  90 01 00 04 */	stw r0, 0x4(r1)
/* 00000008 0000003C  94 21 FF F0 */	stwu r1, -0x10(r1)
/* 0000000C 00000040  93 E1 00 0C */	stw r31, 0xc(r1)
/* 00000010 00000044  48 00 00 01 */	bl OSDisableInterrupts
/* 00000014 00000048  80 80 00 00 */	lwz r4, Reschedule@sda21(r0)
/* 00000018 0000004C  38 04 00 01 */	addi r0, r4, 0x1
/* 0000001C 00000050  90 00 00 00 */	stw r0, Reschedule@sda21(r0)
/* 00000020 00000054  7C 9F 23 78 */	mr r31, r4
/* 00000024 00000058  48 00 00 01 */	bl OSRestoreInterrupts
/* 00000028 0000005C  7F E3 FB 78 */	mr r3, r31
/* 0000002C 00000060  80 01 00 14 */	lwz r0, 0x14(r1)
/* 00000030 00000064  83 E1 00 0C */	lwz r31, 0xc(r1)
/* 00000034 00000068  38 21 00 10 */	addi r1, r1, 0x10
/* 00000038 0000006C  7C 08 03 A6 */	mtlr r0
/* 0000003C 00000070  4E 80 00 20 */	blr
.endfn OSDisableScheduler

.fn OSEnableScheduler, global
/* 00000040 00000074  7C 08 02 A6 */	mflr r0
/* 00000044 00000078  90 01 00 04 */	stw r0, 0x4(r1)
/* 00000048 0000007C  94 21 FF F0 */	stwu r1, -0x10(r1)
/* 0000004C 00000080  93 E1 00 0C */	stw r31, 0xc(r1)
/* 00000050 00000084  48 00 00 01 */	bl OSDisableInterrupts
/* 00000054 00000088  80 80 00 00 */	lwz r4, Reschedule@sda21(r0)
/* 00000058 0000008C  38 04 FF FF */	subi r0, r4, 0x1
/* 0000005C 00000090  90 00 00 00 */	stw r0, Reschedule@sda21(r0)
/* 00000060 00000094  7C 9F 23 78 */	mr r31, r4
/* 00000064 00000098  48 00 00 01 */	bl OSRestoreInterrupts
/* 00000068 0000009C  7F E3 FB 78 */	mr r3, r31
/* 0000006C 000000A0  80 01 00 14 */	lwz r0, 0x14(r1)
/* 00000070 000000A4  83 E1 00 0C */	lwz r31, 0xc(r1)
/* 00000074 000000A8  38 21 00 10 */	addi r1, r1, 0x10
/* 00000078 000000AC  7C 08 03 A6 */	mtlr r0
/* 0000007C 000000B0  4E 80 00 20 */	blr
.endfn OSEnableScheduler
