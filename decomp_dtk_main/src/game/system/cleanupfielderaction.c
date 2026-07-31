#include <types.h>

typedef void (*Callback)(void*);

typedef struct DispatchTable
{
    char pad[0x18];
    Callback fn18;
} DispatchTable;

typedef struct HasDispatch
{
    char pad[0xc4];
    DispatchTable* table;
} HasDispatch;

extern void fn_801C4704(void* arg);
extern void fn_801C6CD8(void* arg);

//801A13F0
void cleanupFielderAction(void* self)
{
    void* obj = *(void**)((char*)self + 0x1e8);
    if (obj != 0)
    {
        if (obj != 0)
        {
            fn_801C4704(obj);
            obj = *(void**)((char*)self + 0x1e8);
            fn_801C6CD8(obj);
            *(u32*)((char*)self + 0x1e8) = 0;
        }
        {
            void* other = *(void**)((char*)self + 0x48);
            if (other != 0)
            {
                s32 count = *(s32*)((char*)other + 0x130);
                if (count > 0)
                {
                    *(s32*)((char*)other + 0x130) = count - 1;
                }
            }
        }
    }
    {
        void* obj2 = *(void**)((char*)self + 0);
        if (obj2 != 0)
        {
            fn_801C4704(obj2);
            obj2 = *(void**)((char*)self + 0);
            fn_801C6CD8(obj2);
            *(u32*)((char*)self + 0) = 0;
        }
    }
    ((HasDispatch*)self)->table->fn18((char*)self + 0x48);
    *(u32*)((char*)self + 0x3c) = 0;
}
