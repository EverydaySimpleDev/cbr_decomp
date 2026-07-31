.include "macros.inc"
.file "getvalueatoffset_801c7040.cpp"

# 0x00000000 - 0x00000018
.text
.balign 4

.fn GetValueAtOffset_14, global
/* 00000000 00000034  28 03 00 00 */	cmplwi r3, 0x0
/* 00000004 00000038  41 82 00 0C */	beq .L_00000010
/* 00000008 0000003C  80 63 00 14 */	lwz r3, 0x14(r3)
/* 0000000C 00000040  4E 80 00 20 */	blr
.L_00000010:
/* 00000010 00000044  38 60 00 00 */	li r3, 0x0
/* 00000014 00000048  4E 80 00 20 */	blr
.endfn GetValueAtOffset_14
