#include <stdint.h>
#include <alloca.h>

// options to control how MicroPython is built
#define MICROPY_OBJ_REPR            (MICROPY_OBJ_REPR_B)
#define MICROPY_ALLOC_PATH_MAX      (64)
#define MICROPY_EMIT_X64            (0)
#define MICROPY_EMIT_THUMB          (0)
#define MICROPY_EMIT_INLINE_THUMB   (0)
#define MICROPY_COMP_MODULE_CONST   (0)
#define MICROPY_COMP_CONST          (0)
#define MICROPY_MEM_STATS           (0)
#define MICROPY_DEBUG_PRINTERS      (1)
#define MICROPY_DEBUG_VERBOSE       (0)
#define MICROPY_ENABLE_GC           (1)
#define MICROPY_REPL_EVENT_DRIVEN   (0)
#define MICROPY_HELPER_REPL         (1)
#define MICROPY_HELPER_LEXER_UNIX   (0)
#define MICROPY_ENABLE_SOURCE_LINE  (1)
#define MICROPY_ENABLE_DOC_STRING   (0)
#define MICROPY_ERROR_REPORTING     (MICROPY_ERROR_REPORTING_DETAILED)
#define MICROPY_PY_ASYNC_AWAIT      (0)
#define MICROPY_PY_BUILTINS_BYTEARRAY (0)
#define MICROPY_PY_BUILTINS_MEMORYVIEW (0)
#define MICROPY_PY_BUILTINS_FROZENSET (0)
#define MICROPY_PY_BUILTINS_SET     (0)
#define MICROPY_PY_BUILTINS_SLICE   (0)
#define MICROPY_PY_BUILTINS_PROPERTY (0)
#define MICROPY_PY_MICROPYTHON_MEM_INFO (1)
#define MICROPY_PY___FILE__         (0)
#define MICROPY_PY_GC               (1)
#define MICROPY_PY_ARRAY            (0)
#define MICROPY_PY_COLLECTIONS      (0)
#define MICROPY_PY_MATH             (0)
#define MICROPY_PY_CMATH            (0)
#define MICROPY_PY_IO               (0)
#define MICROPY_PY_STRUCT           (0)
#define MICROPY_PY_SYS              (0)
#define MICROPY_CPYTHON_COMPAT      (0)
#define MICROPY_LONGINT_IMPL        (MICROPY_LONGINT_IMPL_MPZ)
#define MICROPY_FLOAT_IMPL          (MICROPY_FLOAT_IMPL_NONE)

// USE PIC32 / XC32's own <alloca.h>
#define MICROPY_NO_ALLOCA           (0)

// type definitions for the specific machine
#define MP_ENDIANNESS_LITTLE        (1)
#define MPZ_DIG_SIZE                (16)

#define MICROPY_MAKE_POINTER_CALLABLE(p) ((void*)((mp_uint_t)(p)))

#define UINT_FMT "%u"
#define INT_FMT "%d"
typedef int mp_int_t; // must be pointer size
typedef unsigned int mp_uint_t; // must be pointer size

typedef int mp_off_t;

#define MP_PLAT_PRINT_STRN(str, len) mp_hal_stdout_tx_strn_cooked(str, len)

// extra built in names to add to the global namespace
#define MICROPY_PORT_BUILTINS \
    { MP_ROM_QSTR(MP_QSTR_open), MP_ROM_PTR(&mp_builtin_open_obj) },

// extra builtin modules to add to the list of known ones
extern const struct _mp_obj_module_t pyb_module;
extern const struct _mp_obj_module_t mp_module_mcdrive;
extern const struct _mp_obj_module_t mp_module_refgo;
extern const struct _mp_obj_module_t mp_module_sys;

// (the "drive" import module instead of "mcdrive" is kept for compatiblity reasons. 
// new scripts should use "import mcdrive")
#define MICROPY_PORT_BUILTIN_MODULES \
    { MP_ROM_QSTR(MP_QSTR_pyb), MP_ROM_PTR(&pyb_module) }, \
    { MP_OBJ_NEW_QSTR(MP_QSTR_mcdrive), (mp_obj_t)&mp_module_mcdrive }, \
    { MP_OBJ_NEW_QSTR(MP_QSTR_drive), (mp_obj_t)&mp_module_mcdrive }, \
    { MP_OBJ_NEW_QSTR(MP_QSTR_refgo), (mp_obj_t)&mp_module_refgo }, \
    { MP_OBJ_NEW_QSTR(MP_QSTR_sys), (mp_obj_t)&mp_module_sys }, \

#define MP_STATE_PORT MP_STATE_VM

#define MICROPY_PORT_ROOT_POINTERS \
    char *readline_hist[8]; \
    mp_obj_t keyboard_interrupt_obj; \

#define MICROPY_MPHALPORT_H "pic32bit_mphal.h"
#define MICROPY_HW_BOARD_NAME "PIC32SK"
#define MICROPY_HW_MCU_NAME "PIC32MZ"



