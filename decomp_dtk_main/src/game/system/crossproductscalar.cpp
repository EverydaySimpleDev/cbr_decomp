#include <types.h>

//8016C71C
extern "C" void fn_8016C71C(register const void* a, register const void* b, register void* dst)
{
#ifdef __MWERKS__ // clang-format off
    asm {
        lfs   f1, 8(a)
        lfs   f6, 4(b)
        lfs   f5, 0(b)
        lfs   f7, 4(a)
        fmuls f0, f1, f6
        lfs   f3, 8(b)
        fmuls f4, f1, f5
        lfs   f2, 0(a)
        fmuls f1, f7, f3
        fmuls f3, f2, f3
        fmuls f2, f2, f6
        fsubs f0, f1, f0
        fmuls f1, f7, f5
        fsubs f3, f4, f3
        stfs  f0, 0(dst)
        fsubs f0, f2, f1
        stfs  f3, 4(dst)
        stfs  f0, 8(dst)
    }
#endif // clang-format on
}
