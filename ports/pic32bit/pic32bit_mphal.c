/*
 * This file is part of the MicroPython project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2015 Damien P. George
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include <string.h>
#include "py/mphal.h"
#include "board.h"
#include "pic32bit_mphal.h"

#ifdef HARMONY_COMPILE  //defined as project preprocessing macro to be visible projectwide

#endif

static int interrupt_char;

typedef uint32_t MCKERNEL_TIMER_TYPE;
extern volatile MCKERNEL_TIMER_TYPE MCKERNEL_Timer1ms;
extern volatile uint8_t mcPythonUserAbort;

void mp_hal_init(void) {
    MP_STATE_PORT(keyboard_interrupt_obj) = mp_obj_new_exception(&mp_type_KeyboardInterrupt);
}

mp_uint_t mp_hal_ticks_ms(void) {
    return (mp_uint_t)MCKERNEL_Timer1ms;
}

void mp_hal_delay_ms(mp_uint_t ms) {
    if (ms == 0) return;
    MCKERNEL_TIMER_TYPE start_time = MCKERNEL_Timer1ms;
    while ((!mcPythonUserAbort) && MCKERNEL_NOT_TIMEOUT(start_time, ms)) {
        vTaskDelay(1);
    }
}

void mp_hal_set_interrupt_char(int c) {
    interrupt_char = c;
}

// ### OH 2021-05-03: RX/TX currently not supported
// TODO: check if MICROPY_KBD_EXCEPTION can be used and rx / tx redirected to system console / UDP channel 
volatile unsigned char pythonUARTrx;

// http://docs.micropython.org/en/latest/develop/porting.html?highlight=mp_hal_stdin_rx_chr           
// Receive single character, blocking until one is available.
int mp_hal_stdin_rx_chr(void) {
    while (pythonUARTrx == 0) {
        vTaskDelay(1);//release processing time for other tasks
    }
    unsigned char c = pythonUARTrx;
    pythonUARTrx = 0;
    // (add a proper input/output for REPL later)
    return c;
}

void mp_hal_stdout_tx_str(const char *str) {
    mp_hal_stdout_tx_strn(str, strlen(str));
}

// Send the string of given length
void mp_hal_stdout_tx_strn(const char *str, size_t len) {
    for (; len > 0; --len) {
        uart_tx_char(*str++);
    }
}

void mp_hal_stdout_tx_strn_cooked(const char *str, size_t len) {
    for (; len > 0; --len) {
        if (*str == '\n') {
            uart_tx_char('\r');
        }
        uart_tx_char(*str++);
    }
}
