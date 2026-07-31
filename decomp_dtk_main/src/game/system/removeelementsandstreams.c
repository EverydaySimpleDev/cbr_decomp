#include <types.h>

extern const f32 lbl_8065D6A8;
extern char MainGame[];
extern void fn_801A89A0(void* arg);
extern void fn_8001E660(void* arg, int mode);

//800C17BC
void removeElementsAndStreams(void* self)
{
    *(u32*)((char*)self + 0x0) = 0;
    *(f32*)((char*)self + 0x4) = lbl_8065D6A8;

    if (*(u32*)((char*)self + 0x14) != 0)
    {
        fn_801A89A0(MainGame + 0x9114);
        *(u32*)((char*)self + 0x14) = 0;
    }
    if (*(u32*)((char*)self + 0x18) != 0)
    {
        fn_801A89A0(MainGame + 0x9114);
        *(u32*)((char*)self + 0x18) = 0;
    }

    {
        void* ptr = MainGame + 0xE7E24;
        fn_8001E660(ptr, 0x186);
        fn_8001E660(ptr, 0x18b);
    }
}
