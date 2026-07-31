.include "macros.inc"
.file "osgetconsoletype_80161478.c"

# 0x00000000 - 0x00000024
.text
.balign 4

.fn OSGetConsoleType, global
/* 00000000 00000034  80 60 00 00 */	lwz r3, BootInfo@sda21(r0)
/* 00000004 00000038  28 03 00 00 */	cmplwi r3, 0x0
/* 00000008 0000003C  41 82 00 10 */	beq .L_00000018
/* 0000000C 00000040  80 63 00 2C */	lwz r3, 0x2c(r3)
/* 00000010 00000044  28 03 00 00 */	cmplwi r3, 0x0
/* 00000014 00000048  4C 82 00 20 */	bnelr
.L_00000018:
/* 00000018 0000004C  3C 60 10 00 */	lis r3, 0x1000
/* 0000001C 00000050  38 63 00 02 */	addi r3, r3, 0x2
/* 00000020 00000054  4E 80 00 20 */	blr
.endfn OSGetConsoleType
