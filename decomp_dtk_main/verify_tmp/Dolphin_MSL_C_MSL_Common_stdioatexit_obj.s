.include "macros.inc"
.file "stdioatexit.c"

# 0x00000000 - 0x00000010
.text
.balign 4

.fn __stdio_atexit, global
/* 00000000 00000040  3C 60 00 00 */	lis r3, __close_all@ha
/* 00000004 00000044  38 03 00 00 */	addi r0, r3, __close_all@l
/* 00000008 00000048  90 00 00 00 */	stw r0, __stdio_exit@sda21(r0)
/* 0000000C 0000004C  4E 80 00 20 */	blr
.endfn __stdio_atexit
