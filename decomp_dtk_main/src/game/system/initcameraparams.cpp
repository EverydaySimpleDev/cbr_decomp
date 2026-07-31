#include <types.h>

extern "C" f32 lbl_8065C8B0; // 0.0f
extern "C" f32 lbl_8065C8B4; // 1.0f
extern "C" f32 lbl_8065CA10; // 1.4f
extern "C" f32 lbl_8065A368; // global written at the end
extern "C" char lbl_80366E58[0x308];
extern "C" char lbl_802015B0[0x174];

extern "C" void InitializeCameraData(void* cam, int id);

#define F32(base, off) (*(f32*)((char*)(base) + (off)))
#define S32(base, off) (*(s32*)((char*)(base) + (off)))
#define U8(base, off) (*(u8*)((char*)(base) + (off)))

//8006D5A4
extern "C" void InitializeCameraParameters(void* obj)
{
    F32(obj, 0xa8) = lbl_8065C8B0;
    F32(obj, 0xac) = lbl_8065C8B0;
    F32(obj, 0xb0) = lbl_8065C8B0;
    F32(obj, 0x140) = lbl_8065C8B0;
    F32(obj, 0x144) = lbl_8065C8B0;
    S32(obj, 0x98) = 0;
    S32(obj, 0x9c) = 0;
    S32(obj, 0xa0) = 0;
    S32(obj, 0xa4) = 0;
    S32(obj, 0xb4) = 0;
    F32(obj, 0x1d4) = lbl_8065C8B0;
    S32(obj, 0xb8) = 0;
    S32(obj, 0x17c) = 0;
    S32(obj, 0x180) = 0;

    char* base = lbl_80366E58;
    char* table = lbl_802015B0;

    InitializeCameraData(base + 0x1e0, 0x9a);
    InitializeCameraData(base + 0x14c, 0x98);
    InitializeCameraData(base + 0x274, 0x99);

    U8(base + 0x1e0, 0x74) = 0;
    U8(base + 0x14c, 0x74) = 0;
    U8(base + 0x274, 0x74) = 0;

    S32(obj, 0xbc) = 0;
    F32(obj, 0xc0) = lbl_8065C8B0;
    F32(obj, 0xc4) = lbl_8065C8B0;
    F32(obj, 0xc8) = lbl_8065C8B0;

    struct Vec3 { f32 x, y, z; };
    Vec3 t1 = *(Vec3*)(table + 0x78);
    F32(obj, 0x128) = t1.x;
    F32(obj, 0x12c) = t1.y;
    F32(obj, 0x130) = t1.z;

    S32(obj, 0x148) = 0;
    F32(obj, 0x14c) = lbl_8065C8B0;
    S32(obj, 0x150) = 0;
    S32(obj, 0x154) = 0;
    U8(obj, 0x158) = 0;

    Vec3 t2 = *(Vec3*)(table + 0x84);
    F32(obj, 0x170) = t2.x;
    F32(obj, 0x174) = t2.y;
    F32(obj, 0x178) = t2.z;

    F32(obj, 0x16c) = lbl_8065C8B4;
    S32(obj, 0x188) = 0;
    F32(obj, 0x18c) = lbl_8065C8B0;

    Vec3 t3 = *(Vec3*)(table + 0x90);
    F32(obj, 0x190) = t3.x;
    F32(obj, 0x194) = t3.y;
    F32(obj, 0x198) = t3.z;

    S32(obj, 0x19c) = 0;
    S32(obj, 0x1a0) = 0;
    F32(obj, 0x1a4) = lbl_8065C8B0;

    Vec3 t4 = *(Vec3*)(table + 0x9c);
    F32(obj, 0x1a8) = t4.x;
    F32(obj, 0x1ac) = t4.y;
    F32(obj, 0x1b0) = t4.z;

    S32(obj, 0x1b4) = 0;
    F32(obj, 0x1b8) = lbl_8065C8B0;
    F32(obj, 0x1bc) = lbl_8065C8B0;
    U8(obj, 0x1c0) = 0;
    S32(obj, 0x1c4) = 0;
    F32(obj, 0x1c8) = lbl_8065C8B0;
    F32(obj, 0x1cc) = lbl_8065C8B0;
    S32(obj, 0x184) = 0;
    S32(obj, 0x1d0) = 0;

    F32(obj, 0xcc) = lbl_8065C8B0;
    F32(obj, 0xd0) = lbl_8065C8B0;
    S32(obj, 0xd4) = 0;
    S32(obj, 0xd8) = 0;
    F32(obj, 0xdc) = lbl_8065CA10;
    F32(obj, 0xe0) = lbl_8065C8B0;

    S32(obj, 0xf0) = 0;
    U8(obj, 0x100) = 0;
    F32(obj, 0x104) = F32(obj, 0xcc) - F32(obj, 0xd0);
    F32(obj, 0x114) = lbl_8065C8B0;

    F32(obj, 0xe4) = lbl_8065C8B0;
    S32(obj, 0xf4) = 0;
    U8(obj, 0x101) = 0;
    F32(obj, 0x108) = F32(obj, 0xcc) - F32(obj, 0xd0);
    F32(obj, 0x118) = lbl_8065C8B0;

    F32(obj, 0xe8) = lbl_8065C8B0;
    S32(obj, 0xf8) = 0;
    U8(obj, 0x102) = 0;
    F32(obj, 0x10c) = F32(obj, 0xcc) - F32(obj, 0xd0);
    F32(obj, 0x11c) = lbl_8065C8B0;

    F32(obj, 0xec) = lbl_8065C8B0;
    S32(obj, 0xfc) = 0;
    U8(obj, 0x103) = 0;
    F32(obj, 0x110) = F32(obj, 0xcc) - F32(obj, 0xd0);
    F32(obj, 0x120) = lbl_8065C8B0;

    U8(obj, 0x124) = 0;
    U8(obj, 0x134) = 0;
    F32(obj, 0x138) = lbl_8065C8B0;
    F32(obj, 0x13c) = lbl_8065C8B0;

    lbl_8065A368 = lbl_8065C8B4;

    S32(obj, 0x164) = 5;
}
