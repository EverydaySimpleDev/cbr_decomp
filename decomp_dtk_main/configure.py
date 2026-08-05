#!/usr/bin/env python3

###
# Generates build files for the project.
# This file also includes the project configuration,
# such as compiler flags and the object matching status.
#
# Usage:
#   python3 configure.py
#   ninja
#
# Append --help to see available options.
###

import sys
import argparse


from pathlib import Path
from tools.project import (
    Object,
    ProjectConfig,
    calculate_progress,
    generate_build,
    is_windows,
)

# Game versions
DEFAULT_VERSION = 0
VERSIONS = [
    "GGTE01",	# 0
]

if len(VERSIONS) > 1:
    versions_str = ", ".join(VERSIONS[:-1]) + f" or {VERSIONS[-1]}"
else:
    versions_str = VERSIONS[0]

parser = argparse.ArgumentParser()
parser.add_argument(
    "mode",
    default="configure",
    help="configure or progress (default: configure)",
    nargs="?",
)
parser.add_argument(
    "--version",
    dest="version",
    default=VERSIONS[DEFAULT_VERSION],
    help=f"version to build ({versions_str})",
)
parser.add_argument(
    "--build-dir",
    dest="build_dir",
    type=Path,
    default=Path("build"),
    help="base build directory (default: build)",
)
parser.add_argument(
    "--compilers",
    dest="compilers",
    type=Path,
    help="path to compilers (optional)",
)
parser.add_argument(
    "--map",
    dest="map",
    action="store_true",
    help="generate map file(s)",
)
parser.add_argument(
    "--debug",
    dest="debug",
    action="store_true",
    help="build with debug info (non-matching)",
)
if not is_windows():
    parser.add_argument(
        "--wrapper",
        dest="wrapper",
        type=Path,
        help="path to wibo or wine (optional)",
    )
parser.add_argument(
    "--build-dtk",
    dest="build_dtk",
    type=Path,
    help="path to decomp-toolkit source (optional)",
)
parser.add_argument(
    "--sjiswrap",
    dest="sjiswrap",
    type=Path,
    help="path to sjiswrap.exe (optional)",
)
parser.add_argument(
    "--verbose",
    dest="verbose",
    action="store_true",
    help="print verbose output",
)
args = parser.parse_args()

config = ProjectConfig()
config.version = args.version.upper()
if config.version not in VERSIONS:
    sys.exit(f"Invalid version '{config.version}', expected {versions_str}")
version_num = VERSIONS.index(config.version)

# Apply arguments
config.build_dir = args.build_dir
config.build_dtk_path = args.build_dtk
config.compilers_path = args.compilers
config.debug = args.debug
config.generate_map = args.map
config.sjiswrap_path = args.sjiswrap
if not is_windows():
    config.wrapper = args.wrapper

# Tool versions
config.compilers_tag = "20231018"
config.dtk_tag = "v0.6.2"
config.sjiswrap_tag = "v1.1.1"
config.wibo_tag = "0.6.9"
config.asflags = [
    "-mgekko",
    "--strip-local-absolute",
    "-I include",
    f"-I build/{config.version}/include",
    f"--defsym version={version_num}",
]


# Project
config.config_path = Path("config") / config.version / "config.yml"
config.check_sha_path = Path("config") / config.version / "build.sha1"
config.ldflags = [
    "-fp hardware",
    "-nodefaults",
    # "-listclosure", # Uncomment for Wii linkers
]

# Base flags, common to most GC/Wii games.
# Generally leave untouched, with overrides added below.
cflags_base = [
    "-nodefaults",
    "-proc gekko",
    "-align powerpc",
    "-enum int",
    "-fp hardware",
    "-Cpp_exceptions off",
    "-use_lmw_stmw on",
    # "-W all",
    "-O4,p",
    "-inline auto",
    '-pragma "cats off"',
    '-pragma "warn_notinlined off"',
    "-maxerrors 1",
    "-nosyspath",
    "-RTTI on",
    "-char signed",
    "-fp_contract on",
    "-str reuse",
	"-multibyte", # For Wii compilers, replace with `-enc SJIS`
    "-i include",
    "-i src/sysdolphin/baselib",
    "-i src/sysdolphin",
    f"-i build/{config.version}/include",
    "-multibyte",
    f"-DVERSION={version_num}",
]

# Debug flags
if config.debug:
    cflags_base.extend(["-sym on", "-DDEBUG=1"])
else:
    cflags_base.append("-DNDEBUG=1")

# Metrowerks library flags
cflags_runtime = [
    *cflags_base,
    "-use_lmw_stmw on",
    "-str reuse,pool,readonly",
    "-gccinc",
    "-common off",
	"-inline auto",
]
# Metrowerks library flags
cflags_trk = [
    *cflags_base,
    "-use_lmw_stmw on",
    "-str reuse,readonly",
    "-common off",
    "-sdata 0",
    "-sdata2 0",
    "-inline auto,deferred",
    "-sdatathreshold 0"
]
# Metrowerks library asm flags
cflags_asm = [
    "-mgekko",
    "--strip-local-absolute",
    "-I include",
    f"-I build/{config.version}/include",
    f"--defsym version={version_num}",
]


# REL flags
cflags_rel = [
    *cflags_base,
    "-sdata 0",
    "-sdata2 0",
]

config.linker_version = "GC/1.3.2"


# Helper function for Dolphin libraries
def DolphinLib(lib_name, objects):
    return {
        "lib": lib_name,
        "mw_version": "GC/1.3.2",
        "cflags": cflags_base,
        "host": False,
        "objects": objects,
    }


# Helper function for REL script objects
def Rel(lib_name, objects):
    return {
        "lib": lib_name,
        "mw_version": "GC/1.3.2",
        "cflags": cflags_rel,
        "host": True,
        "objects": objects,
    }


Matching = True
NonMatching = False

