.include "macros.inc"
.file "stubreturn_80015640.cpp"

# 0x00000000 - 0x0000000C
.text
.balign 4

.fn fn_80015638, global
/* 00000000 00000040  38 60 00 01 */	li r3, 0x1
/* 00000004 00000044  4E 80 00 20 */	blr
.endfn fn_80015638

.fn fn_80015640, global
/* 00000008 00000048  4E 80 00 20 */	blr
.endfn fn_80015640
