#include <types.h>
#include <Dolphin/vec.h>

extern "C" const f32 lbl_8065F2B0;
extern "C" const f32 lbl_8065F2B4;

//8016C6B8
extern "C" asm f32 computeVectorLength(register const Vec* vec)
{
    nofralloc
    lfs      f4, lbl_8065F2B0
    psq_l    f0, 0(vec), 0, 0
    ps_mul   f0, f0, f0
    lfs      f1, 8(vec)
    fsubs    f2, f4, f4
    ps_madd  f1, f1, f1, f0
    ps_sum0  f1, f1, f0, f0
    fcmpu    cr0, f1, f2
    beq      end
    frsqrte  f0, f1
    lfs      f3, lbl_8065F2B4
    fmuls    f2, f0, f0
    fmuls    f0, f0, f4
    fnmsubs  f2, f2, f1, f3
    fmuls    f0, f2, f0
    fmuls    f1, f1, f0
end:
    opword   0x4E800020
}
