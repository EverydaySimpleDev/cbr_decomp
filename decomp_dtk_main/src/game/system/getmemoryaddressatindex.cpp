#include <types.h>

extern "C" char lbl_803675CC[0x104];

//8006DCFC
extern "C" int GetMemoryAddressAtIndex(int idx)
{
    char* base = *(char**)(lbl_803675CC + 0xf0);
    u8 b4e = *(u8*)(base + 0x4e);
    u8 b4d = *(u8*)(base + 0x4d);
    u8 b4f = *(u8*)(base + 0x4f);
    u8 b4c = *(u8*)(base + 0x4c);
    u32 packed = (b4d << 8) + (b4e << 16) + (b4f << 24);
    char* addr = base + packed + 8 + idx * 0xc;
    return *(int*)(addr + b4c);
}
