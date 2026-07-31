#include <types.h>

extern "C" char lbl_803670CC[0x88];

//80068B98
extern "C" void fn_80068B98(void)
{
    *(int*)(lbl_803670CC + 0x78) = 2;
}
