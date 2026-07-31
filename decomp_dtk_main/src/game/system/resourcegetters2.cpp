#include <types.h>

extern "C" char lbl_803672CC[0x300];

static inline u32 ReadLE32(void* p)
{
    unsigned char* b = (unsigned char*)p;
    return b[0] + (b[1] << 8) + (b[2] << 16) + ((u32)b[3] << 24);
}

//8006F3BC
extern "C" u32 fn_8006F3BC(void)
{
    return *(u32*)(lbl_803672CC + 0x1a4);
}

//8006F3CC
extern "C" u32 fn_8006F3CC(void)
{
    return *(u32*)(lbl_803672CC + 0x1a0);
}

//8006F3DC
extern "C" u32 fn_8006F3DC(void)
{
    return *(u32*)(lbl_803672CC + 0x19c);
}

//8006F3EC
extern "C" u32 fn_8006F3EC(void)
{
    return *(u32*)(lbl_803672CC + 0x194);
}

//8006F3FC
extern "C" u32 fn_8006F3FC(void)
{
    return *(u32*)(lbl_803672CC + 0x190);
}

//8006F40C
extern "C" u32 fn_8006F40C(void)
{
    return *(u32*)(lbl_803672CC + 0x18c);
}

//8006F41C
extern "C" u32 fn_8006F41C(void)
{
    return *(u32*)(lbl_803672CC + 0x188);
}

//8006F42C
extern "C" u32 fn_8006F42C(void)
{
    return *(u32*)(lbl_803672CC + 0x184);
}

//8006F43C
extern "C" void* fn_8006F43C(int idx)
{
    char* arrayBase = *(char**)(lbl_803672CC + 0x180);
    u32 packed = ReadLE32(arrayBase + idx * 4);
    if (packed == 0) {
        return 0;
    }
    return *(char**)(lbl_803672CC + 0x150) + packed;
}

//8006F490
extern "C" void* fn_8006F490(void)
{
    return *(void**)(lbl_803672CC + 0x150);
}

//8006F4A0
extern "C" void* fn_8006F4A0(int idx)
{
    return *(char**)(lbl_803672CC + 0x178) + idx * 0x38;
}
