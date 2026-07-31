.include "macros.inc"
.file "ostime_8016b070.c"

# 0x00000000 - 0x00000020
.text
.balign 4

.fn OSGetTime, global
/* 00000000 00000034  7C 6D 42 E6 */	mftb r3, 269
/* 00000004 00000038  7C 8C 42 E6 */	mftb r4, 268
/* 00000008 0000003C  7C AD 42 E6 */	mftb r5, 269
/* 0000000C 00000040  7C 03 28 00 */	cmpw r3, r5
/* 00000010 00000044  40 82 00 00 */	bne OSGetTime
/* 00000014 00000048  4E 80 00 20 */	blr
.endfn OSGetTime

.fn OSGetTick, global
/* 00000018 0000004C  7C 6C 42 E6 */	mftb r3, 268
/* 0000001C 00000050  4E 80 00 20 */	blr
.endfn OSGetTick
