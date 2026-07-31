#include <cfile.h>
#include<types.h>

/*
game/system/cfile.cpp:
	extab       start:0x80005F60 end:0x80005F68
	extabindex  start:0x80006E3C end:0x80006E48
	.text       start:0x8019FCE4 end:0x8019FD08
	.sdata      start:0x8065ABB8 end:0x8065ABC0

*/
//global var
int __OSCurrHeap = 0;//8065abb8
extern "C" void OSAllocFromHeap(int dat);//801626a0 -- local single-arg forward-declare matching this call site's actual register usage, NOT OSAllocFromHeap's real (heap, size) signature; do not "fix" to match Dolphin/OS/OSAlloc.h's declaration, this file is byte-exact matching as-is
void CFile::fn_8019FCE4()//fn_8019FCE4__5CFileFv
{
	OSAllocFromHeap(__OSCurrHeap);
}
