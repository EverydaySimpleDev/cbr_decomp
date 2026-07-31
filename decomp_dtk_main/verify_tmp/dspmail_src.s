.include "macros.inc"
.file "dspmail_8017cd80.c"

# 0x00000000 - 0x0000004C
.text
.balign 4

.fn DSPCheckMailToDSP, global
/* 00000000 00000034  3C 60 CC 00 */	lis r3, 0xcc00
/* 00000004 00000038  A0 03 50 00 */	lhz r0, 0x5000(r3)
/* 00000008 0000003C  54 03 8F FE */	extrwi r3, r0, 1, 16
/* 0000000C 00000040  4E 80 00 20 */	blr
.endfn DSPCheckMailToDSP

.fn DSPCheckMailFromDSP, global
/* 00000010 00000044  3C 60 CC 00 */	lis r3, 0xcc00
/* 00000014 00000048  A0 03 50 04 */	lhz r0, 0x5004(r3)
/* 00000018 0000004C  54 03 8F FE */	extrwi r3, r0, 1, 16
/* 0000001C 00000050  4E 80 00 20 */	blr
.endfn DSPCheckMailFromDSP

.fn DSPReadMailFromDSP, global
/* 00000020 00000054  3C 60 CC 00 */	lis r3, 0xcc00
/* 00000024 00000058  38 63 50 00 */	addi r3, r3, 0x5000
/* 00000028 0000005C  A0 03 00 04 */	lhz r0, 0x4(r3)
/* 0000002C 00000060  A0 63 00 06 */	lhz r3, 0x6(r3)
/* 00000030 00000064  50 03 80 1E */	rlwimi r3, r0, 16, 0, 15
/* 00000034 00000068  4E 80 00 20 */	blr
.endfn DSPReadMailFromDSP

.fn DSPSendMailToDSP, global
/* 00000038 0000006C  3C 80 CC 00 */	lis r4, 0xcc00
/* 0000003C 00000070  54 60 84 3E */	srwi r0, r3, 16
/* 00000040 00000074  B0 04 50 00 */	sth r0, 0x5000(r4)
/* 00000044 00000078  B0 64 50 02 */	sth r3, 0x5002(r4)
/* 00000048 0000007C  4E 80 00 20 */	blr
.endfn DSPSendMailToDSP
