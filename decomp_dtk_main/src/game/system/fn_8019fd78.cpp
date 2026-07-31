//8019FD78
extern "C" void fn_8019FD78(void* unused1, void* self, void* unused2, int flag)
{
    int* field = *(int**)((char*)self + 0x2C);
    if (flag) {
        *field = -2;
    } else {
        *field = 0;
    }
}
