.include "macros.inc"
.file "ppcsetfpnonieeemode_8016125c.c"

# 0x00000000 - 0x00000008
.text
.balign 4

.fn PPCSetFpNonIEEEMode, global
/* 00000000 00000034  FF A0 00 4C */	mtfsb1 cr7gt
/* 00000004 00000038  4E 80 00 20 */	blr
.endfn PPCSetFpNonIEEEMode
