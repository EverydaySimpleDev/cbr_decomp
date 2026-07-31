#include <types.h>

extern void fn_801C3D40(void* node, void* callback, void* arg);

typedef void (*RenderCallback)(void* node, void* arg, int flag);

//801C4084
void RenderChildObjects(void* node, void* callback, void* arg)
{
    void* child;
    if (node == 0)
    {
        return;
    }
    if (callback != 0)
    {
        ((RenderCallback)callback)(node, arg, 0);
    }
    if ((*(u32*)((char*)node + 0x14) & 0x1000) == 0)
    {
        child = *(void**)((char*)node + 0x10);
        while (child != 0)
        {
            fn_801C3D40(child, callback, arg);
            child = *(void**)((char*)child + 0x8);
        }
    }
}
