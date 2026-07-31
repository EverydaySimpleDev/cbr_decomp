#include <types.h>

typedef void (*Callback)(void*);

extern void fn_80167EBC(void* arg);
extern void fn_80191D00(void* arg, int mode);

//801A923C
void closeAndCleanupDataStructures(void* self)
{
    void* obj = *(void**)((char*)self + 0x138);
    int hasObj = obj != 0;
    if (hasObj)
    {
        if (hasObj)
        {
            Callback cb = *(Callback*)((char*)obj + 0x38);
            cb(obj);
        }
        obj = *(void**)((char*)self + 0x138);
        fn_80167EBC(obj);
        if (*(void**)((char*)self + 0x13c) != 0)
        {
            fn_80191D00(*(void**)((char*)self + 0x13c), 1);
        }
        {
            u32 table = *(u32*)((char*)self + 0x134);
            Callback cb2 = *(Callback*)(table + 0x20);
            cb2((char*)self + 0x4c);
        }
        *(u32*)((char*)self + 0x138) = 0;
        *(u32*)((char*)self + 0x13c) = 0;
    }
}
