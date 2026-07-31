.include "macros.inc"
.file "gxfiforeadenable_80185d7c.c"

# 0x00000000 - 0x00000028
.text
.balign 4

.fn __GXFifoReadEnable, global
/* 00000000 00000034  80 60 00 00 */	lwz r3, __GXData@sda21(r0)
/* 00000004 00000038  38 80 00 01 */	li r4, 0x1
/* 00000008 0000003C  88 03 00 0B */	lbz r0, 0xb(r3)
/* 0000000C 00000040  50 80 07 FE */	rlwimi r0, r4, 0, 31, 31
/* 00000010 00000044  98 03 00 0B */	stb r0, 0xb(r3)
/* 00000014 00000048  80 80 00 00 */	lwz r4, __GXData@sda21(r0)
/* 00000018 0000004C  80 60 00 00 */	lwz r3, __cpReg@sda21(r0)
/* 0000001C 00000050  80 04 00 08 */	lwz r0, 0x8(r4)
/* 00000020 00000054  B0 03 00 02 */	sth r0, 0x2(r3)
/* 00000024 00000058  4E 80 00 20 */	blr
.endfn __GXFifoReadEnable
