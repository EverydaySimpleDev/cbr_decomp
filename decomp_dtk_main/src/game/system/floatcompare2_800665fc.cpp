#include <types.h>

extern "C" char MainGame[];
extern "C" f32 lbl_8065C8B8;

//800665FC
extern "C" ASM int fn_800665FC(void* obj)
{
#ifdef __MWERKS__ // clang-format off
    nofralloc
    lis     r4, MainGame@ha
    lfs     f2, 0x1d4(r3)
    addi    r4, r4, MainGame@l
    lfs     f1, lbl_8065C8B8
    addis   r3, r4, 0x1
    lwz     r3, -0x6944(r3)
    addis   r3, r3, 0x1
    lfs     f0, -0x69a4(r3)
    fmuls   f0, f1, f0
    fcmpu   cr0, f2, f0
    mfcr    r0
    extrwi  r3, r0, 1, 2
    blr
#endif // clang-format on
}
