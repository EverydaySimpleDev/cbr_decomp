#include <types.h>

struct Vec3
{
    f32 x, y, z;
};

//800A2CC8
ASM void copyVector3_2(register struct Vec3* out, register struct Vec3* in)
{
    nofralloc
    lfs      f0, 0x0(in)
    lfs      f1, 0x4(in)
    stfs     f0, 0x0(out)
    lfs      f0, 0x8(in)
    stfs     f1, 0x4(out)
    stfs     f0, 0x8(out)
    blr
}
