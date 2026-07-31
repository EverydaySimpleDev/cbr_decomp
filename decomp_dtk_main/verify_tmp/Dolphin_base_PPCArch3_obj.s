.include "macros.inc"
.file "PPCArch3.c"

# 0x00000000 - 0x00000018
.text
.balign 4

.fn PPCMfhid2, global
/* 00000000 00000040  7C 78 E2 A6 */	mfspr r3, HID2
/* 00000004 00000044  4E 80 00 20 */	blr
.endfn PPCMfhid2

.fn PPCMthid2, global
/* 00000008 00000048  7C 78 E3 A6 */	mtspr HID2, r3
/* 0000000C 0000004C  4E 80 00 20 */	blr
.endfn PPCMthid2

.fn PPCMtwpar, global
/* 00000010 00000050  7C 79 E3 A6 */	mtspr WPAR, r3
/* 00000014 00000054  4E 80 00 20 */	blr
.endfn PPCMtwpar
