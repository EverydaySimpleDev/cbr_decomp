#include <types.h>
#include <Dolphin/os.h>

struct LocalPadInfo
{
    void* padDataPtr;
    void* tag;
};

extern "C" void fn_8019E3C8(LocalPadInfo* out, u8 padIndex);
extern "C" void fn_801482A8(void* self, f32* outXY);
extern "C" void fn_801483C0(void* self, u32 deltaFrames);
extern "C" char MainGame[];
extern "C" const char lbl_8020AA7C[]; // "%4.2f %4.2f\n"
extern "C" const char lbl_8020AA8C[]; // "CCameraActionLeticker::Update %4.2f %4.2f %d\n"
extern "C" const f32 lbl_8065DBC8;    // pi/2
extern "C" const f32 lbl_8065DBD4;    // 180/pi
extern "C" const f32 lbl_8065DC20;    // -5 degrees (radians)
extern "C" const f32 lbl_8065DC24;    // +5 degrees (radians)
extern "C" const f64 lbl_8065DC18;    // 2^52 bias-trick constant
extern "C" char lbl_80210790[];

#define F32(base, off) (*(f32*)((char*)(base) + (off)))
#define S32(base, off) (*(s32*)((char*)(base) + (off)))
#define U8(base, off) (*(u8*)((char*)(base) + (off)))

// DEFERRED: extremely close (1 instruction/4 bytes off in the mask-idiom
// sub-expression only; rest of the function is logically and structurally
// correct). Current best is the single-`volatile zeroMask` form below --
// see project memory before trying to improve on it.
extern "C" void CCameraActionLeticker_Update(void* self, u32 deltaFrames)
{
    LocalPadInfo local;
    fn_8019E3C8(&local, 0);

    volatile u32 zeroMask = 0;
    u32 a = *(u32*)(MainGame + 0x1b10);
    u32 b = *(u32*)(MainGame + 0x1b14);
    u32 am = a & zeroMask;
    u32 bm = b & 0x80000000;
    u32 bx = bm ^ zeroMask;
    u32 ax = am ^ zeroMask;
    u32 mask6 = (bx | ax) ? 1 : 0x400000;
    zeroMask = 0;
    bx = bm ^ zeroMask;
    ax = am ^ zeroMask;
    u32 mask4 = (bx | ax) ? 2 : 0x800000;

    if (S32(self, 0x50) == 0)
    {
        u32 flags = *(u32*)((char*)local.padDataPtr + 0x14);
        if (flags & mask6)
        {
            u8 inBounds;
            if (U8(self, 0x54) == 0)
            {
                inBounds = 1;
            }
            else
            {
                f32 xy[2];
                fn_801482A8(self, xy);
                OSReport(lbl_8020AA7C, xy[0], xy[1]);
                if (xy[0] < F32(self, 0x58) || F32(self, 0x5c) < xy[0] ||
                    xy[1] < F32(self, 0x60) || F32(self, 0x64) < xy[1])
                {
                    OSReport(lbl_8020AA8C, xy[0], xy[1], (int)(lbl_8065DBD4 * F32(self, 0x48)));
                    inBounds = 0;
                }
                else
                {
                    inBounds = 1;
                }
            }
            if (inBounds)
            {
                F32(self, 0x48) -= lbl_8065DBC8;
                F32(self, 0x4c) = lbl_8065DC20;
                S32(self, 0x50) = 0x12;
            }
        }
        else if (flags & mask4)
        {
            u8 inBounds;
            if (U8(self, 0x54) == 0)
            {
                inBounds = 1;
            }
            else
            {
                f32 xy[2];
                fn_801482A8(self, xy);
                OSReport(lbl_8020AA7C, xy[0], xy[1]);
                if (xy[0] < F32(self, 0x58) || F32(self, 0x5c) < xy[0] ||
                    xy[1] < F32(self, 0x60) || F32(self, 0x64) < xy[1])
                {
                    OSReport(lbl_8020AA8C, xy[0], xy[1], (int)(lbl_8065DBD4 * F32(self, 0x48)));
                    inBounds = 0;
                }
                else
                {
                    inBounds = 1;
                }
            }
            if (inBounds)
            {
                F32(self, 0x48) += lbl_8065DBC8;
                F32(self, 0x4c) = lbl_8065DC24;
                S32(self, 0x50) = 0x12;
            }
        }
    }
    else
    {
        S32(self, 0x50) -= deltaFrames;
        if (S32(self, 0x50) <= 0)
        {
            F32(self, 0x40) = F32(self, 0x48);
            S32(self, 0x50) = 0;
        }
        else
        {
            union
            {
                f64 d;
                struct
                {
                    u32 hi, lo;
                } w;
            } bias;
            bias.w.hi = 0x43300000;
            bias.w.lo = deltaFrames;
            f64 biased = bias.d;
            f32 deltaF = (f32)(biased - lbl_8065DC18);
            F32(self, 0x40) += F32(self, 0x4c) * deltaF;
        }
    }

    fn_801483C0(self, deltaFrames);
    local.tag = lbl_80210790;
}
