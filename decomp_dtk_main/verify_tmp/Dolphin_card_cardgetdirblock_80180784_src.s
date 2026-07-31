.include "macros.inc"
.file "cardgetdirblock_80180784.c"

# 0x00000000 - 0x00000008
.text
.balign 4

.fn __CARDGetDirBlock, global
/* 00000000 00000034  80 63 00 84 */	lwz r3, 0x84(r3)
/* 00000004 00000038  4E 80 00 20 */	blr
.endfn __CARDGetDirBlock
