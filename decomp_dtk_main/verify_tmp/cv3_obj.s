.include "macros.inc"
.file "copyvector3.cpp"

# 0x00000000 - 0x00000030
.text
.balign 4

.fn copyVector3, global
/* 00000000 00000040  C0 04 00 00 */	lfs f0, 0x0(r4)
/* 00000004 00000044  C0 24 00 04 */	lfs f1, 0x4(r4)
/* 00000008 00000048  D0 03 00 00 */	stfs f0, 0x0(r3)
/* 0000000C 0000004C  C0 04 00 08 */	lfs f0, 0x8(r4)
/* 00000010 00000050  D0 23 00 04 */	stfs f1, 0x4(r3)
/* 00000014 00000054  D0 03 00 08 */	stfs f0, 0x8(r3)
/* 00000018 00000058  4E 80 00 20 */	blr
.endfn copyVector3

.fn GetNumLeadingZerosInDifference, global
/* 0000001C 0000005C  80 03 00 04 */	lwz r0, 0x4(r3)
/* 00000020 00000060  7C 04 00 50 */	subf r0, r4, r0
/* 00000024 00000064  7C 00 00 34 */	cntlzw r0, r0
/* 00000028 00000068  54 03 DE 3E */	extrwi r3, r0, 8, 19
/* 0000002C 0000006C  4E 80 00 20 */	blr
.endfn GetNumLeadingZerosInDifference
