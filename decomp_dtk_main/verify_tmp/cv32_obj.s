.include "macros.inc"
.file "copyvector3_2.c"

# 0x00000000 - 0x0000001C
.text
.balign 4

.fn copyVector3_2, global
/* 00000000 00000040  C0 04 00 00 */	lfs f0, 0x0(r4)
/* 00000004 00000044  C0 24 00 04 */	lfs f1, 0x4(r4)
/* 00000008 00000048  D0 03 00 00 */	stfs f0, 0x0(r3)
/* 0000000C 0000004C  C0 04 00 08 */	lfs f0, 0x8(r4)
/* 00000010 00000050  D0 23 00 04 */	stfs f1, 0x4(r3)
/* 00000014 00000054  D0 03 00 08 */	stfs f0, 0x8(r3)
/* 00000018 00000058  4E 80 00 20 */	blr
.endfn copyVector3_2
