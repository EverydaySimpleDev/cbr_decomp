.include "macros.inc"
.file "getfieldat0x80c.c"

# 0x00000000 - 0x00000008
.text
.balign 4

.fn fn_80025A98, global
/* 00000000 00000034  80 63 08 0C */	lwz r3, 0x80c(r3)
/* 00000004 00000038  4E 80 00 20 */	blr
.endfn fn_80025A98
