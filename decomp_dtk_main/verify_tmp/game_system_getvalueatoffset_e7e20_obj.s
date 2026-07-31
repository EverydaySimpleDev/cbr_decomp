.include "macros.inc"
.file "getvalueatoffset_e7e20.c"

# 0x00000000 - 0x00000034
.text
.balign 4

.fn ReturnValue, global
/* 00000000 00000040  3C 63 00 0E */	addis r3, r3, 0xe
/* 00000004 00000044  80 63 7E 20 */	lwz r3, 0x7e20(r3)
/* 00000008 00000048  4E 80 00 20 */	blr
.endfn ReturnValue

.fn GetFieldAt0x1B0C, global
/* 0000000C 0000004C  80 63 1B 0C */	lwz r3, 0x1b0c(r3)
/* 00000010 00000050  4E 80 00 20 */	blr
.endfn GetFieldAt0x1B0C

.fn fn_8000A540, global
/* 00000014 00000054  38 63 1B 20 */	addi r3, r3, 0x1b20
/* 00000018 00000058  4E 80 00 20 */	blr
.endfn fn_8000A540

.fn fn_8000A548, global
/* 0000001C 0000005C  38 63 1C B4 */	addi r3, r3, 0x1cb4
/* 00000020 00000060  4E 80 00 20 */	blr
.endfn fn_8000A548

.fn fn_8000A550, global
/* 00000024 00000064  38 63 1E 48 */	addi r3, r3, 0x1e48
/* 00000028 00000068  4E 80 00 20 */	blr
.endfn fn_8000A550

.fn fn_8000A558, global
/* 0000002C 0000006C  38 63 2B A8 */	addi r3, r3, 0x2ba8
/* 00000030 00000070  4E 80 00 20 */	blr
.endfn fn_8000A558
