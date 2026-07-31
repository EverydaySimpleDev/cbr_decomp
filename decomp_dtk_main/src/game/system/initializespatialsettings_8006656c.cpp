#include <types.h>

extern "C" f32 lbl_8065C8B0;
extern "C" f32 lbl_8065C8B4;
extern "C" f32 lbl_8065C8B8;

//8006656C
extern "C" ASM void InitializeSpatialSettings(void* self, f32 param)
{
#ifdef __MWERKS__ // clang-format off
    nofralloc
    lfs     f3, lbl_8065C8B4
    li      r0, 0
    lfs     f0, lbl_8065C8B8
    stfs    f3, 0xe0(r3)
    lfs     f2, lbl_8065C8B0
    fmuls   f0, f0, f1
    stb     r0, 0x100(r3)
    stfs    f2, 0x104(r3)
    stfs    f2, 0x114(r3)
    stfs    f3, 0xe4(r3)
    stb     r0, 0x101(r3)
    stfs    f2, 0x108(r3)
    stfs    f2, 0x118(r3)
    stfs    f3, 0xe8(r3)
    stb     r0, 0x102(r3)
    stfs    f2, 0x10c(r3)
    stfs    f2, 0x11c(r3)
    stfs    f3, 0xec(r3)
    stb     r0, 0x103(r3)
    stfs    f2, 0x110(r3)
    stfs    f2, 0x120(r3)
    stfs    f3, 0xf0(r3)
    stb     r0, 0x104(r3)
    stfs    f2, 0x114(r3)
    stfs    f2, 0x124(r3)
    stfs    f0, 0xd0(r3)
    lfs     f0, 0xd0(r3)
    stfs    f0, 0xcc(r3)
    blr
#endif // clang-format on
}
