#ifndef xobjs
#define xobjs
#include<Dolphin/vec.h>
#include<cfile.h>
#include<evt.h>
struct CVec : public Vec //0xc
{
    CVec() {};
    virtual ~CVec(){};
};

struct CObjVec : CVec
{
    CVec vecA;
    CVec vecB;
    CObjVec(){};
    virtual ~CObjVec(){};
};

struct CJObj  //Done
{   
    int unkval;
    CVec vecA;
    CVec vecB;
    CVec vecC;
    CJObj(){};
    virtual ~CJObj(){};
};
struct hsdJObj
{
    int unk[246];
};
struct CXObj : CJObj //Done
{
    CJArchive archive;
    CObjVec objVecA, objVecB, objVecC;
    CVec vec;
    // 33 virtuals total (retail vtable slots 0x0c-0x8c), confirmed against the
    // ChibiRobo vtable dump at 0x80227ee8 (see reference-cbr-decomp-layout /
    // project-cbr-decomp-status memory). Only JumpHandler is implemented so far;
    // the rest are unresolved placeholders (empty bodies) named from the Ghidra
    // map where it has a real name, otherwise Unk_<vtable offset>.
    //80025aa4 (0x0c)
    virtual void JumpHandler(double param_1, hsdJObj* param_2, int param_3);
    virtual void process_tree_with_param(){}; //80025b7c (0x10)
    virtual void GetHeightOfJump(){}; //80025c54 (0x14)
    virtual void SetLineHeightForText(){}; //80025d2c (0x18)
    virtual void Unk_1c(){}; //80027a98 (0x1c)
    virtual void update_parameter_value(){}; //80025e04 (0x20)
    virtual void updateJobjWithQuaternion(){}; //80025edc (0x24)
    virtual void updateCameraRotationAndTranslation(){}; //8002608c (0x28)
    virtual void setZPosition(){}; //8002623c (0x2c)
    virtual void translateObject(){}; //80017d1c (0x30)
    virtual void updateTranslation(){}; //80017bb0 (0x34)
    virtual void SceneTransitionTrigger(){}; //80027e88 (0x38)
    virtual void Unk_3c(){}; //80027cfc (0x3c)
    virtual void updateJobjPositionWithQuaternion(){}; //80018334 (0x40)
    virtual void setJobjPositionWithRotation(){}; //80018118 (0x44)
    virtual void Unk_48(){}; //800a36e8 (0x48)
    virtual void AddVertexToMesh(){}; //801a306c (0x4c)
    virtual void ProcessTextureAndInitializeObject(){}; //801a1498 (0x50)
    virtual void Unk_54(){}; //800b7b5c (0x54)
    virtual void updateNodePositionAndCallBack(){}; //801a138c (0x58)
    virtual void update_position_and_maybe_call_handler(){}; //801a1328 (0x5c)
    virtual void update_and_notify_position_components(){}; //801a12c4 (0x60)
    virtual void translateObject3D(){}; //8002657c (0x64)
    virtual void UpdateObjPos(){}; //800263ec (0x68)
    virtual void Unk_6c(){}; //80027b70 (0x6c)
    virtual void updatePositionAndRotation(){}; //80026938 (0x70)
    virtual void updatePositionCoordinates(){}; //800266f8 (0x74)
    virtual void Unk_78(){}; //800a0694 (0x78)
    virtual void normalizeRotationAngles(){}; //801a2030 (0x7c)
    virtual void Unk_80(){}; //800a3f88 (0x80)
    virtual void Unk_84(){}; //80090254 (0x84)
    // Ghidra names this override "cPlayer::PostPhysicsUpdate" on ChibiRobo's
    // concrete vtable -- likely a mixin/multiple-inheritance override, not
    // literally introduced by this class. Kept generic pending investigation.
    virtual void PostPhysicsUpdate(){}; //800a54fc (0x88)
    virtual void HandleJobj(){}; //801a0bcc (0x8c)
    CXObj(){};
    virtual ~CXObj(){};
};
struct CXObjIntp : CXObj //done
{
    char unk[144];
    CJObj obj;
    CXObjIntp(){};
    virtual ~CXObjIntp(){};
};

struct XObj : CXObjIntp //Done
{
    char unk0[12];
    CStatus status;
    CoordInfo coordInfo;
    AttrInfo attrInfo;
    char unk1[24];
    CVec vecA;
    char unk2[1312];
    CVec vecB;
    char unk3[8];
    CEvt objEvt;
    char unk4[8];
    CAnmQueue animQueue;
    char unk5[100];
    CJAnim anim;

    XObj(){};
    virtual ~XObj(){};
};
struct Cursor :  XObj 
{
    Cursor(){};
    virtual ~Cursor(){};
};
struct MenuCursor : Cursor
{
    MenuCursor() {};
    virtual ~MenuCursor() {};
};
struct MenuEx
{
    char unk0[40];
    MenuCursor menuCursor;
    char unk1[16];
    MenuEx() {};
    ~MenuEx() {};
};
struct MenuExSetup
{
    char unk0[4];
    MenuEx menu;
    MenuExSetup() {};
    ~MenuExSetup() {};
};
struct XOBJS
{
    char unk[4568];
    XOBJS(){};
    virtual ~XOBJS(){};
};
struct XObjLeticker : XObj
{
    XObjLeticker() {};
    virtual ~XObjLeticker() {};
};
#endif