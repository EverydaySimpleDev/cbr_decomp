#include <types.h>
#include <Dolphin/os.h>

extern "C" char MainGame[];
extern "C" void fn_80148550(void*);
extern "C" const char lbl_8020AAF8[];
extern "C" const f32 lbl_8065DB38;

#define F32(base, off) (*(f32*)((char*)(base) + (off)))
#define S32(base, off) (*(s32*)((char*)(base) + (off)))
#define U8(base, off) (*(u8*)((char*)(base) + (off)))

// DEFERRED: not byte-exact -- pure register-choice residual
// (unfixable via source restructuring). See project memory.
extern "C" void CCameraActionLeticker_Reset(void* self)
{
    OSReport(lbl_8020AAF8);
    fn_80148550(self);
    F32(self, 0x48) = lbl_8065DB38;
    u32* flag = (u32*)(MainGame + 0x1b14);
    S32(self, 0x50) = 0;
    U8(self, 0x54) = 0;
    *flag |= 0x80;
}
