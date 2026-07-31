.include "macros.inc"
.file "tablelookup_801a4ec8.cpp"

# 0x00000000 - 0x00000010
.text
.balign 4

.fn fn_801A4EC8, global
/* 00000000 00000040  88 04 00 00 */	lbz r0, 0x0(r4)
/* 00000004 00000044  1C 00 00 06 */	mulli r0, r0, 0x6
/* 00000008 00000048  7C 63 02 14 */	add r3, r3, r0
/* 0000000C 0000004C  4E 80 00 20 */	blr
.endfn fn_801A4EC8
