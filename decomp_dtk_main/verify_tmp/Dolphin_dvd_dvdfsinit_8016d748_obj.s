.include "macros.inc"
.file "dvdfsinit_8016d748.c"

# 0x00000000 - 0x00000038
.text
.balign 4

.fn __DVDFSInit, global
/* 00000000 00000040  3C 60 80 00 */	lis r3, 0x8000
/* 00000004 00000044  90 60 00 00 */	stw r3, BootInfo_8065B538@sda21(r0)
/* 00000008 00000048  80 03 00 38 */	lwz r0, 0x38(r3)
/* 0000000C 0000004C  90 00 00 00 */	stw r0, FstStart_8065B53C@sda21(r0)
/* 00000010 00000050  80 60 00 00 */	lwz r3, FstStart_8065B53C@sda21(r0)
/* 00000014 00000054  28 03 00 00 */	cmplwi r3, 0x0
/* 00000018 00000058  4D 82 00 20 */	beqlr
/* 0000001C 0000005C  80 03 00 08 */	lwz r0, 0x8(r3)
/* 00000020 00000060  90 00 00 00 */	stw r0, MaxEntryNum_8065B544@sda21(r0)
/* 00000024 00000064  80 00 00 00 */	lwz r0, MaxEntryNum_8065B544@sda21(r0)
/* 00000028 00000068  1C 00 00 0C */	mulli r0, r0, 0xc
/* 0000002C 0000006C  7C 03 02 14 */	add r0, r3, r0
/* 00000030 00000070  90 00 00 00 */	stw r0, FstStringStart_8065B540@sda21(r0)
/* 00000034 00000074  4E 80 00 20 */	blr
.endfn __DVDFSInit
