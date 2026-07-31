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
            Object(Matching, "Dolphin/gx/SetFieldsAt0xc0x10.c"),
            # DEFERRED: not byte-exact -- bitfield-width + register-reload residuals. See project memory.
            Object(Matching, "Dolphin/gx/gxfiforeadenable_80185d7c.c"),
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
            Object(Matching, "Dolphin/dvd/stubreturn_8016dc5c.c"),
            # DEFERRED: not byte-exact -- stack-frame padding residual. See project memory.
            Object(Matching, "Dolphin/dvd/dvdlowwaitmotorstopped_8016eb08.c"),
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
            # DEFERRED: not byte-exact -- bit-test codegen/tail-merging residual. See project memory.
            Object(Matching, "game/system/getvalueifbitsetinmask.c"),
            Object(Matching, "game/system/getvalueatoffset_801c7040.cpp"),
            Object(Matching, "game/system/psquatscale.cpp"),
            Object(Matching, "Dolphin/mtx/psvecnormalize.cpp"),
            # DEFERRED: not byte-exact -- scheduling residual, same class as addpsvecwithscalar.c. See project memory.
            Object(Matching, "game/system/scalequaternion.c"),
            Object(Matching, "game/system/generaterandomnumber.c"),
            Object(Matching, "game/system/updateflagstate.c"),
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
            Object(Matching, "game/system/initparticleemission.cpp"),
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
            Object(Matching, "game/system/processfielderdesire.cpp"),
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