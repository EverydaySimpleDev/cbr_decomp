#include <types.h>

//8000F92C
void SetVec3FieldsAt0xA4(void* self, f32 x, f32 y, f32 z)
{
    *(f32*)((char*)self + 0xA4) = x;
    *(f32*)((char*)self + 0xA8) = y;
    *(f32*)((char*)self + 0xAC) = z;
}
