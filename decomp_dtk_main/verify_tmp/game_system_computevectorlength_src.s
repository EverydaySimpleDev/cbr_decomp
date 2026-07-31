.include "macros.inc"
.file "computevectorlength.cpp"

# 0x00000000 - 0x00000044
.text
.balign 4

.fn computeVectorLength, global
/* 00000000 00000034  C0 80 00 00 */	lfs f4, lbl_8065F2B0@sda21(r0)
/* 00000004 00000038  E0 03 00 00 */	psq_l f0, 0x0(r3), 0, qr0
/* 00000008 0000003C  10 00 00 32 */	ps_mul f0, f0, f0
/* 0000000C 00000040  C0 23 00 08 */	lfs f1, 0x8(r3)
/* 00000010 00000044  EC 44 20 28 */	fsubs f2, f4, f4
/* 00000014 00000048  10 21 00 7A */	ps_madd f1, f1, f1, f0
/* 00000018 0000004C  10 21 00 14 */	ps_sum0 f1, f1, f0, f0
/* 0000001C 00000050  FC 01 10 00 */	fcmpu cr0, f1, f2
/* 00000020 00000054  41 82 00 20 */	beq .L_00000040
/* 00000024 00000058  FC 00 08 34 */	frsqrte f0, f1
/* 00000028 0000005C  C0 60 00 00 */	lfs f3, lbl_8065F2B4@sda21(r0)
/* 0000002C 00000060  EC 40 00 32 */	fmuls f2, f0, f0
/* 00000030 00000064  EC 00 01 32 */	fmuls f0, f0, f4
/* 00000034 00000068  EC 42 18 7C */	fnmsubs f2, f2, f1, f3
/* 00000038 0000006C  EC 02 00 32 */	fmuls f0, f2, f0
/* 0000003C 00000070  EC 21 00 32 */	fmuls f1, f1, f0
.L_00000040:
/* 00000040 00000074  4E 80 00 20 */	blr
.endfn computeVectorLength
