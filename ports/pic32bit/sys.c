#include "py/nlr.h"
#include "py/obj.h"
#include "py/runtime.h"
#include "py/binary.h"
//#include "portmodules.h"





#include <stdio.h>
#include <stdlib.h>

#include "pic32bit_mphal.h"





STATIC mp_obj_t time(void) {
    return MP_OBJ_NEW_SMALL_INT(mp_hal_ticks_ms());
}

STATIC mp_obj_t wait(mp_obj_t period) {

    mp_hal_delay_ms(MP_OBJ_SMALL_INT_VALUE(period));
//    //printf functions seems to be interrupt blocking and prolong timing if printed during pause..
    return mp_const_none;
}



STATIC MP_DEFINE_CONST_FUN_OBJ_0(sys_time_obj, time);
STATIC MP_DEFINE_CONST_FUN_OBJ_1(sys_wait_obj, wait);


STATIC const mp_map_elem_t sys_globals_table[] = {
	{ MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_OBJ_NEW_QSTR(MP_QSTR_sys) },
	{ MP_OBJ_NEW_QSTR(MP_QSTR_time), (mp_obj_t)&sys_time_obj },
	{ MP_OBJ_NEW_QSTR(MP_QSTR_wait), (mp_obj_t)&sys_wait_obj },
};

STATIC MP_DEFINE_CONST_DICT (
	mp_module_sys_globals,
	sys_globals_table
);

const mp_obj_module_t mp_module_sys = {
	.base = { &mp_type_module },
	.globals = (mp_obj_dict_t*)&mp_module_sys_globals,
};






