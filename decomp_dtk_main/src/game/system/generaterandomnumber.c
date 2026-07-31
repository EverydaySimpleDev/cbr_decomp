#include <types.h>

extern u32 lbl_8065AB70;

u32 generateRandomNumber(void)
{
    lbl_8065AB70 = lbl_8065AB70 * 0x41c64e6d + 0x3039;
    return (lbl_8065AB70 >> 16) & 0x7fff;
}
