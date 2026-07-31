.include "macros.inc"
.file "dvdlowbreak_8016d69c.c"

# 0x00000000 - 0x00000014
.text
.balign 4

.fn DVDLowBreak, global
/* 00000000 00000040  38 00 00 01 */	li r0, 0x1
/* 00000004 00000044  90 00 00 00 */	stw r0, StopAtNextInt@sda21(r0)
/* 00000008 00000048  38 60 00 01 */	li r3, 0x1
/* 0000000C 0000004C  90 00 00 00 */	stw r0, lbl_8065B510@sda21(r0)
/* 00000010 00000050  4E 80 00 20 */	blr
.endfn DVDLowBreak
