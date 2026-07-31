#include <types.h>

struct Vec3
{
    f32 x, y, z;
};

//800A2C98
extern "C" ASM void copyVector3(register Vec3* out, register Vec3* in)
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

//800A2CB4
extern "C" int GetNumLeadingZerosInDifference(char* obj, int val)
{
    return *(int*)(obj + 4) - val == 0;
}
