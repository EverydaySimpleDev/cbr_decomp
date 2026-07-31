.include "macros.inc"
.file "computeeuclideandistance.cpp"

# 0x00000000 - 0x00000054
.text
.balign 4

.fn computeEuclideanDistance, global
/* 00000000 00000040  E0 03 00 04 */	psq_l f0, 0x4(r3), 0, qr0
/* 00000004 00000044  E0 24 00 04 */	psq_l f1, 0x4(r4), 0, qr0
/* 00000008 00000048  10 40 08 28 */	ps_sub f2, f0, f1
/* 0000000C 0000004C  E0 03 00 00 */	psq_l f0, 0x0(r3), 0, qr0
/* 00000010 00000050  E0 24 00 00 */	psq_l f1, 0x0(r4), 0, qr0
/* 00000014 00000054  10 42 00 B2 */	ps_mul f2, f2, f2
/* 00000018 00000058  10 00 08 28 */	ps_sub f0, f0, f1
/* 0000001C 0000005C  C0 60 00 00 */	lfs f3, lbl_8065F2B0@sda21(r0)
/* 00000020 00000060  10 20 10 3A */	ps_madd f1, f0, f0, f2
/* 00000024 00000064  EC 03 18 28 */	fsubs f0, f3, f3
/* 00000028 00000068  10 21 10 94 */	ps_sum0 f1, f1, f2, f2
/* 0000002C 0000006C  FC 00 08 00 */	fcmpu cr0, f0, f1
/* 00000030 00000070  41 82 00 20 */	beq .L_00000050
/* 00000034 00000074  C0 80 00 00 */	lfs f4, lbl_8065F2B4@sda21(r0)
/* 00000038 00000078  FC 00 08 34 */	frsqrte f0, f1
/* 0000003C 0000007C  EC 40 00 32 */	fmuls f2, f0, f0
/* 00000040 00000080  EC 00 00 F2 */	fmuls f0, f0, f3
/* 00000044 00000084  EC 42 20 7C */	fnmsubs f2, f2, f1, f4
/* 00000048 00000088  EC 02 00 32 */	fmuls f0, f2, f0
/* 0000004C 0000008C  EC 21 00 32 */	fmuls f1, f1, f0
.L_00000050:
/* 00000050 00000090  4E 80 00 20 */	blr
.endfn computeEuclideanDistance
