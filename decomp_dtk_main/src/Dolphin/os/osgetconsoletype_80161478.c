// DEFERRED: not byte-exact -- control-flow canonicalization (bnelr fusion).
// See project memory.
typedef struct OSBootInfo {
    char pad[0x2C];
    unsigned long consoleType;
} OSBootInfo;

extern OSBootInfo* BootInfo;

//80161478
unsigned long OSGetConsoleType(void)
{
    unsigned long result;

    if (BootInfo == 0) {
        goto useDefault;
    }
    result = BootInfo->consoleType;
    if (result != 0) {
        goto done;
    }
useDefault:
    result = 0x10000002;
done:
    return result;
}
