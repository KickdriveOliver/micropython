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



//include harmony stuff
#ifdef HARMONY_COMPILE  //defined as project preprocessing macro to be visible projectwide
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdlib.h>
#include "system_config.h"
#include "system_definitions.h"
#include "vscan.h"
#endif


#include "board.h"

/********************************************************************/
// CPU

void cpu_init(void) {

    //this is performed by Harmony initialization in MPLABX

}

/********************************************************************/
// LEDs



#define LED_ON (1)
#define LED_OFF (0)

void led_init(void) {
    //this is performed by Harmony initialization in MPLABX
}

void led_state(int led, int state) {
#ifdef HARMONY_COMPILE  //defined as project preprocessing macro to be visible projectwide
    /* ### OH 2020-02-11 temp disabled
    int val = state ? LED_ON : LED_OFF;
    switch (led) {
        case 1: BSP_LEDStateSet(BSP_LED_1, val);
            break;
        case 2: BSP_LEDStateSet(BSP_LED_2, val);
            break;
        case 3: BSP_LEDStateSet(BSP_LED_3, val);
            break;
    }
     */ 
#endif
}

void led_toggle(int led) {
#ifdef HARMONY_COMPILE  //defined as project preprocessing macro to be visible projectwide
    /* ### OH 2020-02-11 temp disabled
    switch (led) {
        case 1: BSP_LEDToggle(BSP_LED_1);
            break;
        case 2: BSP_LEDToggle(BSP_LED_2);
            break;
        case 3: BSP_LEDToggle(BSP_LED_3);
            break;
    } */
#endif
}

/********************************************************************/
// switches

void switch_init(void) {
    // set switch GPIO as inputs
    //this is performed by Harmony initialization in MPLABX
}

int switch_get(int sw) {
    int val = 1;
#ifdef HARMONY_COMPILE  //defined as project preprocessing macro to be visible projectwide
    /* ### OH 2020-02-11 temp disabled
    switch (sw) {
        case 1: val = (BSP_SWITCH_STATE_PRESSED == BSP_SwitchStateGet(BSP_SWITCH_1));
            break;
        case 2: val = (BSP_SWITCH_STATE_PRESSED == BSP_SwitchStateGet(BSP_SWITCH_2));
            break;
        case 3: val = (BSP_SWITCH_STATE_PRESSED == BSP_SwitchStateGet(BSP_SWITCH_3));
            break;
    }*/ 
    val = 0;
#endif
    return val;
}

/********************************************************************/
// UART

void uart_init(void) {

    //performed as par of the Harmony initialization
}

char rxChar;
#define RXBUFSIZE 64
unsigned char rxBuf[RXBUFSIZE];
unsigned int rxBufPos = 0;

int uart_rx_any(void) {
    char input[10];
    input[0] = 0;
    int returned = 0;
/* ### OH 2020-10-20 don't use UART. Redirect to TCP/IP later
#ifdef HARMONY_COMPILE  //defined as project preprocessing macro to be visible projectwide
    //returned = DRV_USART0_Read(input, 1);
    if (DRV_USART1_ReceiverBufferIsEmpty()) {

    } else {
        returned = DRV_USART1_ReadByte();
    }
#endif
 */
    rxChar = input[0];
    return (returned);
}

void uart_tx_char(int chr) {
    // TX output to UDP debug 
    rxBuf[rxBufPos++] = (unsigned char)chr;
    if (rxBufPos == RXBUFSIZE || chr == '\n') {
        udpDebugConsoleAppIoWrite(rxBuf, rxBufPos);
        rxBufPos = 0;
    }
}
