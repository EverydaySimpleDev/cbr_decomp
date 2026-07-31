#include <types.h>

//800B2108
extern "C" int ComputeArrayBasedOffset(char* obj, int idx, int multiplier)
{
    return *(int*)(obj + idx * 0x14 + 0x9694) + multiplier * (*(int*)(obj + idx * 0x14 + 0x96A4));
}

//800B2128
extern "C" int GetValueAtOffset_A860(char* obj)
{
    return *(int*)(obj + 0xA860);
}

//800B2134
extern "C" f32 GetFieldAt0x780(char* obj)
{
    return *(f32*)(obj + 0x780);
}

//800B213C
extern "C" void SetFieldAt0x4_213C(char* obj, int value)
{
    *(int*)(obj + 4) = value;
}

//800B2144
extern "C" void SetGuardedParams_2144(char* obj, void* param1, char* param2)
{
    *(void**)(obj + 0xbac) = param1;
    if (param2 != NULL) {
        *(char**)(obj + 0xbc8) = param2;
        *(int*)(obj + 0xbd0) = *(int*)(param2 + 0x784);
    }
}

//800B2164
extern "C" int IsFlagSetInSystemState_(char* obj)
{
    int mask2 = 0;
    int a = *(int*)(obj + 0x228) & 0x10;
    int b = *(int*)(obj + 0x22c) & mask2;
    b = b ^ mask2;
    a = a ^ mask2;
    return (b | a) != 0;
}

//800B2198
extern "C" void SetGuardedParams_2198(char* obj, void* param1, char* param2)
{
    *(void**)(obj + 0xb68) = param1;
    if (param2 != NULL) {
        *(char**)(obj + 0xb84) = param2;
        *(int*)(obj + 0xb8c) = *(int*)(param2 + 0x784);
    }
}

//800B21B8
extern "C" int IsBit3SetInParameter_(char* obj)
{
    int mask2 = 0;
    int a = *(int*)(obj + 0x228) & 0x8;
    int b = *(int*)(obj + 0x22c) & mask2;
    b = b ^ mask2;
    a = a ^ mask2;
    return (b | a) != 0;
}

//800B21EC
extern "C" void ResetSubsystemState(char* obj)
{
    char* sub = *(char**)(obj + 0xa64);
    if (sub != NULL) {
        *(u32*)(sub + 0x22c) = *(u32*)(sub + 0x22c) & 0xFFFFFFFF;
        *(u32*)(sub + 0x228) = *(u32*)(sub + 0x228) & ~0x04000000u;
        *(void**)(obj + 0xa64) = NULL;
    }
    *(int*)(obj + 0xa48) = 0;
}

//800B2230
extern "C" void SetGuardedParams_2230(char* obj, void* param1, char* param2)
{
    *(void**)(obj + 0xac4) = param1;
    if (param2 != NULL) {
        *(char**)(obj + 0xae0) = param2;
        *(int*)(obj + 0xae8) = *(int*)(param2 + 0x784);
    }
}

//800B2250
extern "C" int IsDataStructureEnabled(char* obj)
{
    int mask2 = 0;
    int a = *(int*)(obj + 0x228) & 0x2;
    int b = *(int*)(obj + 0x22c) & mask2;
    b = b ^ mask2;
    a = a ^ mask2;
    return (b | a) != 0;
}

//800B2284
extern "C" int GetArrayElementAt0x25C(char* obj, int idx)
{
    return *(int*)(obj + idx * 4 + 0x25c);
}

//800B2294
extern "C" int IsFlag0x20SetInParams(char* obj)
{
    int mask2 = 0;
    int a = *(int*)(obj + 0x228) & 0x20;
    int b = *(int*)(obj + 0x22c) & mask2;
    b = b ^ mask2;
    a = a ^ mask2;
    return (b | a) != 0;
}
