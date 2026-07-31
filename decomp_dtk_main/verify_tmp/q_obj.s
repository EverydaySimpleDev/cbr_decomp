.include "macros.inc"
.file "floatcompare2_800665fc.cpp"

# 0x00000000 - 0x00000034
.text
.balign 4

.fn fn_800665FC, global
/* 00000000 00000040  3C 80 00 00 */	lis r4, MainGame@ha
/* 00000004 00000044  C0 43 01 D4 */	lfs f2, 0x1d4(r3)
/* 00000008 00000048  38 84 00 00 */	addi r4, r4, MainGame@l
/* 0000000C 0000004C  C0 20 00 00 */	lfs f1, lbl_8065C8B8@sda21(r0)
/* 00000010 00000050  3C 64 00 01 */	addis r3, r4, 0x1
/* 00000014 00000054  80 63 96 BC */	lwz r3, -0x6944(r3)
/* 00000018 00000058  3C 63 00 01 */	addis r3, r3, 0x1
/* 0000001C 0000005C  C0 03 96 5C */	lfs f0, -0x69a4(r3)
/* 00000020 00000060  EC 01 00 32 */	fmuls f0, f1, f0
/* 00000024 00000064  FC 02 00 00 */	fcmpu cr0, f2, f0
/* 00000028 00000068  7C 00 00 26 */	mfcr r0
/* 0000002C 0000006C  54 03 1F FE */	extrwi r3, r0, 1, 2
/* 00000030 00000070  4E 80 00 20 */	blr
.endfn fn_800665FC
