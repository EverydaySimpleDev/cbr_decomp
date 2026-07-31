#include <types.h>

//8000A52C
u32 ReturnValue(void* self)
{
    return *(u32*)((char*)self + 0xE7E20);
}

//8000A538
u32 GetFieldAt0x1B0C(void* self)
{
    return *(u32*)((char*)self + 0x1B0C);
}

//8000A540
void* fn_8000A540(void* self)
{
    return (char*)self + 0x1B20;
}

//8000A548
void* fn_8000A548(void* self)
{
    return (char*)self + 0x1CB4;
}

//8000A550
void* fn_8000A550(void* self)
{
    return (char*)self + 0x1E48;
}

//8000A558
void* fn_8000A558(void* self)
{
    return (char*)self + 0x2BA8;
}
