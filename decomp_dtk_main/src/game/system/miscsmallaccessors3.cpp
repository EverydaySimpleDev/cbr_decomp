#include <types.h>

typedef unsigned char BOOL8;

extern "C" f64 __frsqrte(f64);
extern "C" f32 lbl_8065AB80;
extern "C" f64 lbl_8065D588;
extern "C" u32 get_4_byte_int_from_memory(int idx);
extern "C" f64 lbl_8065D398;
extern "C" f32 lbl_8065D484;
extern "C" const f64 lbl_8065D578;
extern "C" const f64 lbl_8065D580;

typedef union
{
    struct
    {
        u32 hi, lo;
    } parts;
    f64 d;
} DoubleBits;

static f32 NormalizeMemoryIntAt(int idx)
{
    u32 raw = get_4_byte_int_from_memory(idx);
    DoubleBits u;
    u.parts.hi = 0x43300000;
    u.parts.lo = raw ^ 0x80000000;
    f64 val = u.d - lbl_8065D398;
    return (f32)(val / lbl_8065D484);
}

//800B22C8
extern "C" void SetFieldAt0x4_22C8(char* obj, int value)
{
    *(int*)(obj + 4) = value;
}

//800B22D0
extern "C" int IsFieldOrOffset298NonZero(char* obj)
{
    return (*(int*)(obj + 0x0) != 0) || (*(int*)(obj + 0x298) != 0);
}

//800B22F8
extern "C" f32 GetNormalizedMemoryIntAt2(void)
{
    return NormalizeMemoryIntAt(2);
}

//800B2340
extern "C" f32 GetNormalizedMemoryIntAt1(void)
{
    return NormalizeMemoryIntAt(1);
}

//800B2388
extern "C" void SetFieldAt0x14(char* obj, f32 value)
{
    *(f32*)(obj + 0x14) = value;
}

//800B2390
extern "C" int gdev_cc_shutdown_8(void)
{
    return 1;
}

//800B2398
extern "C" f32 SqrtWithNaNFallback(f32 x)
{
    if (x > 0.0f) {
        const f64& _half = lbl_8065D578;
        const f64& _three = lbl_8065D580;
        f64 guess = __frsqrte((f64)x);
        guess = _half * guess * (_three - guess * guess * x);
        guess = _half * guess * (_three - guess * guess * x);
        guess = _half * guess * (_three - guess * guess * x);
        return (f32)(x * guess);
    }

    if (x < lbl_8065D588) {
        return lbl_8065AB80;
    }

    u32 bits = *(u32*)&x;
    u32 expField = bits & 0x7F800000;
    int cls;
    if (expField == 0x7F800000) {
        cls = (bits & 0x7FFFFF) == 0 ? 2 : 1;
    } else if (expField >= 0x7F800000) {
        cls = 4;
    } else if (expField == 0) {
        cls = (bits & 0x7FFFFF) == 0 ? 3 : 5;
    } else {
        cls = 4;
    }

    if (cls == 1) {
        return lbl_8065AB80;
    }
    return x;
}
