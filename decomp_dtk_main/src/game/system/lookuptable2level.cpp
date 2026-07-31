#include <types.h>

extern "C" char MainGame[];
extern "C" void* lbl_802246EC[7];

//8006DBC8
extern "C" u32 fn_8006DBC8(int idx)
{
    u8 byteIdx = *(u8*)(MainGame + 0x3318);
    void** table = (void**)lbl_802246EC[byteIdx];
    return *(u32*)(table + idx);
}
