#include <types.h>

//80185A18
void SetFieldsAt0xC0x10_80185A18(void* obj, void* a, void* b)
{
    *(void**)((char*)obj + 0xC) = a;
    *(void**)((char*)obj + 0x10) = b;
}
