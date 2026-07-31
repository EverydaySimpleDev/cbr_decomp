.include "macros.inc"
.file "PPCArch2.c"

# 0x00000000 - 0x00000044
.text
.balign 4

.fn PPCHalt, weak
/* 00000000 00000034  7C 00 04 AC */	sync
.L_00000004:
/* 00000004 00000038  60 00 00 00 */	nop
/* 00000008 0000003C  38 60 00 00 */	li r3, 0x0
/* 0000000C 00000040  60 00 00 00 */	nop
/* 00000010 00000044  4B FF FF F4 */	b .L_00000004
.endfn PPCHalt

.fn PPCMtmmcr0, global
/* 00000014 00000048  7C 78 EB A6 */	mtspr MMCR0, r3
/* 00000018 0000004C  4E 80 00 20 */	blr
.endfn PPCMtmmcr0

.fn PPCMtmmcr1, global
/* 0000001C 00000050  7C 7C EB A6 */	mtspr MMCR1, r3
/* 00000020 00000054  4E 80 00 20 */	blr
.endfn PPCMtmmcr1

.fn PPCMtpmc1, global
/* 00000024 00000058  7C 79 EB A6 */	mtspr PMC1, r3
/* 00000028 0000005C  4E 80 00 20 */	blr
.endfn PPCMtpmc1

.fn PPCMtpmc2, global
/* 0000002C 00000060  7C 7A EB A6 */	mtspr PMC2, r3
/* 00000030 00000064  4E 80 00 20 */	blr
.endfn PPCMtpmc2

.fn PPCMtpmc3, global
/* 00000034 00000068  7C 7D EB A6 */	mtspr PMC3, r3
/* 00000038 0000006C  4E 80 00 20 */	blr
.endfn PPCMtpmc3

.fn PPCMtpmc4, global
/* 0000003C 00000070  7C 7E EB A6 */	mtspr PMC4, r3
/* 00000040 00000074  4E 80 00 20 */	blr
.endfn PPCMtpmc4
