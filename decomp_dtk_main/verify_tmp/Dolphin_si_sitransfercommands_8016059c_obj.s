.include "macros.inc"
.file "sitransfercommands_8016059c.c"

# 0x00000000 - 0x00000010
.text
.balign 4

.fn SITransferCommands, global
/* 00000000 00000040  3C 60 CC 00 */	lis r3, 0xcc00
/* 00000004 00000044  3C 00 80 00 */	lis r0, 0x8000
/* 00000008 00000048  90 03 64 38 */	stw r0, 0x6438(r3)
/* 0000000C 0000004C  4E 80 00 20 */	blr
.endfn SITransferCommands
