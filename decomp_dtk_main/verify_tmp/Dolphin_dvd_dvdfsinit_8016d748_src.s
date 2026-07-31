.include "macros.inc"
.file "dvdfsinit_8016d748.c"

# 0x00000000 - 0x00000038
.text
.balign 4

.fn __DVDFSInit, global
/* 00000000 00000034  3C 60 80 00 */	lis r3, 0x8000
/* 00000004 00000038  90 60 00 00 */	stw r3, BootInfo@sda21(r0)
/* 00000008 0000003C  80 03 00 38 */	lwz r0, 0x38(r3)
/* 0000000C 00000040  90 00 00 00 */	stw r0, FstStart@sda21(r0)
/* 00000010 00000044  80 60 00 00 */	lwz r3, FstStart@sda21(r0)
/* 00000014 00000048  28 03 00 00 */	cmplwi r3, 0x0
/* 00000018 0000004C  4D 82 00 20 */	beqlr
/* 0000001C 00000050  80 03 00 08 */	lwz r0, 0x8(r3)
/* 00000020 00000054  90 00 00 00 */	stw r0, MaxEntryNum@sda21(r0)
/* 00000024 00000058  80 00 00 00 */	lwz r0, MaxEntryNum@sda21(r0)
/* 00000028 0000005C  1C 00 00 0C */	mulli r0, r0, 0xc
/* 0000002C 00000060  7C 03 02 14 */	add r0, r3, r0
/* 00000030 00000064  90 00 00 00 */	stw r0, FstStringStart@sda21(r0)
/* 00000034 00000068  4E 80 00 20 */	blr
.endfn __DVDFSInit

# 0x00000000 - 0x00000010
.section .sbss, "wa", @nobits
.balign 8

.obj MaxEntryNum, local
	.skip 0x4
.endobj MaxEntryNum

.obj FstStringStart, local
	.skip 0x4
.endobj FstStringStart

.obj FstStart, local
	.skip 0x4
.endobj FstStart

.obj BootInfo, local
	.skip 0x4
.endobj BootInfo
