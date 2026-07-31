#include <types.h>
#include <Dolphin/vec.h>

extern "C" const f32 lbl_8065F2B0;
extern "C" const f32 lbl_8065F2B4;

//8016C878
extern "C" asm f32 computeEuclideanDistance(register const Vec* a, register const Vec* b)
{
    nofralloc
    psq_l    f0, 4(a), 0, 0
    psq_l    f1, 4(b), 0, 0
    ps_sub   f2, f0, f1
    psq_l    f0, 0(a), 0, 0
    psq_l    f1, 0(b), 0, 0
    ps_mul   f2, f2, f2
    ps_sub   f0, f0, f1
    lfs      f3, lbl_8065F2B0
    ps_madd  f1, f0, f0, f2
    fsubs    f0, f3, f3
    ps_sum0  f1, f1, f2, f2
    fcmpu    cr0, f0, f1
    beq      end
    lfs      f4, lbl_8065F2B4
    frsqrte  f0, f1
    fmuls    f2, f0, f0
    fmuls    f0, f0, f3
    fnmsubs  f2, f2, f1, f4
    fmuls    f0, f2, f0
    fmuls    f1, f1, f0
end:
    opword   0x4E800020
}
