#include <types.h>

typedef int (*Callback)(void*, void*, void*, void*);

extern void fn_801D9758(void* arg);
extern void fn_801D6C20(void* arg, int a, int b);
extern void* lbl_8065B9A4;
extern void* lbl_8065B9A0;
extern void fn_801AF354(void* list);
extern void fn_801D94B0(int a, void* b, void* c);

//801BA030
void processDataForQueue(void* self)
{
    void** slot = 0;
    void* tmp8;

    if (self == 0)
    {
        return;
    }

    if (*(void**)((char*)self + 0x18) != 0)
    {
        fn_801D9758(*(void**)((char*)self + 0x18));
        *(void**)((char*)self + 0x18) = 0;
    }
    if (*(void**)((char*)self + 0x1c) != 0)
    {
        fn_801D6C20(*(void**)((char*)self + 0x1c), 7, 1);
        *(void**)((char*)self + 0x1c) = 0;
    }

    tmp8 = *(void**)((char*)self + 0x8);
    if (*(u32*)((char*)self + 0x4) & 0x04000000)
    {
        void* g = lbl_8065B9A4;
        if (g != 0)
        {
            slot = &tmp8;
            while (*slot != 0)
            {
                slot = (void**)((char*)*slot + 8);
            }
            *slot = g;
        }
    }

    if (*(u32*)((char*)self + 0x4) & 0x1000)
    {
        void* d = lbl_8065B9A0;
        if (d != 0 && *(void**)((char*)d + 0x58) != 0)
        {
            *(void**)((char*)d + 0x8) = tmp8;
            tmp8 = lbl_8065B9A0;
        }
    }
    fn_801AF354(tmp8);

    {
        void* v0 = *(void**)((char*)self + 0x0);
        Callback cb = *(Callback*)((char*)v0 + 0x44);
        int result = cb(self, tmp8, (char*)self + 0x1c, v0);
        fn_801D94B0(result, (char*)self + 0x18, (char*)self + 0x1c);
    }

    if (slot != 0)
    {
        *slot = 0;
    }
}
