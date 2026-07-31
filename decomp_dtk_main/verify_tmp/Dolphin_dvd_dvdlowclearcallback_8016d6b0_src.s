.include "macros.inc"
.file "dvdlowclearcallback_8016d6b0.c"

# 0x00000000 - 0x0000001C
.text
.balign 4

.fn DVDLowClearCallback, global
/* 00000000 00000034  3C 60 CC 00 */	lis r3, 0xcc00
/* 00000004 00000038  38 00 00 00 */	li r0, 0x0
/* 00000008 0000003C  90 03 60 04 */	stw r0, 0x6004(r3)
/* 0000000C 00000040  80 60 00 00 */	lwz r3, Callback@sda21(r0)
/* 00000010 00000044  90 00 00 00 */	stw r0, WaitingCoverClose@sda21(r0)
/* 00000014 00000048  90 00 00 00 */	stw r0, Callback@sda21(r0)
/* 00000018 0000004C  4E 80 00 20 */	blr
.endfn DVDLowClearCallback
