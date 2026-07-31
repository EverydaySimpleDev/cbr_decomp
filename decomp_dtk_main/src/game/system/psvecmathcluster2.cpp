#include <types.h>

//8016C768
extern "C" asm void fn_8016C768(register const void* a, register const void* b, register void* dst)
{
    nofralloc
    psq_l       f1, 0(b), 0, 0
    lfs         f2, 8(a)
    psq_l       f0, 0(a), 0, 0
    ps_merge10  f6, f1, f1
    lfs         f3, 8(b)
    ps_mul      f4, f1, f2
    ps_muls0    f7, f1, f0
    ps_msub     f5, f0, f3, f4
    ps_msub     f8, f0, f6, f7
    ps_merge11  f9, f5, f5
    ps_merge01  f10, f5, f8
    psq_st      f9, 0(dst), 1, 0
    ps_neg      f10, f10
    psq_st      f10, 4(dst), 0, 0
    blr
}
