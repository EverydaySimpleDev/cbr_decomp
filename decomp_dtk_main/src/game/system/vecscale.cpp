#include <types.h>

struct CVec3Tagged
{
    f32 x, y, z;
    void* vtable;
};

extern "C" char lbl_80210314[12];

//8002442C
struct RawVec3 { u32 x, y, z; };

extern "C" void scale_vector_by_scalar(CVec3Tagged* out, CVec3Tagged* in, f32 divisor)
{
    RawVec3 tmp = *(RawVec3*)in;
    *(f32*)&tmp.x = *(f32*)&tmp.x / divisor;
    *(f32*)&tmp.y = *(f32*)&tmp.y / divisor;
    *(f32*)&tmp.z = *(f32*)&tmp.z / divisor;
    *(RawVec3*)out = tmp;
    out->vtable = lbl_80210314;
}
