.include "macros.inc"
.file "settranslationx.c"

# 0x00000000 - 0x00000020
.text
.balign 4

.fn setTranslationX, global
/* 00000000 00000040  28 03 00 00 */	cmplwi r3, 0x0
/* 00000004 00000044  4D 82 00 20 */	beqlr
/* 00000008 00000048  80 63 00 0C */	lwz r3, 0xc(r3)
/* 0000000C 0000004C  28 03 00 00 */	cmplwi r3, 0x0
/* 00000010 00000050  40 82 00 08 */	bne .L_00000018
/* 00000014 00000054  4E 80 00 20 */	blr
.L_00000018:
/* 00000018 00000058  D0 23 00 0C */	stfs f1, 0xc(r3)
/* 0000001C 0000005C  4E 80 00 20 */	blr
.endfn setTranslationX
