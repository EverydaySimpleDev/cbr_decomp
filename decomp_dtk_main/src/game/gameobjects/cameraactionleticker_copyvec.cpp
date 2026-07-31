#include <types.h>

struct RawVec3
{
    u32 w[3];
};

extern "C" void CCameraActionLeticker_CopyVec(void* self, void* param)
{
    RawVec3* src = *(RawVec3**)((char*)param + 0x44);
    *(RawVec3*)self = *src;
}
