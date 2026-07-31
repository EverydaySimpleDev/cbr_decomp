.include "macros.inc"
.file "lcstoreblocks_801631e4.c"

# 0x00000000 - 0x00000024
.text
.balign 4

.fn LCStoreBlocks, global
/* 00000000 00000034  54 A6 F6 FE */	extrwi r6, r5, 5, 25
/* 00000004 00000038  54 63 01 3E */	clrlwi r3, r3, 4
/* 00000008 0000003C  7C C6 1B 78 */	or r6, r6, r3
/* 0000000C 00000040  7C DA E3 A6 */	mtspr DMA_U, r6
/* 00000010 00000044  54 A6 17 3A */	clrlslwi r6, r5, 30, 2
/* 00000014 00000048  7C C6 23 78 */	or r6, r6, r4
/* 00000018 0000004C  60 C6 00 02 */	ori r6, r6, 0x2
/* 0000001C 00000050  7C DB E3 A6 */	mtspr DMA_L, r6
/* 00000020 00000054  4E 80 00 20 */	blr
.endfn LCStoreBlocks
