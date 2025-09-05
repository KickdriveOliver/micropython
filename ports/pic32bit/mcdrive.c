#include "py/nlr.h"
#include "py/obj.h"
#include "py/runtime.h"
#include "py/binary.h"
//#include "portmodules.h"

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "pic32bit_mphal.h"
#include "../IEC61800/targetlib.h"

//dsPic 16 bit limit: MAXIMUM NUMERIC DATA that can be handeld by python is 536870911 = 0x1fffffff
//! (should not be relevant on PIC32)
//Whne return value is not needed use  
//return mp_const_none;

STATIC mp_obj_t WriteObject(mp_obj_t index, mp_obj_t subindex, mp_obj_t value) {
    int ret=Lib_WriteInt(MP_OBJ_SMALL_INT_VALUE(index), MP_OBJ_SMALL_INT_VALUE(subindex), mp_obj_get_int(value));
    return MP_OBJ_NEW_SMALL_INT(ret);
}

STATIC mp_obj_t ReadObject(mp_obj_t index, mp_obj_t subindex) {
    int32_t returnValue;    	
	Lib_ReadInt(MP_OBJ_SMALL_INT_VALUE(index), MP_OBJ_SMALL_INT_VALUE(subindex), &returnValue);
    return mp_obj_new_int(returnValue);
}

STATIC mp_obj_t WriteControl(mp_obj_t value) {
    Lib_WriteControl(MP_OBJ_SMALL_INT_VALUE(value));
    return mp_const_none;
}

STATIC mp_obj_t SendEmcyMsg(size_t n_args, const mp_obj_t *args) {
    // Compatibility: for error code 0, support old fixed 0x509b error code
    // and less arguments. 
    // e.g. drive.SendEmcyMsg(0x12345678) is equivalent to drive.SendEmcyMsg(0x509b, 0x00, 0x12345678);
    WORD errorCode = 0x509b; 
    BYTE errorRegister = 0;
    DWORD errorNumber = 0;
    if (n_args > 0) {
        errorNumber = mp_obj_get_int(args[0]);
    }
    if (n_args > 1) {
        errorRegister = MP_OBJ_SMALL_INT_VALUE(args[1]);
    }       
    if (n_args > 2) {
        errorCode = MP_OBJ_SMALL_INT_VALUE(args[2]);
    }   
    Lib_SendEmcyMsg(errorNumber, errorRegister, errorCode);
    return mp_const_none;
}

STATIC mp_obj_t EnableDrive(void) {
	int ret= Lib_EnableDrive();
    return MP_OBJ_NEW_SMALL_INT(ret);
}

STATIC mp_obj_t StopMotion(void) {
	Lib_StopMotion();
    return mp_const_none;
}

STATIC mp_obj_t ContinueMotion(void) {
	Lib_ContinueMotion();
    return mp_const_none;
}

STATIC mp_obj_t PowerQuit(void) {
	Lib_PowerQuit();
    return mp_const_none;
}

STATIC mp_obj_t StorePermanent(void) {
	Lib_StorePermanent();
    return mp_const_none;
}

STATIC mp_obj_t ResetToFactory(void) {
	Lib_ResetToFactory();
    return mp_const_none;
}


STATIC mp_obj_t GoPosAbs(mp_obj_t targetPos) {
    Lib_GoPosAbs(0, mp_obj_get_int(targetPos));
    return mp_const_none;
}
STATIC mp_obj_t GoPosRel(mp_obj_t targetPos) {
    Lib_GoPosRel(0, mp_obj_get_int(targetPos));
    return mp_const_none;
}
STATIC mp_obj_t GoVel(mp_obj_t velocity) {
    Lib_GoVel(mp_obj_get_int(velocity));
    return mp_const_none;
}

STATIC mp_obj_t ReadStatusword() {
    WORD returnValue;    	
    Lib_ReadStatusword(&returnValue);
    return MP_OBJ_NEW_SMALL_INT(returnValue);
}

STATIC mp_obj_t SetTargetPos(mp_obj_t targetPos) {
    Lib_SetTargetPos(mp_obj_get_int(targetPos));
    return mp_const_none;
}

STATIC mp_obj_t SetPosVel(mp_obj_t velocity) {
    Lib_SetPosVel(mp_obj_get_int(velocity));
    return mp_const_none;
}

STATIC mp_obj_t SetAcc(mp_obj_t acceleration) {
    Lib_SetAcc(mp_obj_get_int(acceleration));
    return mp_const_none;
}

STATIC mp_obj_t SetDec(mp_obj_t deceleration) {
    Lib_SetDec(mp_obj_get_int(deceleration));
    return mp_const_none;
}

STATIC mp_obj_t GetActualPos() {
    int32_t returnValue;    	
    Lib_GetActualPos(&returnValue);
    return mp_obj_new_int(returnValue);
}

STATIC mp_obj_t SetOpMode(mp_obj_t value) {
    Lib_SetOpMode(MP_OBJ_SMALL_INT_VALUE(value));
    return mp_const_none;
}

