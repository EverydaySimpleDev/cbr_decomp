//801908E0
extern "C" void* getObjectFromId(void* self)
{
    return self ? *(void**)((char*)self + 0x8) : 0;
}
