.include "macros.inc"
.file "setglobalfield_80068b98.cpp"

# 0x00000000 - 0x00000014
.text
.balign 4

.fn fn_80068B98, global
/* 00000000 00000040  3C 60 00 00 */	lis r3, lbl_803670CC@ha
/* 00000004 00000044  38 00 00 02 */	li r0, 0x2
/* 00000008 00000048  38 63 00 00 */	addi r3, r3, lbl_803670CC@l
/* 0000000C 0000004C  90 03 00 78 */	stw r0, 0x78(r3)
/* 00000010 00000050  4E 80 00 20 */	blr
.endfn fn_80068B98
