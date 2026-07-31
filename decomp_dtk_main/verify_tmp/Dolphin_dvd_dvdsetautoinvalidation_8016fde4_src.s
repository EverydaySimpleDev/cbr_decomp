.include "macros.inc"
.file "dvdsetautoinvalidation_8016fde4.c"

# 0x00000000 - 0x00000010
.text
.balign 4

.fn DVDSetAutoInvalidation, global
/* 00000000 00000034  80 00 00 00 */	lwz r0, autoInvalidation@sda21(r0)
/* 00000004 00000038  90 60 00 00 */	stw r3, autoInvalidation@sda21(r0)
/* 00000008 0000003C  7C 03 03 78 */	mr r3, r0
/* 0000000C 00000040  4E 80 00 20 */	blr
.endfn DVDSetAutoInvalidation
