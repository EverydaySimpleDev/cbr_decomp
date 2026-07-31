.include "macros.inc"
.file "osallocfromarenalo_80162ca8.c"

# 0x00000000 - 0x0000002C
.text
.balign 4

.fn OSAllocFromArenaLo, global
/* 00000000 00000034  80 00 00 00 */	lwz r0, __OSArenaLo@sda21(r0)
/* 00000004 00000038  38 84 FF FF */	subi r4, r4, 0x1
/* 00000008 0000003C  7C 85 20 F8 */	nor r5, r4, r4
/* 0000000C 00000040  7C 00 22 14 */	add r0, r0, r4
/* 00000010 00000044  7C A6 00 38 */	and r6, r5, r0
/* 00000014 00000048  7C 06 1A 14 */	add r0, r6, r3
/* 00000018 0000004C  7C 00 22 14 */	add r0, r0, r4
/* 0000001C 00000050  7C A0 00 38 */	and r0, r5, r0
/* 00000020 00000054  90 00 00 00 */	stw r0, __OSArenaLo@sda21(r0)
/* 00000024 00000058  7C C3 33 78 */	mr r3, r6
/* 00000028 0000005C  4E 80 00 20 */	blr
.endfn OSAllocFromArenaLo