STATIC mp_obj_t GetOpMode(void) {
    BYTE returnValue;    	
	Lib_GetOpMode(&returnValue);
    return MP_OBJ_NEW_SMALL_INT(returnValue);
}

STATIC mp_obj_t SetTorque(mp_obj_t torqueValue) {
    Lib_SetTorque(MP_OBJ_SMALL_INT_VALUE(torqueValue));
    return mp_const_none;
}

STATIC mp_obj_t ChkIn(mp_obj_t inputNumber) {
    BYTE ret = Lib_ChkIn(MP_OBJ_SMALL_INT_VALUE(inputNumber));
    return MP_OBJ_NEW_SMALL_INT(ret);
}

STATIC mp_obj_t SetOut(mp_obj_t inputNumber) {
    Lib_SetOut(MP_OBJ_SMALL_INT_VALUE(inputNumber));
    return mp_const_none;
}

STATIC mp_obj_t ClearOut(mp_obj_t inputNumber) {
    Lib_ClearOut(MP_OBJ_SMALL_INT_VALUE(inputNumber));
    return mp_const_none;
}

STATIC mp_obj_t GoHome(size_t n_args, const mp_obj_t *args) {
    if (n_args == 4) {
        int8_t method = MP_OBJ_SMALL_INT_VALUE(args[0]);
        DWORD velocity = mp_obj_get_int(args[1]);
        DWORD acceleration = mp_obj_get_int(args[2]);
        DWORD offset = mp_obj_get_int(args[3]);   
        Lib_GoHome(method, velocity, acceleration,  offset);
    }
    return mp_const_none;
}

STATIC mp_obj_t ChkEnabled(void) {
    BYTE ret = Lib_ChkReady();
    return MP_OBJ_NEW_SMALL_INT(ret);
}

STATIC mp_obj_t ChkReady(void) {
    BYTE ret = Lib_ChkReady();
    return MP_OBJ_NEW_SMALL_INT(ret);
}

STATIC mp_obj_t ChkMoving(void) {
    BYTE ret = Lib_ChkMoving();
    return MP_OBJ_NEW_SMALL_INT(ret);
}
STATIC mp_obj_t ChkError(void) {
    BYTE ret = Lib_ChkError();
    return MP_OBJ_NEW_SMALL_INT(ret);
}

STATIC mp_obj_t ChkMfrStatus(mp_obj_t bitNo) {
    BYTE ret = Lib_ChkMfrStatus(MP_OBJ_SMALL_INT_VALUE(bitNo));
    return MP_OBJ_NEW_SMALL_INT(ret);
}

STATIC MP_DEFINE_CONST_FUN_OBJ_3(drive_WriteObject_obj, WriteObject);
STATIC MP_DEFINE_CONST_FUN_OBJ_2(drive_ReadObject_obj, ReadObject);
STATIC MP_DEFINE_CONST_FUN_OBJ_1(drive_WriteControl_obj, WriteControl);
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(drive_SendEmcyMsg_obj, 1, 3, SendEmcyMsg);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(drive_EnableDrive_obj, EnableDrive);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(drive_StopMotion_obj, StopMotion);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(drive_ContinueMotion_obj, ContinueMotion);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(drive_PowerQuit_obj, PowerQuit);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(drive_StorePermanent_obj, StorePermanent);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(drive_ResetToFactory_obj, ResetToFactory);
STATIC MP_DEFINE_CONST_FUN_OBJ_1(drive_GoPosAbs_obj, GoPosAbs);
STATIC MP_DEFINE_CONST_FUN_OBJ_1(drive_GoPosRel_obj, GoPosRel);
STATIC MP_DEFINE_CONST_FUN_OBJ_1(drive_GoVel_obj, GoVel);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(drive_ReadStatusword_obj, ReadStatusword);
STATIC MP_DEFINE_CONST_FUN_OBJ_1(drive_SetTargetPos_obj, SetTargetPos);
STATIC MP_DEFINE_CONST_FUN_OBJ_1(drive_SetPosVel_obj, SetPosVel);
STATIC MP_DEFINE_CONST_FUN_OBJ_1(drive_SetAcc_obj, SetAcc);
STATIC MP_DEFINE_CONST_FUN_OBJ_1(drive_SetDec_obj, SetDec);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(drive_GetActualPos_obj, GetActualPos);
STATIC MP_DEFINE_CONST_FUN_OBJ_1(drive_SetOpMode_obj, SetOpMode);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(drive_GetOpMode_obj, GetOpMode);
STATIC MP_DEFINE_CONST_FUN_OBJ_1(drive_SetTorque_obj, SetTorque);
STATIC MP_DEFINE_CONST_FUN_OBJ_1(drive_ChkIn_obj, ChkIn);
STATIC MP_DEFINE_CONST_FUN_OBJ_1(drive_SetOut_obj, SetOut);
STATIC MP_DEFINE_CONST_FUN_OBJ_1(drive_ClearOut_obj, ClearOut);
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(drive_GoHome_obj, 4, 4, GoHome);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(drive_ChkEnabled_obj, ChkEnabled);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(drive_ChkReady_obj, ChkReady);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(drive_ChkMoving_obj, ChkMoving);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(drive_ChkError_obj, ChkError);
STATIC MP_DEFINE_CONST_FUN_OBJ_1(drive_ChkMfrStatus_obj, ChkMfrStatus);

