.include "macros.inc"
.file "settranslationx.c"

# 0x00000000 - 0x00000020
.text
.balign 4

.fn setTranslationX, global
/* 00000000 00000034  28 03 00 00 */	cmplwi r3, 0x0
/* 00000004 00000038  4D 82 00 20 */	beqlr
/* 00000008 0000003C  80 63 00 0C */	lwz r3, 0xc(r3)
/* 0000000C 00000040  28 03 00 00 */	cmplwi r3, 0x0
/* 00000010 00000044  40 82 00 08 */	bne .L_00000018
/* 00000014 00000048  4E 80 00 20 */	blr
.L_00000018:
/* 00000018 0000004C  D0 23 00 0C */	stfs f1, 0xc(r3)
/* 0000001C 00000050  4E 80 00 20 */	blr
.endfn setTranslationX
