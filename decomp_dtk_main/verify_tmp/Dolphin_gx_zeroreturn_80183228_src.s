.include "macros.inc"
.file "zeroreturn_80183228.c"

# 0x00000000 - 0x00000008
.text
.balign 4

.fn fn_80183228, global
/* 00000000 00000034  38 60 00 00 */	li r3, 0x0
/* 00000004 00000038  4E 80 00 20 */	blr
.endfn fn_80183228
