.include "macros.inc"
.file "exigetstate_8015efb0.c"

# 0x00000000 - 0x00000018
.text
.balign 4

.fn EXIGetState, global
/* 00000000 00000034  54 64 30 32 */	slwi r4, r3, 6
/* 00000004 00000038  3C 60 00 00 */	lis r3, Ecb@ha
/* 00000008 0000003C  38 03 00 00 */	addi r0, r3, Ecb@l
/* 0000000C 00000040  7C 60 22 14 */	add r3, r0, r4
/* 00000010 00000044  80 63 00 0C */	lwz r3, 0xc(r3)
/* 00000014 00000048  4E 80 00 20 */	blr
.endfn EXIGetState
