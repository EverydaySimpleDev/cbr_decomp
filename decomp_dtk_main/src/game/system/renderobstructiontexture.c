#include <types.h>

extern void RenderChildObjects(void* node, void* callback, void* arg);
extern void fn_80091784(void);
extern void* lbl_8065FFB8;
extern u32 lbl_8065FFBC;

struct RenderArg
{
    void* a;
    u32 b;
};

//80091834
void RenderObstructionTexture(void** obj, void* param2, u8 param3)
{
    struct RenderArg local;
    local.a = lbl_8065FFB8;
    local.b = lbl_8065FFBC;
    local.a = param2;
    local.b = param3;
    if (*obj != 0)
    {
        RenderChildObjects(*obj, fn_80091784, &local);
    }
}
