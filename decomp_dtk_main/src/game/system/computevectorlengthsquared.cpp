#include <types.h>

//8016C6A0
extern "C" asm f32 fn_8016C6A0(register const void* src)
{
    nofralloc
    psq_l    f0, 0(src), 0, 0
    ps_mul   f0, f0, f0
    lfs      f1, 8(src)
    ps_madd  f1, f1, f1, f0
    ps_sum0  f1, f1, f0, f0
    blr
}
