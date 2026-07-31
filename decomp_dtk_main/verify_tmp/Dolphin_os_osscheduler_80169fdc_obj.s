.include "macros.inc"
.file "osscheduler_80169fdc.c"

# 0x00000000 - 0x00000080
.text
.balign 4

.fn OSDisableScheduler, global
/* 00000000 00000040  7C 08 02 A6 */	mflr r0
/* 00000004 00000044  90 01 00 04 */	stw r0, 0x4(r1)
/* 00000008 00000048  94 21 FF F0 */	stwu r1, -0x10(r1)
/* 0000000C 0000004C  93 E1 00 0C */	stw r31, 0xc(r1)
/* 00000010 00000050  48 00 00 01 */	bl OSDisableInterrupts
/* 00000014 00000054  80 80 00 00 */	lwz r4, Reschedule@sda21(r0)
/* 00000018 00000058  38 04 00 01 */	addi r0, r4, 0x1
/* 0000001C 0000005C  90 00 00 00 */	stw r0, Reschedule@sda21(r0)
/* 00000020 00000060  7C 9F 23 78 */	mr r31, r4
/* 00000024 00000064  48 00 00 01 */	bl OSRestoreInterrupts
/* 00000028 00000068  7F E3 FB 78 */	mr r3, r31
/* 0000002C 0000006C  80 01 00 14 */	lwz r0, 0x14(r1)
/* 00000030 00000070  83 E1 00 0C */	lwz r31, 0xc(r1)
/* 00000034 00000074  38 21 00 10 */	addi r1, r1, 0x10
/* 00000038 00000078  7C 08 03 A6 */	mtlr r0
/* 0000003C 0000007C  4E 80 00 20 */	blr
.endfn OSDisableScheduler

.fn OSEnableScheduler, global
/* 00000040 00000080  7C 08 02 A6 */	mflr r0
/* 00000044 00000084  90 01 00 04 */	stw r0, 0x4(r1)
/* 00000048 00000088  94 21 FF F0 */	stwu r1, -0x10(r1)
/* 0000004C 0000008C  93 E1 00 0C */	stw r31, 0xc(r1)
/* 00000050 00000090  48 00 00 01 */	bl OSDisableInterrupts
/* 00000054 00000094  80 80 00 00 */	lwz r4, Reschedule@sda21(r0)
/* 00000058 00000098  38 04 FF FF */	subi r0, r4, 0x1
/* 0000005C 0000009C  90 00 00 00 */	stw r0, Reschedule@sda21(r0)
/* 00000060 000000A0  7C 9F 23 78 */	mr r31, r4
/* 00000064 000000A4  48 00 00 01 */	bl OSRestoreInterrupts
/* 00000068 000000A8  7F E3 FB 78 */	mr r3, r31
/* 0000006C 000000AC  80 01 00 14 */	lwz r0, 0x14(r1)
/* 00000070 000000B0  83 E1 00 0C */	lwz r31, 0xc(r1)
/* 00000074 000000B4  38 21 00 10 */	addi r1, r1, 0x10
/* 00000078 000000B8  7C 08 03 A6 */	mtlr r0
/* 0000007C 000000BC  4E 80 00 20 */	blr
.endfn OSEnableScheduler
