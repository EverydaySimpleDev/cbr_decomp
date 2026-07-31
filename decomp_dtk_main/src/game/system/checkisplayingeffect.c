#include <types.h>

extern void fn_8009C8E0(void* obj);
extern void UpdateJunkTypeAvailabilityFlags(char* obj);

void CheckIsPlayingEffect(void* obj)
{
    fn_8009C8E0(obj);
    UpdateJunkTypeAvailabilityFlags((char*)obj);
}