config.warn_missing_config = True
config.warn_missing_source = False
config.libs = [
    {
        "lib": "Runtime.PPCEABI.H",
        "mw_version": config.linker_version,
        "cflags": cflags_runtime,
        "host": False,
        "objects": [
            Object(Matching, "Dolphin/Runtime/ptmf_80151434.c"),
            Object(Matching, "Dolphin/Runtime/cvtfp2unsigned_801514c8.c"),
            Object(Matching, "Dolphin/Runtime/div2u_80151654.c"),
            Object(Matching, "Dolphin/Runtime/div2i_80151740.c"),
            Object(Matching, "Dolphin/Runtime/mod2u_80151878.c"),
            Object(Matching, "Dolphin/Runtime/mod2i_8015195c.c"),
            Object(Matching, "Dolphin/Runtime/shl2i_80151a68.c"),
            Object(Matching, "Dolphin/Runtime/shr2u_80151a8c.c"),
            Object(Matching, "Dolphin/Runtime/shr2i_80151ab0.c"),
            Object(Matching, "Dolphin/Runtime/cvtdblusll_80151ad8.c"),
            Object(Matching, "Runtime.PPCEABI.H/__init_cpp_exceptions.cpp"),
            Object(Matching, "Runtime.PPCEABI.H/global_destructor_chain.c"),
            Object(Matching, "Runtime.PPCEABI.H/operator_delete.cpp", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "Runtime.PPCEABI.H/ReturnException.c"),
           
        ],
    },
    {
        "lib": "Dolphin",
        "mw_version": config.linker_version,
        "cflags": cflags_runtime,
        "host": False,
        "objects": [
            Object(Matching, "Dolphin/Runtime/__mem.c"),
            Object(Matching, "Dolphin/Runtime/__va_arg.c"),
            # DEFERRED: registering .text alone duplicates __OSArenaHi/__OSArenaLo; explicit .sdata/.sbss ranges trigger a dtk cyclic-dependency error. See project memory.
            # Object(Matching, "Dolphin/os/OSArena.c"),
            # DEFERRED: not byte-exact -- scheduling residual. See project memory.
            Object(Matching, "Dolphin/os/osgetdiconfig_80161ddc.c"),
            Object(Matching, "Dolphin/os/osalarm_80161e1c.c"),
            Object(Matching, "Dolphin/os/osalloc_801625f4.c"),
            Object(Matching, "Dolphin/os/osallocfromheap_801626a0.c"),
            Object(Matching, "Dolphin/os/osallocfromarenalo_80162ca8.c"),
            Object(Matching, "Dolphin/os/OSAudioSystem.c"),
            Object(Matching, "Dolphin/os/dcstorerange_80162fd8.c"),
            Object(Matching, "Dolphin/os/OSGetExecParams.c"),
            Object(Matching, "Dolphin/os/OSLink.c"),
            Object(Matching, "Dolphin/os/OSSync.c"),
            Object(Matching, "Dolphin/os/PPCSync.c"),
            Object(Matching, "Dolphin/base/PPCArch2.c"),
            # DEFERRED: not byte-exact -- f31 save/restore frame-size residual. See project memory.
            Object(Matching, "Dolphin/base/ppcfpscr_801611d4.c"),
            Object(Matching, "Dolphin/base/PPCArch3.c"),
            Object(Matching, "Dolphin/base/ppcdisablespeculation_80161234.c"),
            Object(Matching, "Dolphin/base/ppcsetfpnonieeemode_8016125c.c"),
            # DEFERRED: not byte-exact -- scheduling/frame-shape residuals. See project memory.
            Object(Matching, "Dolphin/db/dbinit_80161264.c"),
            Object(Matching, "Dolphin/db/db2.c"),
            # DEFERRED: not byte-exact -- control-flow canonicalization (bnelr fusion). See project memory.
            Object(Matching, "Dolphin/os/osfprinit_80161350.c"),
            # Object(Matching, "Dolphin/os/osgetconsoletype_80161478.c"),
            Object(Matching, "Dolphin/os/DCZeroRange.c"),
            Object(Matching, "Dolphin/os/lcstoreblocks_801631e4.c"),
            Object(Matching, "Dolphin/os/PPCMtHID0.c"),
            Object(Matching, "Dolphin/os/stubreturn_801676bc.c"),
            Object(Matching, "Dolphin/os/osdbintend.c"),
            Object(Matching, "Dolphin/os/osswitchfpucontext_80163d88.c"),
            Object(Matching, "Dolphin/os/osfpucontextsave_80163e54.c"),
            Object(Matching, "Dolphin/os/ospanic_80163f80.c"),
            Object(Matching, "Dolphin/os/osseterrorhandler_801640ac.c"),
            Object(Matching, "Dolphin/os/fn_801645ac.c"),
            Object(Matching, "Dolphin/os/fn_80164734.c"),
            Object(Matching, "Dolphin/os/setflag_801647dc.c"),
            Object(Matching, "Dolphin/os/lcstoredata_80163208.c"),
            Object(Matching, "Dolphin/os/oscacheinit_801632c8.c"),
            Object(Matching, "Dolphin/os/osloadfpucontext_801635b4.c"),
            Object(Matching, "Dolphin/os/OSGetCurrentContext.c"),
            Object(Matching, "Dolphin/os/ossavecontext_80163870.c"),
            Object(Matching, "Dolphin/os/osloadcontext_801638f0.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/fn_8018d41c.c"),
            Object(Matching, "Dolphin/os/StubReturns.c"),
            Object(Matching, "Dolphin/gx/StubReturn_8018A2CC.c"),
            Object(Matching, "Dolphin/gx/gxsetindirectmask_8018a2d0.c"),
            Object(Matching, "Dolphin/gx/gxinittlutregion_80189a98.c"),
            Object(Matching, "Dolphin/gx/zeroreturn_80183228.c"),
            # DEFERRED: not byte-exact -- compiles 4 bytes larger, MWCC reassociates the
            # base+size-4 pointer arithmetic differently regardless of source grouping. See project memory.
            # Object(Matching, "Dolphin/gx/gxinitfifobase_8018593c.c"),
            Object(Matching, "Dolphin/gx/gxinitfifoptrs_801859a8.c"),
            Object(Matching, "Dolphin/gx/SetFieldsAt0xc0x10.c"),
            Object(Matching, "Dolphin/gx/gxsetcpufifo_80185a24.c"),
            Object(Matching, "Dolphin/gx/gxsetgpfifo_80185b4c.c"),
            # DEFERRED: not byte-exact -- bitfield-width + register-reload residuals. See project memory.
            Object(Matching, "Dolphin/gx/gxfiforeadenable_80185d7c.c"),
            Object(Matching, "Dolphin/gx/gxfiforeaddisable_80185da0.c"),
            # DEFERRED: not byte-exact -- compiles 8 bytes short, MWCC collapses the
            # if/else 0-or-1 idiom to a branchless neg/or/rlwimi sequence instead of
            # retail's explicit clrlwi./beq branch. See project memory.
            # Object(Matching, "Dolphin/gx/gxfifolink_80185dc4.c"),
            Object(Matching, "Dolphin/gx/gxwritefifointenable_80185df8.c"),
            Object(Matching, "Dolphin/gx/gxwritefifointreset_80185e28.c"),
            Object(Matching, "Dolphin/gx/gxgetcpufifo_80185f58.c"),
            Object(Matching, "Dolphin/gx/gxgetgpfifo_80185f60.c"),
            # DEFERRED: Dolphin/gx/gxsetvtxdesc_80185f68.c (GXSetVtxDesc, 0x80185F68, size 0x26C)
            # Source is verbatim-correct (matches vendored src/Dolphin/gx/GXAttr.c lines 31-95 exactly,
            # confirmed against jumptable_80236880's real byte contents/order - case dispatch mapping,
            # including the 4 duplicate fallthrough-to-tail slots for GX_POS_MTX_ARRAY..GX_LIGHT_ARRAY
            # (values 21-24, no case labels), is 100% correct). Only 2 pure register/scheduling residuals
            # remain, both irreducible so far:
            #  1) Jump-table dispatch prologue: retail emits lis r5,jt@ha / addi r5,r5,jt@l / slwi r0,r3,2
            #     / lwzx r0,r5,r0; MWCC default (-O4,p) emits lis r5,.. / slwi r0,r3,2 / addi r3,r5,.. /
            #     lwzx r0,r3,r0 (reordered + addi dest r3 instead of r5). Per-object "-schedule off" FIXES
            #     this exactly, but at the cost of breaking the GX_VA_NRM/GX_VA_NBT case bodies elsewhere
            #     in the same function (retail keeps "li r5,0x1"+order there; -schedule off changes it to
            #     "li r0,0x1" + different instruction order) - a net wash, not a fix.
            #  2) Post-switch tail (final "if (gx->hasNrms || gx->hasBiNrms)" block through to
            #     "gx->dirtyState |= ..."): retail caches the reloaded __GXData pointer in r4 (recycling
            #     the dead "type" param register); MWCC default picks r5 instead. Same 4 instructions/
            #     opcodes in both, only the register NUMBER differs. This residual is UNAFFECTED by
            #     -schedule on/off either way (confirmed empirically) - it's a separate, independent
            #     register-allocator choice.
            # Also tried: `#pragma scheduling off/on` scoped just around the switch header - had ZERO
            # effect (byte-identical to no pragma at all), suggesting this MWCC version's "scheduling"
            # pragma is a function-level all-or-nothing setting, not toggleable mid-function - so the two
            # residuals above cannot be split apart via scoped pragmas either. File kept on disk verbatim
            # for a future attempt (e.g. compiling alongside sibling GXAttr.c functions in one TU, per the
            # established "cross-function register/inlining context" pattern from HSD_SetupPEMode).
            # Object(Matching, "Dolphin/gx/gxsetvtxdesc_80185f68.c"),
            # DEFERRED: Dolphin/gx/gxcalculatevlim_80186518.c (__GXCalculateVLim, 0x80186518, size 0x124)
            # Source is verbatim vendored logic (matches src/Dolphin/gx/GXAttr.c __GXCalculateVLim exactly),
            # and the 3 lookup tables (originally vendored as per-function "static u8 tblN[]" locals) were
            # correctly redirected to the real SHARED globals lbl_8065ACC0/lbl_8065ACC4/lbl_8065ACC8
            # (confirmed via build/GGTE01/asm/auto_09_8065ABC0_sdata.s real byte content: {0,4,1,2},
            # {0,8,1,2}, {0,12,1,2} respectively - these are referenced by OTHER GXAttr.c-cluster functions
            # too, not exclusive to this one). Compiles 8 bytes too long (0x12C vs declared 0x124) and needs
            # a stack frame (stwu/stw r31/lwz r31, all nonvolatile-register spill) that retail's real build
            # doesn't need at all (retail fits the whole function in volatile regs r0,r3-r9, ending in a
            # bare `beqlr`/`blr`, never touching r10+). Root cause: retail recomputes
            # `li rX, lbl_8065ACC8@sda21` a SECOND time (at its 2nd use site, for the GX_VA_NRM lookup) even
            # though it's the identical subexpression already computed for the GX_VA_POS lookup just above -
            # i.e. retail's real build did NOT common-subexpression-eliminate this repeated address load,
            # while our -O4,p compile does (caches it once, reuses it), which cascades into needing more
            # simultaneous live registers than retail's redundant-but-cheaper version. Tried an explicit
            # (u32) cast on the 2nd lookup's index expression to discourage CSE - no effect (byte-identical
            # output). Same "MWCC CSEs a call-site/subexpression where retail's real build didn't" residual
            # class already documented multiple times in project memory (self+0x4c, table+0 argument, etc.)
            # - "unfixable via source restructuring" per established precedent. Kept on disk for a future
            # attempt (untried: extracting the table-lookup into a manually-repeated inline-asm-guarded
            # sub-function, or compiling alongside GXAttr.c siblings in one TU).
            # Object(Matching, "Dolphin/gx/gxcalculatevlim_80186518.c"),
            Object(Matching, "Dolphin/gx/gxclearvtxdesc_80186880.c"),
            Object(Matching, "Dolphin/gx/gxinvalidatevtxcache_80187154.c"),
            Object(Matching, "Dolphin/gx/gxsetnumtexgens_801873e4.c"),
            Object(Matching, "Dolphin/gx/gxflush_801874b4.c"),
            Object(Matching, "Dolphin/gx/gxsetdrawdone_80187844.c"),
            Object(Matching, "Dolphin/gx/gxwaitdrawdone_801878dc.c"),
            Object(Matching, "Dolphin/gx/gxdrawdone_80187928.c"),
            Object(Matching, "Dolphin/gx/gxpixmodesync_801879a8.c"),
            Object(Matching, "Dolphin/gx/gxpokealphamode_801879cc.c"),
            Object(Matching, "Dolphin/gx/gxpokealpharead_801879e0.c"),
            Object(Matching, "Dolphin/gx/gxpokealphaupdate_80187a00.c"),
            Object(Matching, "Dolphin/gx/gxpokedstalpha_80187a94.c"),
            Object(Matching, "Dolphin/gx/gxpokezmode_80187ad0.c"),
            Object(Matching, "Dolphin/gx/gxsetcullmode_80187f94.c"),
            # DEFERRED: Dolphin/gx/gxsetcoplanar_80187fbc.c (GXSetCoPlanar, 0x80187FBC, size 0x34)
            # Source is verbatim-correct (matches vendored src/Dolphin/gx/GXGeometry.c logic exactly,
            # 3 GX_SET_REG/GX_BP_LOAD_REG calls). Compiles 4 bytes too long (0x38 vs declared 0x34) and
            # every instruction OPCODE is a superset of retail's PLUS one extra `clrlwi r5,r3,24`: MWCC
            # defensively truncates the `GXBool enable` (u8-typed) parameter to 8 bits before using it in
            # the GX_SET_REG/__rlwimi bitfield-insert call, even though __rlwimi only reads a specific
            # rotated bit and correctness doesn't actually require the truncation. Retail's real build does
            # NOT emit this truncate. Tried: (u32) cast at the call site (no effect - the defensive clear is
            # tied to the PARAMETER's declared width, not the call site); changing the parameter type to
            # `u32` (rejected by the compiler - conflicts with the shared `GXBool` prototype already declared
            # in the public gx.h header, would require an unsafe project-wide signature change to fix one
            # function). Also causes a register-role swap (gx cached in r6 vs r7, order of the addr-base/
            # genMode-read swapped) as a secondary, likely consequential effect. "Unfixable via source
            # restructuring" class (ABI/parameter-width defensive-code variant, new sub-case for future
            # reference). Kept on disk for a future attempt.
            # Object(Matching, "Dolphin/gx/gxsetcoplanar_80187fbc.c"),
            # DEFERRED: Dolphin/gx/gxsetgenmode_80187ff0.c (__GXSetGenMode, 0x80187FF0, size 0x24)
            # Source is verbatim-correct (matches vendored src/Dolphin/gx/GXGeometry.c __GXSetGenMode
            # exactly - GX_BP_LOAD_REG(gx->genMode); gx->bpSentNot = GX_FALSE;). Every instruction OPCODE
            # matches retail exactly (8 instructions, same total size) but registers/order are swapped:
            # retail loads `gx` first (r4) then the BP addr base (r5), interleaving the 2nd statement's
            # `li r0,0x0` constant between the 1st statement's cmd-byte-write and data-write; our compile
            # computes the addr base first and defers the `gx` load until first needed (a different, equally
            # valid instruction schedule). Tried caching `gx->genMode` into a local BEFORE the macro call
            # (changed the schedule but did not match - moved the cmd-byte write later instead) and caching
            # just the `gx` pointer into a local `GXData*` (compiler optimized the local away entirely, zero
            # effect). Same "unfixable via source restructuring" pure-scheduling residual class as several
            # other GX functions this session. Kept on disk for a future attempt.
            # Object(Matching, "Dolphin/gx/gxsetgenmode_80187ff0.c"),
            # DEFERRED: Dolphin/gx/gxclearboundingbox_80188a84.c (GXClearBoundingBox, 0x80188A84, size 0x38)
            # Source is verbatim-correct (2x GX_BP_LOAD_REG + gx->bpSentNot=GX_FALSE, matches vendored
            # src/Dolphin/gx/GXFrameBuf.c exactly). Every instruction OPCODE matches retail (same 13
            # instructions/0x38 bytes) but the SCHEDULE differs: retail loads `gx` (__GXData) FIRST, before
            # computing either BP constant, while our compile defers the `gx` load until its last use (right
            # before the final sth). Tried caching `gx` into a local `GXData*` at function entry (compiler
            # optimized the local away entirely, zero effect - same as gxsetgenmode_80187ff0.c) and moving
            # the `gx->bpSentNot=GX_FALSE` statement to the TOP of the function (produced a 3rd, still-
            # different, still-wrong schedule). Same "unfixable via source restructuring" pure-scheduling
            # residual as gxsetgenmode_80187ff0.c right next to it - NOTE: this is now the 2nd/3rd confirmed
            # instance in this exact GXFrameBuf.c/GXGeometry.c neighborhood of "retail eagerly loads `gx`
            # before doing anything else, our compile defers it" - worth trying the "compile alongside
            # sibling functions in one TU" theory here specifically if revisited, since it recurs enough in
            # this one area to suggest a shared root cause (unlike the more scattered residuals elsewhere).
            # Object(Matching, "Dolphin/gx/gxclearboundingbox_80188a84.c"),
            Object(Matching, "Dolphin/gx/gxinitlightattn_80188abc.c"),
            # DEFERRED: Dolphin/gx/gxinitlightdistattn_80188c68.c (GXInitLightDistAttn, 0x80188C68, size 0xD0)
            # Source is verbatim-correct (matches vendored src/Dolphin/gx/GXLight.c exactly; also fixed the
            # float constants to reference the real SHARED globals lbl_8065F380(0.0f)/lbl_8065F398(1.0f)/
            # lbl_8065F3AC(0.5f) instead of raw literals, which otherwise create new anonymous per-file
            # .sdata2 blobs - same technique as gxcalculatevlim_80186518.c). Compiles 12 bytes SHORT (0xC4
            # vs declared 0xD0): retail reloads lbl_8065F380/lbl_8065F398 fresh via a new `lfs` at nearly
            # every branch/use site (even when the exact same constant was already loaded into a register a
            # few instructions earlier), while our -O4,p compile recognizes the repeated reads of the same
            # global as a common subexpression and caches/reuses the register instead of reloading - same
            # "MWCC CSEs where retail's real build didn't" residual class as gxcalculatevlim_80186518.c's
            # jump-table-address reload. Tried marking the 3 extern float globals `volatile` to force fresh
            # reads everywhere - overcorrected badly (forced fresh reloads even WITHIN a single expression's
            # sub-terms where retail itself DOES reuse a value, ballooning to 0xEC bytes, worse than either
            # baseline). Plain (non-volatile) extern is the closest form (12 bytes short) and is what's kept
            # on disk. "Unfixable via source restructuring" class, new instance confirming the CSE-avoidance
            # residual recurs specifically around this project's shared float-constant/table globals.
            # Object(Matching, "Dolphin/gx/gxinitlightdistattn_80188c68.c"),
            Object(Matching, "Dolphin/gx/gxinitlightpos_80188d38.c"),
            Object(Matching, "Dolphin/gx/gxinitlightdir_80188d48.c"),
            Object(Matching, "Dolphin/gx/gxinitlightcolor_80188d64.c"),
            # DEFERRED: compiles 4 bytes larger than retail (0x80 vs 0x7C) --
            # shifts every symbol after it. See project memory.
            # Object(Matching, "Dolphin/gx/gxloadlightobjimm_80188d70.c"),
            Object(Matching, "Dolphin/os/OSGetStackPointer.c"),
            Object(Matching, "Dolphin/os/osinitcontext_80163a24.c"),
            Object(Matching, "Dolphin/os/osdumpcontext_80163ae0.c"),
            Object(Matching, "Dolphin/os/osdisableinterrupts_80166e50.c"),
            Object(Matching, "Dolphin/os/OSGetInterruptHandler.c"),
            Object(Matching, "Dolphin/os/osmaskinterrupts_80166f40.c"),
            Object(Matching, "Dolphin/os/osdispatchinterrupt_80167328.c"),
            Object(Matching, "Dolphin/os/StubReturn_80169E30.c"),
            # DISABLED: new .bss global (Scb) shifts downstream layout, reproduces the save-load black-screen bug. See project memory.
            # Object(Matching, "Dolphin/os/osgetprogressivemode_80169808.c"),
            # Object(Matching, "Dolphin/os/osgetlanguage_8016991c.c"),
            Object(Matching, "Dolphin/os/OSInitThreadQueue.c"),
            Object(Matching, "Dolphin/gx/GXInitTexObjUserData.c"),
            Object(Matching, "Dolphin/os/osgetphysicalmemsize_801682ac.c"),
            Object(Matching, "Dolphin/axfx/AXFXHooks.c"),
            Object(Matching, "game/system/initializearray_80169be0.cpp"),
            # DEFERRED: not byte-exact -- scheduling residual. See project memory.
            Object(Matching, "game/system/structzeroinit_80169d84.cpp"),
            Object(Matching, "game/system/checkstatefield.cpp"),
            Object(Matching, "Dolphin/os/osscheduler_80169fdc.c"),
            Object(Matching, "Dolphin/os/osthread1_8016a05c.c"),
            Object(Matching, "Dolphin/os/seteffectivepriority_8016a100.c"),
            Object(Matching, "Dolphin/os/selectthread_8016a2c0.c"),
            Object(Matching, "Dolphin/os/osreschedule_8016a4e8.c"),
            Object(Matching, "Dolphin/os/oscreatethread_8016a554.c"),
            Object(Matching, "Dolphin/os/osthreadcluster_8016a73c.c"),
            Object(Matching, "Dolphin/os/osclearstack_8016afc4.c"),
            Object(Matching, "Dolphin/os/ostime_8016b070.c"),
            Object(Matching, "Dolphin/os/osgetsystemtime_8016b090.c"),
            Object(Matching, "Dolphin/os/ostimetosystemtime_8016b0f4.c"),
            # DISABLED: not byte-matching -- oversized compile shifted downstream addresses (__start.c). See project memory.
            # Object(Matching, "Dolphin/os/__start.c"),
            Object(Matching, "Dolphin/os/__ppc_eabi_init.cpp"),
            # DISABLED: not byte-matching -- broken memory-card subsystem, caused real save corruption. See project memory.
            # Object(Matching, "Dolphin/card/CARDOpen.c"),
            Object(Matching, "Dolphin/pad/paddisablerecalibration_80174678.c"),
            Object(Matching, "Dolphin/ai/aistartdma_801747c0.c"),
            Object(Matching, "Dolphin/ai/aistopdma_801747d8.c"),
            Object(Matching, "Dolphin/ai/aigetdmastartaddr_801747f0.c"),
            Object(Matching, "Dolphin/ai/aigetstreamplaystate_801748e4.c"),
            Object(Matching, "Dolphin/ai/aigetdspsamplerate_801749d4.c"),
            Object(Matching, "Dolphin/ai/aisetstreamvolleft_80174acc.c"),
            Object(Matching, "Dolphin/ar/argetdmastatus_80175044.c"),
            Object(Matching, "Dolphin/ar/arstartdma_80175080.c"),
            Object(Matching, "Dolphin/ar/arclearinterrupt_80175390.c"),
            Object(Matching, "Dolphin/ar/argetinterruptstatus_801753b0.c"),
            Object(Matching, "Dolphin/dsp/dspmail_8017cd80.c"),
            Object(Matching, "Dolphin/dsp/dspcanceltask_8017cf08.c"),
            Object(Matching, "Dolphin/card/cardputcontrolblock_8017eb20.c"),
            Object(Matching, "Dolphin/card/cardgetdirblock_80180784.c"),
            # DEFERRED: not byte-exact -- addi-vs-mr register-copy opcode choice. See project memory.
            # Object(Matching, "Dolphin/gx/GXDisplayList.c"),
            # DEFERRED: Dolphin/gx/gxsetprojection_8018c2c0.c (GXSetProjection, 0x8018C2C0, size 0xA4)
            # Source is verbatim-correct (matches vendored src/Dolphin/gx/GXTransform.c exactly, including
            # hand-inlining the `static` helpers `WriteProjPS`/`__GXSetProjection` directly into the body
            # since MWCC's automatic inliner refuses to inline functions containing a raw whole-function
            # `asm { }` block, even within the same translation unit - confirmed by first trying them as
            # separate `static` functions, which compiled to 2 extra un-inlined `local`-scope functions
            # totaling far more than retail's real 0xA4 bytes; retail's real build has everything fully
            # inlined into one function). After manual inlining, compiles 4 bytes SHORT (0xA0 vs 0xA4) and
            # is otherwise near-perfect: only 2 residuals remain, (1) a 1-instruction `gx` load reordering
            # (cosmetic, same "gx eager-load" scheduling class as other GX deferrals this session) and (2)
            # retail explicitly computes `addi r3,r4,0x4dc` (materializing a real pointer register for
            # `gx->projMtx`) before the 3 `psq_l` paired-single loads use SMALL offsets (0,8,16) on that
            # pointer, while our compile folds the `+0x4dc` struct-field offset directly into each `psq_l`'s
            # own displacement field instead (large offsets 0x4dc/0x4e4/0x4ec directly on `gx`) - MWCC
            # optimizing away the separate address materialization our source's raw `asm` block expects.
            # Tried: `f32* volatile src` (rejected by the compiler - asm-block operands require `register`,
            # not `volatile`) and an explicit `(const f32*)&gx->projMtx[0]` cast instead of plain array-decay
            # assignment (zero effect, byte-identical). "Unfixable via source restructuring" class, new
            # variant specific to raw-asm-block operand address-folding. Very close (4 bytes/2 residuals) -
            # a good candidate to revisit first if resuming this area.
            # Object(Matching, "Dolphin/gx/gxsetprojection_8018c2c0.c"),
            Object(Matching, "Dolphin/gx/gxcleargpmetric_8018d0c0.c"),
            Object(Matching, "Dolphin/mtx/psmtxmultvec.c"),
            Object(Matching, "Dolphin/mtx/psmtxmultvecsr.c"),
            Object(Matching, "Dolphin/mtx/mtx44persp_8016c490.c"),
            Object(Matching, "Dolphin/mtx/psvecsubtract.c"),
            # DEFERRED: not byte-exact -- scheduling residual. See project memory.
            Object(Matching, "Dolphin/dvd/dvdlowbreak_8016d69c.c"),
            # DEFERRED: not byte-exact -- scheduling residual. See project memory.
            Object(Matching, "Dolphin/dvd/dvdlowreset_8016d5e0.c"),
            Object(Matching, "Dolphin/dvd/dvdlowclearcallback_8016d6b0.c"),
            Object(Matching, "Dolphin/dvd/dvdlowsetwatype_8016d6cc.c"),
            Object(Matching, "Dolphin/dvd/dvdfsinit_8016d748.c"),
            Object(Matching, "Dolphin/dvd/dvdclose_8016dae8.c"),
            # DEFERRED: caused a live crash (jump into garbage .bss via a bad
            # callback pointer) when boot-tested via ISO. See project memory.
            # Object(Matching, "Dolphin/dvd/dvdreadasyncprio_8016db6c.c"),
            # Object(Matching, "Dolphin/dvd/cbforreadasync_8016dc2c.c"),
            Object(Matching, "Dolphin/dvd/stubreturn_8016dc5c.c"),
            # DEFERRED: not byte-exact -- stack-frame padding residual. See project memory.
            Object(Matching, "Dolphin/dvd/dvdlowwaitmotorstopped_8016eb08.c"),
            # DEFERRED: caused a live crash (jump into garbage .bss via a bad
            # callback pointer) when boot-tested via ISO. See project memory.
            # Object(Matching, "Dolphin/dvd/dvdreadabsasyncprio_8016f89c.c"),
            # Object(Matching, "Dolphin/dvd/dvdreadabsasyncforbs_8016f978.c"),
            # Object(Matching, "Dolphin/dvd/dvdcancelstreamasync_8016fb1c.c"),
            Object(Matching, "Dolphin/dvd/dvdreset_8016fca8.c"),
            Object(Matching, "Dolphin/dvd/dvdgetcommandblockstatus_8016fcec.c"),
            Object(Matching, "Dolphin/dvd/dvdsetautoinvalidation_8016fde4.c"),
            Object(Matching, "Dolphin/dvd/dvdgetcurrentdiskid_80170190.c"),
            Object(Matching, "Dolphin/dvd/dvdqueue.c"),
            Object(Matching, "Dolphin/dvd/dvderror.c"),
            Object(Matching, "Dolphin/dvd/dvdcomparediskid_80170774.c"),
            Object(Matching, "Dolphin/dvd/dvdFatal.c"),
            Object(Matching, "Dolphin/MSL_C/MSL_Common_Embedded/Math/Double_precision/s_copysign.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "Dolphin/MSL_C/MSL_Common_Embedded/Math/Double_precision/s_floor.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "Dolphin/MSL_C/MSL_Common_Embedded/Math/Double_precision/s_frexp.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "Dolphin/MSL_C/MSL_Common_Embedded/Math/Double_precision/s_ldexp.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "Dolphin/MSL_C/MSL_Common_Embedded/Math/Double_precision/s_modf.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "Dolphin/MSL_C/MSL_Common_Embedded/Math/Double_precision/e_fmod.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "Dolphin/MSL_C/MSL_Common_Embedded/Math/Double_precision/e_rem_pio2.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "Dolphin/MSL_C/MSL_Common_Embedded/Math/Double_precision/k_cos.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "Dolphin/MSL_C/MSL_Common_Embedded/Math/Double_precision/k_rem_pio2.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "Dolphin/MSL_C/MSL_Common_Embedded/Math/Double_precision/k_sin.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "Dolphin/MSL_C/MSL_Common_Embedded/Math/Double_precision/k_tan.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "Dolphin/MSL_C/MSL_Common_Embedded/Math/Double_precision/s_atan.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "Dolphin/MSL_C/MSL_Common_Embedded/Math/Double_precision/s_tan.c", extra_cflags=["-i include/stl"]),
            # DEFERRED: not byte-exact -- missing frsp residual. See project memory.
            Object(Matching, "Dolphin/MSL_C/MSL_Common_Embedded/Math/Single_precision/trigwrappers_8015cedc.c"),
            Object(Matching, "Dolphin/MSL_C/MSL_Common_Embedded/Math/Double_precision/sqrt_8015cf24.c"),
            Object(Matching, "Dolphin/MSL_C/PPC_EABI/criticalregionsempty.c"),
            Object(Matching, "Dolphin/MSL_C/MSL_Common/mem.c", extra_cflags=["-i include/stl"]),
            # DEFERRED: byte-exact in isolation, but claiming it breaks the whole DOL's CHECK (a dtk __mod2u boundary-size ambiguity). See project memory.
            # Object(Matching, "Dolphin/MSL_C/PPC_EABI/stubreturn_80151958.c"),
            Object(Matching, "Dolphin/MSL_C/MSL_Common/mem_funcs.c"),
            Object(Matching, "Dolphin/MSL_C/MSL_Common/stdioatexit.c"),
            Object(Matching, "Dolphin/MSL_C/MSL_Common/strchr.c"),
            Object(Matching, "Dolphin/MSL_C/MSL_Common/strcmp.c"),
            Object(Matching, "Dolphin/MSL_C/MSL_Common/strncpy.c"),
            Object(Matching, "Dolphin/MSL_C/MSL_Common/strcpy.c"),
            Object(Matching, "Dolphin/MSL_C/MSL_Common/free.c"),
            Object(Matching, "Dolphin/MSL_C/MSL_Common/ansi_files.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "Dolphin/MSL_C/MSL_Common/file_io.c"),
            Object(Matching, "Dolphin/MSL_C/MSL_Common/buffer_io.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "Dolphin/MSL_C/MSL_Common/ctype.c", extra_cflags=["-i include/stl"]),
            # DISABLED: entire SI controller-read cluster -- bisection-confirmed cause of broken controller input. Two real opword bugs fixed (see those files) but insufficient alone; root cause of the remaining breakage not yet isolated. See project memory.
            # Object(Matching, "Dolphin/si/SISamplingRate.c"),
            Object(Matching, "Dolphin/vi/vigetcurrentline_801729f4.c"),
            Object(NonMatching, "Dolphin/vi/vigettvformat_80172a8c.c"),
            Object(Matching, "Dolphin/vi/vigetdtvstatus_80172af4.c"),
            # DEFERRED: not byte-exact -- scheduling residual. See project memory.
            # Object(Matching, "Dolphin/si/sibusy_8015f958.c"),
            # Object(Matching, "Dolphin/si/completetransfer_8015f9b4.c"),
            # Object(Matching, "Dolphin/si/siinterrupthandler_8015fcb0.c"),
            # Object(Matching, "Dolphin/si/sienablepollinginterrupt_8015fff4.c"),
            # Object(Matching, "Dolphin/si/siinit_8016024c.c"),
            # Object(Matching, "Dolphin/si/sitransfer_80160300.c"),
            # Object(Matching, "Dolphin/si/sigetstatus_8016050c.c"),
            # Object(Matching, "Dolphin/si/sitransfercommands_8016059c.c"),
            # Object(Matching, "Dolphin/si/sisetxy_801605ac.c"),
            # Object(Matching, "Dolphin/si/sigetresponseraw_80160720.c"),
            # Object(Matching, "Dolphin/si/sialarmhandler_801608b8.c"),
            # Object(Matching, "Dolphin/si/gettypecallback_80160ab0.c"),
            # DEFERRED: not byte-exact -- scheduling residual. See project memory.
            Object(Matching, "Dolphin/exi/setexiinterruptmask_8015d9c4.c"),
            Object(Matching, "Dolphin/exi/exiimm_8015dab8.c"),
            Object(Matching, "Dolphin/exi/exiclearinterrupts_8015e0ec.c"),
            Object(Matching, "Dolphin/exi/exidetach_8015e564.c"),
            Object(Matching, "Dolphin/exi/exiinterrupthandlers_8015e85c.c"),
            Object(Matching, "Dolphin/exi/exiinit_8015ec0c.c"),
            Object(Matching, "Dolphin/exi/exigetstate_8015efb0.c"),
            Object(Matching, "Dolphin/exi/exigetid_8015efc8.c"),

        ],
    },
       {
        "lib": "TRK_MINNOW_DOLPHIN",
        "mw_version": config.linker_version,
        "cflags": cflags_trk,
        "host": False,
        "objects": [
            Object(Matching, "TRK_MINNOW_DOLPHIN/mem_TRK.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/fpscr.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/__exception.o"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/dolphin_trk.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/main_TRK.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/mainloop.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/trkinitializedispatcher.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/interruptstatehelpers.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/nubinit.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/usr_put.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/mutex_TRK.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/flush_cache.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/targcont.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/close_console.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/udp_cc.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/ddh_cc_simple.c", extra_cflags=["-sdatathreshold 8"]),
            Object(Matching, "TRK_MINNOW_DOLPHIN/ddh_cc_initinterrupts.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/ddh_cc_peek.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/ddh_cc_stopcontinue.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/gdev_cc_initinterrupts.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/gdev_cc_stopcontinue.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/stubreturn_8015cf44.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/fn_80150954.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/setglobal_80158a0c.c", extra_cflags=["-sdatathreshold 8"]),
            Object(Matching, "TRK_MINNOW_DOLPHIN/flagaccessors_80150150.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/getaddr_8015304c.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/gdev_cc_simple.c", extra_cflags=["-sdatathreshold 8"]),
            Object(Matching, "TRK_MINNOW_DOLPHIN/trktargetgetpc.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/trkdooverride.cpp"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/outputdata.cpp"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/trktargetaccessaram.cpp"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/ddh_cc_initialize.c"),
            Object(Matching, "TRK_MINNOW_DOLPHIN/gdev_cc_initialize.c"),
            # DISABLED: not byte-exact -- pure register-allocation residual (unfixable via source restructuring). See project memory.
            # DISABLED: not byte-exact -- same register-allocation residual as its sibling above (unfixable via source restructuring). See project memory.
            # Object(Matching, "TRK_MINNOW_DOLPHIN/ddh_cc_write.c", extra_cflags=["-sdatathreshold 8"]),
            # DISABLED: not byte-exact -- pure register-role permutation (unfixable via source restructuring). See project memory.
            # Object(Matching, "TRK_MINNOW_DOLPHIN/ddh_cc_read.c", extra_cflags=["-sdatathreshold 8"]),
            # DISABLED: not byte-exact -- down to one register-scheduling residual (unfixable via source restructuring). See project memory.
            # Object(Matching, "TRK_MINNOW_DOLPHIN/gdev_cc_write.c", extra_cflags=["-sdatathreshold 8"]),
            Object(Matching, "TRK_MINNOW_DOLPHIN/trkcommreaddispatch.c"),
            # DISABLED: not byte-exact -- MWCC CSEs a repeated address computation retail recomputes fresh each call. See project memory.
            # Object(Matching, "TRK_MINNOW_DOLPHIN/initprogramendtrap.c"),



        ],
    },
     
     {
        "lib": "SysDolphin",
        "mw_version": config.linker_version,
        "cflags": cflags_runtime,
        "host": False,
        "objects": [
            Object(Matching, "THP/THPAudio.cpp"),
            Object(Matching, "THP/thpsimplegetcurrentframe.c", extra_cflags=["-sdatathreshold 0"]),


        ],
    },
     {
        "lib": "BaseLib",
        "mw_version": config.linker_version,
        "cflags": cflags_runtime,
        "host": False,
        "objects": [
            # DISABLED: not byte-matching -- compiles short vs declared size (ELF size cross-reference). See project memory.
            # Object(Matching, "game/system/registershortcut.cpp"),
            Object(Matching, "game/system/initparams.cpp"),
            Object(Matching, "game/system/ringbufferupdate.cpp"),
            Object(Matching, "game/system/gdevccshutdown.cpp"),
            # DISABLED: not byte-matching -- broken memory-card subsystem, caused real save corruption. See project memory.
            # Object(Matching, "game/system/carddeletehandler.cpp"),
            Object(Matching, "game/system/disableobjfunc.cpp"),
            # DISABLED: not byte-matching -- broken memory-card subsystem, caused real save corruption. See project memory.
            # Object(Matching, "game/system/initcardhandler.cpp"),
            # DISABLED: not byte-matching -- broken memory-card subsystem, caused real save corruption. See project memory.
            # Object(Matching, "game/system/initializecard.cpp"),
            # DISABLED: not byte-matching -- broken memory-card subsystem, caused real save corruption. See project memory.
            # Object(Matching, "game/system/initializecarddata.cpp"),
            # DISABLED: not byte-matching -- broken memory-card subsystem, caused real save corruption. See project memory.
            # Object(Matching, "game/system/initializecard2.cpp"),
            # DISABLED: not byte-matching -- broken memory-card subsystem, caused real save corruption. See project memory.
            # Object(Matching, "game/system/cardwrappers.cpp"),
            # DISABLED: not byte-matching -- broken memory-card subsystem, caused real save corruption. See project memory.
            # Object(Matching, "game/system/cardwrappers2.cpp"),
            Object(Matching, "game/system/initcameramemento.cpp"),
            Object(Matching, "game/system/getvalueataddr.cpp"),
            # DISABLED: not byte-matching -- broken memory-card subsystem, caused real save corruption. See project memory.
            # Object(Matching, "game/system/loadcardhandler.cpp"),
            # DISABLED: not byte-matching -- broken memory-card subsystem, caused real save corruption. See project memory.
            # Object(Matching, "game/system/cardhandlerthread.cpp"),
            Object(Matching, "game/system/gdevccshutdown2.cpp"),
            Object(Matching, "game/system/gdevccshutdown3.cpp"),
            Object(Matching, "game/system/project3d.cpp"),
            Object(Matching, "game/system/vecelemmul.cpp"),
            Object(Matching, "game/system/findlargestvalue.cpp"),
            Object(Matching, "game/system/clearinterrupts.cpp"),
            Object(Matching, "game/system/processtreenode.cpp"),
            Object(Matching, "game/system/processobjectsintree.cpp"),
            Object(Matching, "game/system/processtranslationx.cpp"),
            Object(Matching, "game/system/renderchildupdatestate.cpp"),
            Object(Matching, "game/system/translatexdeps.cpp"),
            Object(Matching, "game/system/updatechildobjtree.cpp"),
            # DISABLED: not byte-matching -- compiles short vs declared size (ELF size cross-reference). See project memory.
            # Object(Matching, "game/system/cleanupobject.cpp"),
            Object(Matching, "game/system/renderobstructiontexture.c"),
            Object(Matching, "game/system/renderchildobjects.c"),
            # Near-miss: not byte-exact -- register-allocation residual (self+0x18/0x1c hoisted vs retail's fresh per-call recompute). See project memory.
            # Object(Matching, "game/system/processdataforqueue.c"),
            # Near-miss: not byte-exact -- 16 bytes short, 3 stacked register/scheduling residuals; extra_cflags below are confirmed correct if revisited. See project memory.
            # Object(Matching, "game/system/loadmoduleandexecute.c", extra_cflags=["-sdatathreshold 12", "-Cpp_exceptions on"]),
            # Near-miss: not byte-exact -- 2 field-existence tests load into r0 vs retail's r4 (register-choice residual). See project memory.
            # Object(Matching, "game/system/removeelementsandstreams.c"),
            # Near-miss: not byte-exact -- register-choice swap between a persisted parameter and local. See project memory.
            # DEFERRED: not byte-exact -- MWCC's inline-asm parser can't emit a compact base-register-less SDA21 address load. See project memory.
            Object(Matching, "game/system/updatetreenodestate.c"),
            # DEFERRED: sysdolphin/baselib/hsdjobjunref_801c6cd8.c (HSD_JObjUnref, 0x801C6CD8,
            # size 0x148). Source is a 100%-correct reconstruction (confirmed via isolated .o
            # disasm diff - every instruction, operand, and byte offset matches except one) using
            # the real disasm-derived assert strings lbl_8025A0F8="object.h"/lbl_8025A12C="HSD_OBJ
            # (o)->ref_count_individual != 0" (the vendored source's own HSD_JObj_804068E4/
            # HSD_JObj_80406918 names are WRONG placeholder addresses, same class of stale-name bug
            # documented elsewhere in this project). The ONLY residual: object.h's shared inline
            # `ref_DEC()` helper - used here for the first time in this project, unmodified from the
            # header - picks register r3 for its internal `ret` boolean where retail's real compile
            # picks r0; every subsequent instruction in the whole function shifts registers to match
            # (byte count identical, purely cosmetic operand-letter differences). Tried inverting the
            # top-level guard to `if (jobj == NULL || !ref_DEC(jobj)) return;` early-return form -
            # made it WORSE (2/17 instead of 16/17), reverted. This is the same "register-choice
            # residual, unfixable via source restructuring" class as the already-deferred
            # HSD_ObjAllocAddFree/HSD_Alloc from earlier in this project. Kept on disk, ready for a
            # future attempt (e.g. once another caller of the untouched object.h ref_DEC/iref_DEC
            # exists to cross-check register-allocation behavior against).
            # Object(Matching, "sysdolphin/baselib/hsdjobjunref_801c6cd8.c"),
            Object(Matching, "sysdolphin/baselib/hsdjobjresolverefs_801c6840.c"),
            # DEFERRED: sysdolphin/baselib/hsdjobjresolverefsall_801c6938.c (HSD_JObjResolveRefsAll,
            # 0x801C6938, size 0x2D4). Vendored source is a simple while-loop + one recursive call
            # to itself plus a call to HSD_JObjResolveRefs per iteration - logically correct - but
            # retail's real compile (from the ORIGINAL monolithic jobj.c, where HSD_JObjResolveRefs's
            # full body was defined earlier in the SAME translation unit) auto-INLINED
            # HSD_JObjResolveRefs's entire ~25-instruction body directly into 3 manually-unrolled
            # recursion levels (using register sets r27/r28, r30/r29, r26/r25), then falls back to
            # two REAL calls (`bl HSD_JObjResolveRefs` + `bl HSD_JObjResolveRefsAll`) only at the 4th
            # nesting level. Since this project splits every function into its own translation unit,
            # HSD_JObjResolveRefs's body is invisible to this file's compile, so MWCC cannot make the
            # same inline-vs-call choice per call site - a plain `bl HSD_JObjResolveRefs` at every
            # loop level is smaller than retail's inlined version, so "-inline auto"'s size-based
            # recursion-unrolling budget goes DEEPER than retail (confirmed: produced 5+ unrolled
            # levels instead of retail's 3, all calling the real external function, size 0x24C vs
            # retail's 0x2D4). Manually duplicating HSD_JObjResolveRefs's body as a local static
            # copy would let MWCC inline it, but the recursive "base case" call would then need to
            # target the REAL external HSD_JObjResolveRefs symbol specifically (matching retail's
            # `bl fn_801C6840`) while shallower levels inline a local duplicate - not something
            # straightforwardly expressible in C source; the compiler's inline-vs-call choice per
            # call site of the SAME global function only naturally arises when the full body is
            # defined in-TU, which conflicts with this project's one-function-per-file convention.
            # Good candidate for a future attempt (e.g. testing whether just inlining a `static`
            # duplicate is close enough once diffed, or finding the right cflags to tune the
            # recursion-inlining depth threshold). Kept on disk, not wired.
            # Object(Matching, "sysdolphin/baselib/hsdjobjresolverefsall_801c6938.c"),
            Object(Matching, "sysdolphin/baselib/hsdjobjunrefthis_801c6e20.c"),
            Object(Matching, "sysdolphin/baselib/hsdjobjreqanimall_801c4704.c"),
            Object(Matching, "sysdolphin/baselib/hsdjobjaddchild_801c6ec8.c"),
            # DEFERRED: sysdolphin/baselib/hsdjobjinit_801c8cf4.c (JObjInit, 0x801C8CF4, size
            # 0x64). Source is 100% correct - calls HSD_OBJECT_PARENT_INFO(&hsdJObj)->init(o), then
            # on success sets jobj->flags=JOBJ_MTX_DIRTY and scale.x/y/z=1.0f (reusing the real
            # shared constant lbl_8065FB00 via a local `one` variable to force the single-load/
            # triple-store CSE retail uses, matching the technique from HSD_LObjGetLightVector).
            # Total size matches retail exactly (0x64) and every byte matches except a pure
            # INSTRUCTION SCHEDULING swap: retail orders `li r0,0x40(flags const); lfs f0,one; stw
            # r0,flags; li r3,0(status); stfs x3`, while every C statement ordering tried here
            # (float-before-flags, flags-before-float-before-status, status-first matching vendored
            # literal order) produced `li r0; li r3; stw; lfs; stfs x3` or similar - MWCC's scheduler
            # groups the two independent GPR immediate loads together regardless of source order,
            # rather than interleaving the float load between them like retail does. Tried 3 distinct
            # statement orderings; none reproduced retail's specific interleaving. Same class as
            # other scheduling/branch-shape residuals in this project that don't respond to source
            # restructuring. Kept on disk, not wired.
            # Object(Matching, "sysdolphin/baselib/hsdjobjinit_801c8cf4.c"),
            Object(Matching, "sysdolphin/baselib/hsdjobjalloc_801c77f0.c"),
            # DEFERRED: sysdolphin/baselib/hsdjobjsetcurrent_801c784c.c (HSD_JObjSetCurrent,
            # 0x801C784C, size 0x190). Source hand-inlines `ref_INC(jobj)` (matches perfectly) and
            # a manual copy of `HSD_JObjUnref(current_jobj)`'s body (matches perfectly structurally,
            # same shared-base-offset string technique as HSD_JObjResolveRefs) - total size matches
            # retail exactly (0x190) after moving the `current_jobj` load to the top of the function
            # (fixed an earlier extra `mr` copy instruction). The ONLY remaining residual is the
            # exact same object.h `ref_DEC()` register-choice issue as the already-deferred
            # `HSD_JObjUnref` (0x801C6CD8): picks r3 for its internal `ret` where retail picks r0.
            # Tried a ternary form (`cond ? ref_DEC(x) : 0` instead of `&&`) and a fully hand-inlined
            # local `my_ref_DEC` duplicate instead of calling the header's version - the ternary made
            # no difference, the hand-inlined duplicate compiled 16 bytes SMALLER (a different,
            # worse shape). Reverted to the closest version (using the real `ref_DEC()`, exact size
            # match, single register-letter residual throughout). Same "unfixable via source
            # restructuring, needs a second real caller of object.h's ref_DEC to cross-check" class
            # noted for HSD_JObjUnref. Kept on disk, not wired.
            # Object(Matching, "sysdolphin/baselib/hsdjobjsetcurrent_801c784c.c"),
            Object(Matching, "sysdolphin/baselib/hsdwobjreqanim_801d2f08.c"),
            Object(Matching, "sysdolphin/baselib/hsdidinitallocdata_801d2c88.c"),
            Object(Matching, "sysdolphin/baselib/hsdidsetup_801d2cb8.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "sysdolphin/baselib/hsdidinserttotable_801d2ce8.c", extra_cflags=["-i include/stl", "-use_lmw_stmw off"]),
            Object(Matching, "sysdolphin/baselib/hsdstateinvalidate_801a9f7c.c", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "sysdolphin/baselib/hsdstateinvalidaterendermode_801a9fdc.c"),
            Object(Matching, "sysdolphin/baselib/hsdsetuprendermodewithcustompe_801aa318.c", extra_cflags=["-Cpp_exceptions on"]),
            # DEFERRED: not byte-exact -- logic/structure/instruction-opcodes now confirmed
            # 100% correct (same mnemonics, same field offsets, same branch topology as
            # retail) after caching each HSD_PEDesc field into a named local once and
            # applying (u32) casts to the u8-vs-u8 comparisons. Remaining gap is PURE
            # register-numbering: retail cycles through r26-r31 across the 8 cache-check
            # blocks in a different assignment than our compile, despite matching
            # instruction-for-instruction otherwise. ~316 lines differ only in register
            # number (e.g. r30 vs r29), not opcode/offset. Tried reordering local
            # declarations with no effect. See project memory for full diagnosis.
            # Object(Matching, "sysdolphin/baselib/hsdsetuppemode_801aa3a8.c", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "sysdolphin/baselib/hsdstateinvalidatevtxattr_801aa034.c", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "sysdolphin/baselib/hsdstateinvalidateprimitive_801aa054.c"),
            Object(Matching, "sysdolphin/baselib/hsdstatesetalphaupdate_801aa070.c", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "sysdolphin/baselib/hsdstatesetcolorupdate_801aa0b8.c", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "sysdolphin/baselib/hsdstatesetzmode_801aa164.c", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "sysdolphin/baselib/hsdstatesetcullmode_801aa1f4.c", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "sysdolphin/baselib/hsdsetmaterialshininess_801aa294.c"),
            # DEFERRED: not byte-exact -- float-clamp register-choice/scheduling residual
            # (extra fmr moves, f0/f1 vs retail's f2). See project memory.
            # Object(Matching, "sysdolphin/baselib/hsdsetmaterialcolor_801aa2a4.c", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "sysdolphin/baselib/hsdstatesetlinewidth_801aa100.c", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "sysdolphin/baselib/hsdstatesetpointsize_801aa230.c", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "sysdolphin/baselib/hsdidremovebyidfromtable_801d2dd4.c"),
            Object(Matching, "sysdolphin/baselib/hsdidgetdatafromtable_801d2e80.c"),
            Object(Matching, "sysdolphin/baselib/wobjupdatefunc_801d2fbc.c"),
            Object(Matching, "sysdolphin/baselib/hsdwobjaddanim_801d2f54.c"),
            Object(Matching, "sysdolphin/baselib/hsdwobjsetposition_801d32bc.c"),
            Object(Matching, "sysdolphin/baselib/wobjload_801d3148.c"),
            Object(Matching, "sysdolphin/baselib/hsdwobjinit_801d31b0.c"),
            Object(Matching, "sysdolphin/baselib/hsdwobjloaddesc_801d3224.c"),
            Object(Matching, "sysdolphin/baselib/hsdwobjsetpositionx_801d3304.c", extra_cflags=["-sdatathreshold 12"]),
            Object(Matching, "sysdolphin/baselib/hsdwobjsetpositiony_801d33d8.c", extra_cflags=["-sdatathreshold 12"]),
            Object(Matching, "sysdolphin/baselib/hsdwobjsetpositionz_801d34ac.c", extra_cflags=["-sdatathreshold 12"]),
            Object(Matching, "sysdolphin/baselib/hsdwobjgetposition_801d3580.c", extra_cflags=["-sdatathreshold 12"]),
            Object(Matching, "sysdolphin/baselib/hsdwobjalloc_801d3668.c"),
            Object(Matching, "sysdolphin/baselib/hsdlistinitallocdata_801d3b10.c"),
            Object(Matching, "sysdolphin/baselib/hsdslistalloc_801d3b54.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "sysdolphin/baselib/hsdslistallocandappend_801d3bb0.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "sysdolphin/baselib/hsdslistallocandprepend_801d3c30.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "sysdolphin/baselib/hsdslistappendlist_801d3cb0.c"),
            Object(Matching, "sysdolphin/baselib/hsdslistprependlist_801d3d20.c"),
            Object(Matching, "sysdolphin/baselib/hsdslistremove_801d3d70.c"),
            # Near-miss: not byte-exact -- double-indirect callback dispatch register shifted by one (same quirk as closeandcleanupdatastructures.c). See project memory.
            # Object(Matching, "game/system/cleanupfielderaction.c"),
            # Near-miss: not byte-exact -- double-indirect callback dispatch register shifted by one. See project memory.
            # Object(Matching, "game/system/closeandcleanupdatastructures.c"),
            Object(Matching, "game/system/renderdepthfx.cpp"),
            Object(Matching, "game/system/initgraphicsettings.cpp"),
            Object(Matching, "game/system/checkisplayingeffect.c"),
            Object(Matching, "game/system/configureeffectbuffer.cpp"),
            Object(Matching, "game/system/iswithinrange.cpp"),
            Object(Matching, "game/system/setelementinarray.cpp"),
            # DISABLED: not byte-matching -- compiles to ~26% of declared size, likely missing check blocks. See project memory.
            # Object(Matching, "game/system/updatejunktypeavailabilityflags.cpp"),
            Object(Matching, "game/system/updateobjectsinlinkedlistwithmask.cpp"),
            Object(Matching, "game/system/getdat.cpp"),
            Object(Matching, "game/system/handletextobjects.cpp"),
            Object(Matching, "game/system/isprocessconditionmet.cpp"),
            Object(Matching, "game/system/leadingzeros.cpp"),
            Object(Matching, "game/system/copyvector3.cpp"),
            # DEFERRED: not byte-exact -- instruction-scheduling residual (also present in the neighboring, already-Matching copyVector3). See project memory.
            Object(Matching, "game/system/copyvector3_2.c"),
            Object(Matching, "game/system/getvalueatoffset_e7e20.c"),
            Object(Matching, "game/gameobjects/getfieldat0x80c.c"),
            Object(Matching, "game/system/setvec3at0xa4.c"),
            Object(Matching, "game/system/hsddobjsetcurrent.c"),
            Object(Matching, "game/graphics/game_gx.cpp"),
            Object(Matching, "game/globals.cpp"),
            Object(Matching, "game/system/destructor_80008344.cpp"),
            Object(Matching, "game/system/cgschandestructor.cpp"),
            Object(Matching, "game/system/cpadone_dt.cpp"),
            Object(Matching, "game/gameobjects/xobjleticker_dt.cpp"),
            Object(Matching, "game/system/ringgetnext.c"),
            Object(Matching, "game/system/getobjectfield_801b8e5c.cpp"),
            Object(Matching, "game/system/setflagonobject.c"),
            Object(Matching, "game/system/clearnodeflag.c"),
            Object(Matching, "game/system/ringgetstart.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjgetinterestwobj_801c0164.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjgeteyepositionwobj_801c01a4.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjgetinterest_801c01e4.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjsetinterest_801c0250.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjgeteyeposition_801c02bc.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjseteyeposition_801c0328.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjsetmtxdirty_801c0cc8.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjgetinvviewingmtxptrdirect_801c0d58.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjsetfov_801c1450.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjsetaspect_801c1470.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjsettop_801c1490.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjsetbottom_801c14c4.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjsetleft_801c14f8.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjsetright_801c152c.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjgetnear_801c1560.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjsetnear_801c1578.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjgetfar_801c1588.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjsetfar_801c15a0.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjsetscissor_801c15b0.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjsetscissorx4_801c15cc.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjsetviewport_801c15e8.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjsetviewportf_801c1674.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjsetviewportfx4_801c16a0.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjgetprojectiontype_801c16bc.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjsetprojectiontype_801c16d4.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjsetfrustum_801c16e4.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjsetortho_801c1708.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjgetflags_801c172c.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjsetflags_801c1734.c"),
            Object(Matching, "sysdolphin/baselib/hsdaobjsetrewindframe_801bd020.c"),
            Object(Matching, "sysdolphin/baselib/hsdaobjsetendframe_801bd030.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjclearflags_801c174c.c"),
            Object(Matching, "sysdolphin/baselib/hsdcobjgetcurrent_801c1764.c"),
            Object(Matching, "sysdolphin/baselib/hsdpobjclearmtxmark_801acb64.c"),
            Object(Matching, "sysdolphin/baselib/hsdtobjremoveall_801aeedc.c", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "sysdolphin/baselib/hsdtobjgetcurrentbytype_801b10a4.c"),
            Object(Matching, "sysdolphin/baselib/hsdmobjunset_801ba30c.c"),
            Object(Matching, "sysdolphin/baselib/hsdlobjgetcurrentbytype_801be7f4.c"),
            Object(Matching, "sysdolphin/baselib/hsdlightid2index_801be828.c"),
            # DEFERRED: sysdolphin/baselib/hsdindex2lightid_801be914.c (HSD_Index2LightID,
            # 0x801BE914, size 0x70). Source is a 100%-correct byte-for-byte switch->jump-table
            # reconstruction (confirmed via isolated .o disasm diff), but MWCC emits its own local
            # jump-table data object ("@86") rather than reusing retail's existing named symbol
            # jumptable_80259CC8 (.data:0x80259CC8, size 0x24, already declared in symbols.txt).
            # Adding a matching `.data start:0x80259CC8 end:0x80259CEC` split entry fixes all 16
            # REL modules (verified via shasum -c), but the main DOL link still places the table
            # at the wrong spot, shifting .text section 1's address/size (visible via `dtk elf
            # disasm` and direct DOL section-header inspection) and failing only the DOL checksum.
            # Root cause is in how the top-level DOL link orders/places this specific local jump
            # table relative to surrounding auto-generated data blobs - not a C-source issue.
            # Object(Matching, "sysdolphin/baselib/hsdindex2lightid_801be914.c"),
            Object(Matching, "sysdolphin/baselib/hsdlobjsetcolor_801be984.c"),
            Object(Matching, "sysdolphin/baselib/hsdlobjgetcolor_801be990.c"),
            Object(Matching, "sysdolphin/baselib/hsdlobjsetspot_801be99c.c"),
            Object(Matching, "sysdolphin/baselib/hsdlobjsetdistattn_801be9b0.c"),
            Object(Matching, "sysdolphin/baselib/hsdlobjsetposition_801be9c8.c"),
            Object(Matching, "sysdolphin/baselib/hsdlobjaddanim_801bf08c.c"),
            Object(Matching, "sysdolphin/baselib/hsdlobjgetpositionwobj_801beb58.c"),
            Object(Matching, "sysdolphin/baselib/hsdlobjgetinterestwobj_801beb70.c"),
            # DEFERRED: sysdolphin/baselib/hsdlobjgetlightvector_801bd3f8.c (HSD_LObjGetLightVector,
            # 0x801BD3F8, size 0x124). The vendored source was substantially INCOMPLETE - real retail has
            # THREE behaviors missing from lobj.c's version: (1) an explicit `if (dir == NULL) isZero = -1;`
            # guard on the OUTPUT parameter (never in the vendored source at all); (2) an epsilon check using
            # `<=` (FLT_MIN, via the real shared constant lbl_8065FA40) across all 3 axes to detect a
            # degenerate/zero light-direction vector; (3) a hardcoded (0,0,1) fallback direction (via real
            # shared constants lbl_8065FA30=0.0f/lbl_8065FA34=1.0f) written into `dir` whenever step 1 or 2
            # triggers - none of which the vendored `lobj.c` implements (it just unconditionally normalizes
            # whatever PSVECSubtract produces). Also safely renamed 2 more verified callees along the way:
            # `HSD_LObjGetPosition` (0x801BEA50) and `HSD_LObjGetInterest` (0x801BEB18) - both structurally
            # confirmed byte-for-byte against their own already-known vendored bodies. After the full
            # reconstruction, logic is 100% correct and matches for the entire prologue/subtract/normalize/
            # fallback-store portion - the ONLY remaining residual is the `dir == NULL` guard's branch SHAPE:
            # retail keeps a redundant `beq/bne` pair (two separate `li r0,-1` sites, one per triggering
            # condition) where our compile naturally collapses the equivalent logic to a single `bne`, plus
            # one cosmetic register-number difference (f0 vs f1) in the fallback-store block. Tried the
            # separate if/else-if form, an OR-combined single condition, `!dir` vs `dir == NULL`, and
            # dir-truthy-first ordering - none reproduced retail's specific redundant-branch shape. Same
            # "unfixable via source restructuring" class as other control-flow-canonicalization residuals
            # documented elsewhere in this project. Kept on disk with the full reconstruction - very close
            # (4 bytes off) and a good candidate to revisit.
            # Object(Matching, "sysdolphin/baselib/hsdlobjgetlightvector_801bd3f8.c"),
            Object(Matching, "sysdolphin/baselib/hsdlobjsetinterest_801bea90.c"),
            Object(Matching, "sysdolphin/baselib/hsdpobjaddanimall_801aea6c.c", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "sysdolphin/baselib/hsdpobjclearflags_801aeb70.c"),
            Object(Matching, "sysdolphin/baselib/hsdpobjsetflags_801aeb88.c"),
            Object(Matching, "sysdolphin/baselib/hsdpobjremoveall_801ae554.c", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "sysdolphin/baselib/hsddobjremoveall_801b7d8c.c"),
            Object(Matching, "sysdolphin/baselib/hsddobjalloc_801b7e00.c", extra_cflags=["-sdatathreshold 12"]),
            Object(Matching, "sysdolphin/baselib/hsddobjresolverefsall_801b7e5c.c"),
            Object(Matching, "sysdolphin/baselib/hsdmobjaddanim_801b8f04.c"),
            Object(Matching, "sysdolphin/baselib/hsdmobjremove_801ba444.c"),
            # DEFERRED: sysdolphin/baselib/mobjinfoinit_801ba718.c (MObjInfoInit, 0x801BA718,
            # size 0xB0). Major finding: HSD_MObjInfo (mobj.h) was missing a 6th function-pointer
            # field entirely absent from vendored source - `update_func` (type HSD_ObjUpdateFunc,
            # confirmed at real offset 0x4C, pushing `unset` from the vendored-claimed 0x4C to the
            # REAL 0x50) - added to the header as a additive, safe fix (confirmed no other code
            # references those offsets in a way that would break). All 8 function-pointer targets
            # correctly identified and renamed via disasm (MObjRelease, MObjAmnesia, HSD_MObjSetup,
            # HSD_MObjUnset already known, MObjLoad, MObjMakeTExp, MObjSetupTev, and the previously
            # entirely-undocumented MObjUpdateFunc), plus hsdInitClassInfo itself. Also confirmed
            # the "sysdolphin_base_library"/"hsd_mobj" strings live at hsdMObj+0x148/+0x160 (decoded
            # directly from the raw data blob, base-offset technique). Source is 100% logically
            # correct and links clean - the ONLY residual: retail keeps a redundant register copy
            # (`addi r10,r31,0x0` before reusing r10 for all 8 struct-field stores) that this
            # compile optimizes away by using r31 directly, a 4-byte/1-instruction difference. Tried
            # 3 source variations (HSD_MObjInfo* local, HSD_ClassInfo* local, char* base local with
            # macro-applied-at-each-site) - all produced the identical residual. Same
            # "redundant-copy-elision, unfixable via source restructuring" class as
            # HSD_JObjSetCurrent's residual. HIGH VALUE for a future attempt or as a template: this
            # confirms the InfoInit boilerplate pattern (shared across EVERY object type in this
            # project - aobj/pobj/lobj/dobj/tobj/jobj/wobj/robj/fobj/cobj all have one, none landed)
            # is tractable with this exact technique once the redundant-copy quirk is solved. Kept
            # on disk, not wired. mobj.h's added field IS kept (safe/necessary regardless).
            # Object(Matching, "sysdolphin/baselib/mobjinfoinit_801ba718.c"),
            Object(Matching, "sysdolphin/baselib/hsdaobjinitallocdata_801ba7c8.c"),
            Object(Matching, "sysdolphin/baselib/hsdaobjgetflags_801ba7f8.c"),
            Object(Matching, "sysdolphin/baselib/hsdaobjsetflags_801ba810.c"),
            Object(Matching, "sysdolphin/baselib/hsdaobjinitendcallback_801ba82c.c"),
            # DEFERRED: sysdolphin/baselib/hsdaobjalloc_801bac28.c (HSD_AObjAlloc, 0x801BAC28, size 0x6C)
            # Source is verbatim-correct (matches vendored src/sysdolphin/baselib/aobj.c exactly, including
            # the HSD_ASSERT(489, new) line number - confirmed correct via disasm, li r4,0x1e9 = 489 decimal,
            # not a stale-line-number bug this time). Every instruction/byte matches retail except a pure
            # 2-instruction scheduling swap for the final `new->flags = AOBJ_NO_ANIM; new->framerate =
            # lbl_8065FA24;` pair: retail computes BOTH independent values first (lis+lfs) THEN does both
            # stores (stw+stfs), interleaving a `mr r3,r31` (return-value setup) between the two stores; our
            # compile computes flags/stores-it, THEN loads/stores framerate (no hoisting). Tried 4 source
            # variants: statement order swap, explicit locals for both fields (single and both-swapped
            # declaration order), and `-schedule off` (made it WORSE - broke a second, previously-matching
            # part of the function too). "Unfixable via source restructuring" class - the classic 2-
            # instruction load/store scheduling residual already documented several times in project memory
            # (e.g. checkstatusinverted_800a8494.cpp). Kept on disk, ready for a future attempt.
            # Object(Matching, "sysdolphin/baselib/hsdaobjalloc_801bac28.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "sysdolphin/baselib/hsdaobjremove_801babb8.c"),
            Object(Matching, "sysdolphin/baselib/hsdaobjfree_801bac94.c"),
            Object(Matching, "sysdolphin/baselib/hsdfobjinitallocdata_801c1dd0.c", extra_cflags=["-use_lmw_stmw off"]),
            # DEFERRED: sysdolphin/baselib/hsdalloc_801d426c.c (HSD_Alloc, 0x801D426C, size 0x2C)
            # A trampoline through the swappable memory-hooks table (lbl_8064CA70, a 5-slot function-
            # pointer struct: alloc@0/free@4/unk@8/getHeap@0xc/mallocPhysical@0x10 - confirmed via
            # FUNCTION_CANDIDATES.txt + disasm cross-reference of all 5 call sites). Source is correct
            # (`return lbl_8064CA70.alloc(size);`) but compiles with r4 instead of retail's r6 for the
            # table base register - a pure register-choice residual on a 3-instruction leaf trampoline.
            # Kept on disk; the symbol name (HSD_Alloc) is what matters for other callers (e.g.
            # hsdobjallocaddfree_801d0794.c uses it), not this file's own byte-match.
            # Object(Matching, "sysdolphin/baselib/hsdalloc_801d426c.c"),
            Object(Matching, "sysdolphin/baselib/hsdgetnbbits_801d0524.c"),
            Object(Matching, "sysdolphin/baselib/hsdfobjfree_801c3b20.c"),
            Object(Matching, "sysdolphin/baselib/hsdobjsetheap_801d0684.c"),
            # DEFERRED: sysdolphin/baselib/hsdobjallocaddfree_801d0794.c (HSD_ObjAllocAddFree, 0x801D0794,
            # size 0x250). Found and fixed TWO real vendored-source bugs (confirmed via full disasm trace):
            # (1) the vendored `pool_start = HSD_MemAlloc(pool_size);` in the `obj_heap.top==0` branch is
            # WRONG - real retail calls a completely different function, `HSD_Alloc(pool_size, data->align,
            # 1)` (3 args, going through the swappable memory-hooks table at lbl_8064CA70 - see HSD_Alloc's
            # own deferred entry above), not HSD_MemAlloc (memory.c's OSAllocFromHeap-based implementation)
            # at all - a genuine call-target divergence, not just a bug in constants. (2) the vendored
            # `obj_heap.remain -= pool_size;` at the end of that same else-branch does NOT exist in real
            # retail at all - removing it was required to match. Also reused the `data->align` raw-value fix
            # from HSD_ObjAllocInit (computes `(curr + (align-1)) & ~(align-1)` transiently, matching the
            # now-corrected field semantics). After both fixes the function is 100% logically/structurally
            # correct and matches for the ENTIRE prologue/branch-selection/final-store portion - the ONLY
            # remaining diff (102 lines, but same total instruction count/opcodes) is a pure register-swap
            # (r8<->r9) confined to the 8x-unrolled linked-list-init loop's per-iteration `data->size` reload
            # - tried 3 source variants (cached local for size - much worse; swapped mul operand order -
            # much worse; swapped which side of the store computes first - no change) without success.
            # "Unfixable via source restructuring" class. Kept on disk, very close to landing.
            # Object(Matching, "sysdolphin/baselib/hsdobjallocaddfree_801d0794.c"),
            Object(Matching, "sysdolphin/baselib/hsdobjalloc_801d09e4.c"),
            Object(Matching, "sysdolphin/baselib/hsdobjfree_801d0b34.c"),
            Object(Matching, "sysdolphin/baselib/hsdobjallocinit_801d0b5c.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "sysdolphin/baselib/hsdrobjinitallocdata_801d0c80.c"),
            # DEFERRED: not byte-exact -- bit-test codegen/tail-merging residual. See project memory.
            Object(Matching, "game/system/getvalueifbitsetinmask.c"),
            Object(Matching, "game/system/getvalueatoffset_801c7040.cpp"),
            Object(Matching, "game/system/psquatscale.cpp"),
            Object(Matching, "Dolphin/mtx/psvecnormalize.cpp"),
            # DEFERRED: not byte-exact -- scheduling residual, same class as addpsvecwithscalar.c. See project memory.
            Object(Matching, "game/system/scalequaternion.c"),
            Object(Matching, "game/system/generaterandomnumber.c"),
            Object(Matching, "game/system/updateflagstate.c"),
            Object(Matching, "sysdolphin/baselib/hsdstateinvalidatecolorchannel_801b8dc4.c", extra_cflags=["-i include/stl"]),
            Object(Matching, "sysdolphin/baselib/hsdstateinvalidatetevstage_801b8e1c.c"),
            Object(Matching, "sysdolphin/baselib/hsdstateinvalidatetevregister_801b8e28.c"),
            Object(Matching, "sysdolphin/baselib/hsdstateinvalidatetexcoordgen_801b8e48.c"),
            Object(Matching, "sysdolphin/baselib/hsdmobjsetcurrent_801b8e54.c"),
            Object(Matching, "game/system/settranslationx.c"),
            Object(Matching, "game/game.cpp"),
            # DISABLED: not byte-matching -- CheckTitleLogo() caused a title-screen hang. See project memory.
            # Object(Matching, "game/title.cpp"),
            Object(Matching, "game/system/tablelookup_801a4ec8.cpp"),
            Object(Matching, "game/unk_unused/unk_functions.cpp"),
            # DEFERRED: not byte-exact -- 1-instruction guard-clause collapse residual. See project memory.
            # Object(Matching, "game/system/hsdshadowaddobject.cpp", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "game/system/getobjectfield_801905a4.cpp"),
            Object(Matching, "game/system/getobjectfield_801905bc.cpp"),
            Object(Matching, "game/system/getobjectfromid_801908e0.cpp"),
            Object(Matching, "game/system/cfile.cpp"),
            Object(Matching, "game/system/fn_8019fd78.cpp"),
            # DEFERRED: not byte-exact -- branchless bit-trick optimization residual. See project memory.
            # Object(Matching, "game/system/shutdowndevice.c", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "game/system/getviewportaspect.cpp"),
            Object(Matching, "game/system/hsdaddshadowobjects.cpp"),
            Object(Matching, "game/system/getcameravaluesearch.cpp"),
            # DISABLED: not byte-matching -- dead-zero-mask-idiom bug (constant folded away that retail's build didn't fold). See project memory.
            # Object(Matching, "game/system/getcameravalue.cpp"),
            Object(Matching, "game/system/getvalflag.cpp"),
            # DEFERRED: not byte-exact -- 2-instruction scheduling residual. See project memory.
            # Object(Matching, "game/system/checkstatusinverted_800a8494.cpp"),
            Object(Matching, "game/system/checkstatus.cpp"),
            Object(Matching, "game/system/normalizedbytevalues.cpp"),
            # DISABLED: not byte-matching -- float-classification tail uses a different instruction sequence than retail (dolsqrtf cluster bug). See project memory.
            # Object(Matching, "game/system/calcdistancefromorigin.cpp"),
            # DISABLED: not byte-matching -- dead-zero-mask-idiom bug, 1 of ~8 functions sharing this pattern. See project memory.
            # Object(Matching, "game/system/isflag4setinparams.cpp"),
            Object(Matching, "game/system/miscsmallaccessors1.cpp"),
            Object(Matching, "game/system/checkplayerdistfromground.cpp"),
            # DISABLED: not byte-matching -- compiles short vs declared size, a genuine structural gap. See project memory.
            # Object(Matching, "game/system/computewrappeddistance.cpp"),
            # DISABLED: not byte-matching -- shares the dead-zero-mask-idiom bug. See project memory.
            # Object(Matching, "game/system/miscsmallaccessors2a.cpp"),
            Object(Matching, "game/system/miscsmallaccessors2.cpp"),
            # DISABLED: not byte-matching -- shares the dead-zero-mask-idiom bug (4 of 13 functions in this range). See project memory.
            # Object(Matching, "game/system/miscsmallaccessors3a.cpp"),
            # DISABLED: not byte-matching -- shares the dolsqrtf-tail classification bug. See project memory.
            # Object(Matching, "game/system/miscsmallaccessors3.cpp"),
            # DISABLED: not byte-matching -- shares the dolsqrtf-tail classification bug. See project memory.
            # Object(Matching, "game/system/miscsmallaccessors4.cpp"),
            Object(Matching, "game/system/miscsmallaccessors5.cpp"),
            Object(Matching, "game/system/findmatchingbucket.cpp"),
            Object(Matching, "game/system/setobjectflagsandtimer.cpp"),
            Object(Matching, "game/system/resetjobjmatrixdirty.cpp"),
            Object(Matching, "game/system/miscsmallaccessors6.cpp"),
            Object(Matching, "game/system/miscsmallaccessors7.cpp"),
            Object(Matching, "game/system/handlemodelloadinganimating.cpp"),
            # DISABLED: causes a real runtime crash (DSI in a heap-allocator area). See project memory.
            # Object(Matching, "game/system/handlefielderdesirestate.cpp"),
            Object(Matching, "game/system/getboxlengths.cpp"),
            Object(Matching, "game/system/processdatawithinit.cpp"),
            # NonMatching: causes a hang at yes/no prompts (MainGame+0x1b14 flag never gets set correctly).
            # Root cause found: source had wrong obj-relative offsets (missing +0x10000, e.g. 0x3394 should be
            # 0x13394) and a wrong float constant (0.0f should reference lbl_8065D35C, which equals 1.0f).
            # Both fixed in the .cpp, but MWCC hoists the ScaledRandomAngle loop-invariant loads into
            # callee-saved float regs (bigger stack frame) in retail; our version doesn't trigger that
            # optimization, so it's not byte-exact yet. Left disabled (using retail bytes) until resolved.
            # Object(Matching, "game/system/initparticleemission.cpp"),
            Object(Matching, "game/system/updateaudiostreamstate.cpp"),
            Object(Matching, "game/system/childobjdispatch1.cpp"),
            Object(Matching, "game/system/childobjdispatch2.cpp"),
            Object(Matching, "game/system/childobjdispatch3.cpp"),
            Object(Matching, "game/system/findandregisterfreeslot.cpp"),
            Object(Matching, "game/system/updateratelimitedvalue.cpp"),
            Object(Matching, "game/system/initparam1.cpp"),
            Object(Matching, "game/system/addpsvectorwithscalar.cpp"),
            # DISABLED: not byte-exact -- pure register-scheduling permutation (unfixable via source restructuring). See project memory.
            Object(Matching, "game/system/resourceptr4.cpp"),
            # Object(Matching, "game/system/getmemoryaddressatindex.cpp"),
            Object(Matching, "game/system/computevectorlength.cpp"),
            Object(Matching, "game/system/computeeuclideandistance.cpp"),
            Object(Matching, "game/system/computevectorlengthsquared.cpp"),
            Object(Matching, "game/system/psvecmathcluster.cpp"),
            Object(Matching, "game/system/crossproductscalar.cpp"),
            Object(Matching, "game/system/psvecmathcluster2.cpp"),
            # NonMatching: causes the player to spawn holding an invisible item on scene load.
            # Same bug class as initparticleemission.cpp: obj-relative offsets 0x58a0/0x5894/0x5898 were
            # missing +0x10000 (real offsets 0x158a0/0x15894/0x15898), and three 0.0f vtable-call args
            # should have been lbl_8065D35C (1.0f). Both fixed in the .cpp, but remaining register-
            # allocation/instruction-scheduling differences from MWCC keep it from being byte-exact.
            # Left disabled (using retail bytes) until resolved.
            # Object(Matching, "game/system/processfielderdesire.cpp"),
            Object(Matching, "game/system/resetfielderframestate.cpp"),
            # DISABLED: not byte-matching -- compiles to ~30% of declared size. See project memory.
            # Object(Matching, "game/system/updatefielderchildsearch.cpp"),
            # DISABLED: not byte-matching -- compiles to ~23% short of declared size. See project memory.
            # Object(Matching, "game/system/updatefielderchildsearch2.cpp"),
            Object(Matching, "game/system/processchibimodeldata.cpp"),
            Object(Matching, "game/system/handlefielderdesire.cpp"),
            Object(Matching, "game/system/loadfielderdatafile.cpp"),
            Object(Matching, "game/system/resetprojectilescale.cpp"),
            Object(Matching, "game/system/handlefielderstatetransition.cpp"),
            # DISABLED: not byte-matching -- compiles to ~34% short of declared size. See project memory.
            # Object(Matching, "game/system/updatefielderweightvec.cpp"),
            Object(Matching, "game/system/clearprojectilefields.cpp"),
            Object(Matching, "game/system/initfielderobject.cpp"),
            Object(Matching, "game/system/setobjstateandnotify.cpp"),
            Object(Matching, "game/system/projectiledestructor.cpp"),
            Object(Matching, "game/system/destructor_800bc4dc.cpp"),
            Object(Matching, "game/system/initfielderdevicestate.cpp"),
            # DISABLED: not byte-matching -- compiles to ~28% short of declared size. See project memory.
            # Object(Matching, "game/system/initfielderdevicetables.cpp"),
            # DEFERRED: extremely close -- 1 instruction off in a mask-idiom sub-expression. See project memory.
            # Object(Matching, "game/gameobjects/cameraactionleticker_update.cpp"),
            # DEFERRED: not byte-exact -- pure register-choice residual. See project memory.
            # Object(Matching, "game/gameobjects/cameraactionleticker_reset.cpp"),
            Object(Matching, "game/gameobjects/cameraactionleticker_copyvec.cpp"),
            Object(Matching, "game/gameobjects/cameraactionleticker_getters.cpp"),
            Object(Matching, "game/gameobjects/cameraaction.cpp"),
            Object(Matching, "game/gameobjects/xobj.cpp"),
            Object(Matching, "game/gameobjects/stubreturn_80025aa0.cpp"),
            # DISABLED: not byte-exact -- pure register-scheduling residual (unfixable via source restructuring). See project memory.
            Object(Matching, "game/system/addpsvecwithscalar.c"),
            Object(Matching, "game/system/destructor_80012a34.cpp"),
            Object(Matching, "game/system/incrementinteger.cpp"),
            Object(Matching, "game/system/wrapper_8001355c.cpp"),
            Object(Matching, "game/system/stubreturn_8001357c.cpp"),
            Object(Matching, "game/system/stubreturn_80015640.cpp"),
            Object(Matching, "game/system/flagutil.cpp"),
            Object(Matching, "game/system/vecscale.cpp"),
            Object(Matching, "game/system/initcameraparams.cpp"),
            Object(Matching, "game/system/resetglobals.cpp"),
            Object(Matching, "game/system/resetcameradata.cpp"),
            Object(Matching, "game/system/destructor_8006db80.cpp"),
            Object(Matching, "game/system/isbitset.cpp"),
            Object(Matching, "game/system/lookuptable2level.cpp"),
            Object(Matching, "game/system/getplayerprompt.cpp"),
            Object(Matching, "game/system/normalizedposition.cpp"),
            # DEFERRED: not byte-exact -- load/store interleaving scheduling residual. See project memory.
            Object(Matching, "game/system/initializespatialsettings_8006656c.cpp"),
            Object(Matching, "game/system/floatcompare.cpp"),
            # DEFERRED: not byte-exact -- fcmpu-vs-fcmpo comparison-idiom residual. See project memory.
            Object(Matching, "game/system/floatcompare2_800665fc.cpp"),
            Object(Matching, "game/system/valonoff.cpp"),
            Object(Matching, "game/system/setglobalfield_80068b98.cpp"),
            Object(Matching, "game/system/getresultfromglobal.cpp"),
            Object(Matching, "game/system/getshortfields.cpp"),
            Object(Matching, "game/system/resourcegetters2.cpp"),
            Object(Matching, "game/system/dataarambaseaddr.cpp"),
            Object(Matching, "game/system/printmoduleinfo.cpp"),
            Object(Matching, "game/system/closeanddatacleanup.cpp"),
            Object(Matching, "game/system/startloadmoduleexec.cpp"),
            Object(Matching, "game/system/initdevicedata.cpp"),
            Object(Matching, "game/system/deviceindextables.cpp"),
            Object(Matching, "game/system/getmaskedstagevalue.cpp"),
            Object(Matching, "game/system/findstageindex.cpp"),
            Object(Matching, "game/system/getstageoffsetext4.cpp"),
            Object(Matching, "game/system/stagelookup.cpp"),
            Object(Matching, "game/system/getstagecount.cpp"),
            Object(Matching, "game/system/getvalfromptr.cpp"),
            Object(Matching, "game/system/resourceptr1.cpp"),
            Object(Matching, "game/system/resourceu16a.cpp"),
            Object(Matching, "game/system/resourceptr2.cpp"),
            Object(Matching, "game/system/resourceu8extra.cpp"),
            Object(Matching, "game/system/resourceu16b.cpp"),
            Object(Matching, "game/system/resourcebitfield.cpp"),
            Object(Matching, "game/system/resourceptr3.cpp"),
            # DISABLED: not byte-matching -- compiles to ~19% short of declared size despite being a carefully-verified state machine. See project memory.
            # Object(Matching, "game/system/handlemoduleloading.cpp"),
            Object(Matching, "game/system/resourcerange.cpp"),
            Object(Matching, "game/system/checkmainflags.cpp"),
            Object(Matching, "game/system/resourcevalues.cpp"),
            Object(Matching, "game/system/cgamesfx.cpp"),
            Object(Matching, "game/system/audiostate.cpp"),
            Object(Matching, "game/system/stringregistry.cpp"),
        ],
    },
]

if args.mode == "configure":
    # Write build.ninja and objdiff.json
    generate_build(config)

elif args.mode == "progress":
    # Print progress and write progress.json
    config.progress_each_module = args.verbose
    calculate_progress(config)
else:
    sys.exit("Unknown mode: " + args.mode)