STATIC const mp_map_elem_t mcdrive_globals_table[] = {
	{ MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_OBJ_NEW_QSTR(MP_QSTR_drive) },
	{ MP_OBJ_NEW_QSTR(MP_QSTR_SendEmcyMsg), (mp_obj_t)&drive_SendEmcyMsg_obj },	
	{ MP_OBJ_NEW_QSTR(MP_QSTR_WriteObject), (mp_obj_t)&drive_WriteObject_obj },		
	{ MP_OBJ_NEW_QSTR(MP_QSTR_ReadObject), (mp_obj_t)&drive_ReadObject_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_WriteControl), (mp_obj_t)&drive_WriteControl_obj },	
	{ MP_OBJ_NEW_QSTR(MP_QSTR_EnableDrive), (mp_obj_t)&drive_EnableDrive_obj },	
	{ MP_OBJ_NEW_QSTR(MP_QSTR_StopMotion), (mp_obj_t)&drive_StopMotion_obj },
	{ MP_OBJ_NEW_QSTR(MP_QSTR_ContinueMotion), (mp_obj_t)&drive_StopMotion_obj },	
	{ MP_OBJ_NEW_QSTR(MP_QSTR_PowerQuit), (mp_obj_t)&drive_PowerQuit_obj },	
	{ MP_OBJ_NEW_QSTR(MP_QSTR_StorePermanent), (mp_obj_t)&drive_StorePermanent_obj },	
	{ MP_OBJ_NEW_QSTR(MP_QSTR_ResetToFactory), (mp_obj_t)&drive_ResetToFactory_obj },	
	{ MP_OBJ_NEW_QSTR(MP_QSTR_GoPosAbs), (mp_obj_t)&drive_GoPosAbs_obj },
	{ MP_OBJ_NEW_QSTR(MP_QSTR_GoPosRel), (mp_obj_t)&drive_GoPosRel_obj },
	{ MP_OBJ_NEW_QSTR(MP_QSTR_GoVel), (mp_obj_t)&drive_GoVel_obj },  
    { MP_OBJ_NEW_QSTR(MP_QSTR_ReadStatusword), (mp_obj_t)&drive_ReadStatusword_obj }, 
	{ MP_OBJ_NEW_QSTR(MP_QSTR_SetTargetPos), (mp_obj_t)&drive_SetTargetPos_obj },	  	
	{ MP_OBJ_NEW_QSTR(MP_QSTR_SetPosVel), (mp_obj_t)&drive_SetPosVel_obj },	
	{ MP_OBJ_NEW_QSTR(MP_QSTR_SetAcc), (mp_obj_t)&drive_SetAcc_obj },	
	{ MP_OBJ_NEW_QSTR(MP_QSTR_SetDec), (mp_obj_t)&drive_SetDec_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_GetActualPos), (mp_obj_t)&drive_GetActualPos_obj }, 
    { MP_OBJ_NEW_QSTR(MP_QSTR_SetOpMode), (mp_obj_t)&drive_SetOpMode_obj },	
    { MP_OBJ_NEW_QSTR(MP_QSTR_GetOpMode), (mp_obj_t)&drive_GetOpMode_obj },	
    { MP_OBJ_NEW_QSTR(MP_QSTR_SetTorque), (mp_obj_t)&drive_SetTorque_obj },
	{ MP_OBJ_NEW_QSTR(MP_QSTR_ChkIn), (mp_obj_t)&drive_ChkIn_obj },	
    { MP_OBJ_NEW_QSTR(MP_QSTR_SetOut), (mp_obj_t)&drive_SetOut_obj },	
    { MP_OBJ_NEW_QSTR(MP_QSTR_ClearOut), (mp_obj_t)&drive_ClearOut_obj },	
    { MP_OBJ_NEW_QSTR(MP_QSTR_GoHome), (mp_obj_t)&drive_GoHome_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_ChkEnabled), (mp_obj_t)&drive_ChkEnabled_obj },	
    { MP_OBJ_NEW_QSTR(MP_QSTR_ChkReady), (mp_obj_t)&drive_ChkReady_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_ChkMoving), (mp_obj_t)&drive_ChkMoving_obj },    	
    { MP_OBJ_NEW_QSTR(MP_QSTR_ChkError), (mp_obj_t)&drive_ChkError_obj },	
    { MP_OBJ_NEW_QSTR(MP_QSTR_ChkMfrStatus), (mp_obj_t)&drive_ChkMfrStatus_obj }
};


STATIC MP_DEFINE_CONST_DICT (
	mp_module_mcdrive_globals,
	mcdrive_globals_table
);

const mp_obj_module_t mp_module_mcdrive = {
	.base = { &mp_type_module },
	.globals = (mp_obj_dict_t*)&mp_module_mcdrive_globals,
};






