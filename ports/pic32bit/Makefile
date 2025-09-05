include ../../py/mkenv.mk

# qstr definitions (must come before including py.mk)
QSTR_DEFS = qstrdefsport.h

# include py core make definitions
include $(TOP)/py/py.mk

XC32 = /opt/microchip/xc32/v4.00
CROSS_COMPILE = $(XC32)/bin/xc32-

PARTFAMILY = PIC32MZ
PART = 32MZ2048EFM144

INC += -I.
INC += -I$(TOP)
INC += -I$(BUILD)
INC += -I$(XC32)/pic32mx/include
INC += -I$(XC32)/pic32mx/include/proc
INC += -I$(XC32)/pic32mx/lib/proc/32MZ2048EFM144
# INC += -I$(XC32)/support/$(PARTFAMILY)/h

CFLAGS_PIC32BIT = -mprocessor=32MZ2048EFM144 ####-mcpu=$(PART) ###-mlarge-code
CFLAGS = $(INC) -Wall -std=gnu99 -nostdlib $(CFLAGS_PIC32BIT) $(COPT)

#Debugging/Optimization
ifeq ($(DEBUG), 1)
CFLAGS += -O0 -ggdb
else
CFLAGS += -O1 -DNDEBUG
endif

###LDFLAGS = --heap=0 -nostdlib -T $(XC32)/pic32mx/lib/proc/32MZ2048EFM144/p32MZ2048EFM144.ld -Map=$@.map --cref -p$(PART)
LDFLAGS = --defsym=_min_heap_size=0 -nostdlib -T $(XC32)/pic32mx/lib/proc/32MZ2048EFM144/p32MZ2048EFM144.ld -Map=$@.map --cref -p$(PART) 
######LIBS = -L$(XC32)/lib -L$(XC16)/lib/$(PARTFAMILY) -lc -lm -lpic30 -lp$(PART)

SRC_C = \
	main.c \
	board.c \
	pic32bit_mphal.c \
	modpyb.c \
	modpybled.c \
	modpybswitch.c \
	lib/utils/pyexec.c \
	lib/utils/sys_stdio_mphal.c \
	lib/mp-readline/readline.c \
	sys.c \
	mcdrive.c \
	mccom.c \

SRC_S = \
#	gchelper.s \

OBJ = $(PY_O) $(addprefix $(BUILD)/, $(SRC_C:.c=.o) $(SRC_S:.s=.o))

# List of sources for qstr extraction
SRC_QSTR += $(SRC_C)
# Append any auto-generated sources that are needed by sources listed in
# SRC_QSTR
SRC_QSTR_AUTO_DEPS +=

all: $(BUILD)/firmware.hex

$(BUILD)/firmware.hex: $(BUILD)/firmware.elf
	$(ECHO) "Create $@"
	$(Q)$(CROSS_COMPILE)bin2hex $<

$(BUILD)/firmware.elf: $(OBJ)	
	$(ECHO) "LINK $@"
	$(Q)$(LD) $(LDFLAGS) -o $@ $^ $(LIBS)
	$(Q)size $@

$(PY_BUILD)/gc.o: CFLAGS += -O1
$(PY_BUILD)/vm.o: CFLAGS += -O1

include $(TOP)/py/mkrules.mk
