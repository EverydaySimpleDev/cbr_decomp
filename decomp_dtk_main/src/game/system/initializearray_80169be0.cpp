//80169BE0
extern "C" void initialize_array(void* self, int firstValue)
{
    *(int*)((char*)self + 0x0) = firstValue;
    *(int*)((char*)self + 0xC) = 0;
    *(int*)((char*)self + 0x8) = 0;
    *(int*)((char*)self + 0x4) = 0;
    *(int*)((char*)self + 0x14) = -1;
    *(int*)((char*)self + 0x10) = 0;
    *(int*)((char*)self + 0x1C) = 0;
    *(int*)((char*)self + 0x18) = 0;
}
