#include <types.h>

//8016C640
extern "C" void PSQUATScale(register const void* src, register f32 scale, register void* dst)
{
#ifdef __MWERKS__ // clang-format off
    asm {
        psq_l    f0, 0(src), 0, 0
        psq_l    f2, 8(src), 1, 0
        ps_muls0 f0, f0, scale
        psq_st   f0, 0(dst), 0, 0
        ps_muls0 f0, f2, scale
        psq_st   f0, 8(dst), 1, 0
    }
#endif // clang-format on
}
