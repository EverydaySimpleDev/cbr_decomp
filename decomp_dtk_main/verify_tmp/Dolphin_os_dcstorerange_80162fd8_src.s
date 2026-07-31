.include "macros.inc"
.file "dcstorerange_80162fd8.c"

# 0x00000000 - 0x00000030
.text
.balign 4

.fn DCStoreRange, global
/* 00000000 00000034  28 04 00 00 */	cmplwi r4, 0x0
/* 00000004 00000038  4C 81 00 20 */	blelr
/* 00000008 0000003C  54 65 06 FE */	clrlwi r5, r3, 27
/* 0000000C 00000040  7C 84 2A 14 */	add r4, r4, r5
/* 00000010 00000044  38 84 00 1F */	addi r4, r4, 0x1f
/* 00000014 00000048  54 84 D9 7E */	srwi r4, r4, 5
/* 00000018 0000004C  7C 89 03 A6 */	mtctr r4
.L_0000001C:
/* 0000001C 00000050  7C 00 18 6C */	dcbst r0, r3
/* 00000020 00000054  38 63 00 20 */	addi r3, r3, 0x20
/* 00000024 00000058  42 00 FF F8 */	bdnz .L_0000001C
/* 00000028 0000005C  44 00 00 02 */	sc
/* 0000002C 00000060  4E 80 00 20 */	blr
.endfn DCStoreRange
