#include <types.h>

extern "C" void* fn_801D3C30(void* list, void* obj);
extern "C" void fn_801DD248(const char* file, int line, const char* msg);
extern "C" const char lbl_8020F5C4[]; // "object.h"
extern "C" const char lbl_8020F5D0[]; // "HSD_OBJ(o)->ref_count != HSD_OBJ_NOREF"

#define NEXT(n) (*(void**)(n))
#define OWNER(n) (*(void**)((char*)(n) + 4))
#define REFCOUNT(o) (*(u16*)((char*)(o) + 4))

// DEFERRED: not byte-exact -- 1-instruction guard-clause collapse residual
// (control-flow canonicalization). See project memory.
extern "C" void HSD_ShadowAddObject(void* list, void* obj)
{
    if (list != 0)
    {
        if (obj != 0)
        {
            void* node = NEXT(list);
            while (node != 0)
            {
                if (OWNER(node) == obj)
                {
                    return;
                }
                node = NEXT(node);
            }
            NEXT(list) = fn_801D3C30(list, obj);
            if (obj == 0)
            {
                return;
            }
            REFCOUNT(obj)++;
            if (REFCOUNT(obj) == 0xffff)
            {
                fn_801DD248(lbl_8020F5C4, 0x5d, lbl_8020F5D0);
            }
        }
    }
}
