/*********************************************************************
* @file  mcnet.h
* @brief MC ETH communication/networking API for use within Python. 
        Defines Python global objects "mcnet"
* @author fullmo GmbH
* Copyright fullmo GmbH, all rights reserved
*************************************************************************/

#include "py/nlr.h"
#include "py/obj.h"
#include "py/runtime.h"
#include "py/binary.h"

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "pic32bit_mphal.h"


char refGoAnswerBuffer[REFGO_MAX_LINE_LEN + 2];

STATIC mp_obj_t open(mp_obj_t channelSetting, mp_obj_t index) {
    __attribute__((unused)) const char *channelSet = mp_obj_str_get_str(channelSetting);
    __attribute__((unused)) int chnlIndex = mp_obj_get_int(index);
    int ret = RefGoRedirect_Open();
    return MP_OBJ_NEW_SMALL_INT(ret);
}

STATIC mp_obj_t read(mp_obj_t index, mp_obj_t readType) {
    __attribute__((unused)) int chnlIndex = mp_obj_get_int(index);
    __attribute__((unused)) int reTypeInt = mp_obj_get_int(readType);
    const char *readNextCommand = RefGoRedirect_Read();
    size_t readLen = strlen(readNextCommand);
    if (readLen) {
        return mp_obj_new_str(readNextCommand, readLen);
    }
    else {
        return mp_const_none;
    }
}

STATIC mp_obj_t write(mp_obj_t index, mp_obj_t writeType, mp_obj_t msg) {
    __attribute__((unused)) int chnlIndex = mp_obj_get_int(index);
    __attribute__((unused)) int wrTypeInt = mp_obj_get_int(writeType);
    const char *msgData = mp_obj_str_get_str(msg);
    int ret = RefGoRedirect_Write(msgData);
    return MP_OBJ_NEW_SMALL_INT(ret);    
}

STATIC mp_obj_t close(mp_obj_t index) {
    __attribute__((unused)) int chnlIndex = mp_obj_get_int(index);
    RefGoRedirect_Close();
    return mp_const_none;
}

// RefGo cmd object: Process RefGo commands from Python 
STATIC mp_obj_t refgo_cmd(mp_obj_t cmd) {
    const char *cmdStr = mp_obj_str_get_str(cmd);
    ParseRefGoCommand(cmdStr, refGoAnswerBuffer);
    size_t answerLen = strlen(refGoAnswerBuffer);
    if (answerLen > 0) {
        // performance boost:
        // "TS" and "TP" results are returned as integer -> no garbage / gc
        if ((toupper(cmdStr[0]) == 'T') && ((toupper(cmdStr[1]) == 'P') || (toupper(cmdStr[1]) == 'S'))) {
                return mp_obj_new_int(atol(refGoAnswerBuffer));
        } 
        else {
            return mp_obj_new_str(refGoAnswerBuffer, answerLen);
        }
    }
    else {
        return mp_const_none;    
    }
}


STATIC MP_DEFINE_CONST_FUN_OBJ_2(refgo_open_obj, open);
STATIC MP_DEFINE_CONST_FUN_OBJ_2(refgo_read_obj, read);
STATIC MP_DEFINE_CONST_FUN_OBJ_3(refgo_write_obj, write);
STATIC MP_DEFINE_CONST_FUN_OBJ_1(refgo_close_obj, close);
STATIC MP_DEFINE_CONST_FUN_OBJ_1(refgo_cmd_obj, refgo_cmd);

STATIC const mp_map_elem_t refgo_globals_table[] = {
	{ MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_OBJ_NEW_QSTR(MP_QSTR_refgo) },
    { MP_OBJ_NEW_QSTR(MP_QSTR_cmd), (mp_obj_t)&refgo_cmd_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_open), (mp_obj_t)&refgo_open_obj },	
    { MP_OBJ_NEW_QSTR(MP_QSTR_read), (mp_obj_t)&refgo_read_obj },	
    { MP_OBJ_NEW_QSTR(MP_QSTR_write), (mp_obj_t)&refgo_write_obj },	
    { MP_OBJ_NEW_QSTR(MP_QSTR_close), (mp_obj_t)&refgo_close_obj }
};

STATIC MP_DEFINE_CONST_DICT (
	mp_module_refgo_globals,
	refgo_globals_table
);

const mp_obj_module_t mp_module_refgo = {
	.base = { &mp_type_module },
	.globals = (mp_obj_dict_t*)&mp_module_refgo_globals,
};






