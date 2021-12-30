
from PYKB import *


class CKeyboard(Keyboard):
    def change_bt(self, n):
        changed = False
        if self.usb_status == 3:
            self.usb_status = 1
            changed = True
        if n != self.ble_id:
            changed = True
            self.set_bt_id(n)
            self.ble.name = "CosHiM KB-%02d" % n
            self.advertisement.complete_name = self.ble.name
            self.start_advertising()
        elif not self.ble.connected and not self.ble._adapter.advertising:
            self.start_advertising()

        if changed:
            self.on_device_changed("BT{}".format(n))


keyboard = CKeyboard()

___ = TRANSPARENT
BOOT = BOOTLOADER
L1 = LAYER_TAP(1)
L2 = LAYER_TAP(2)

FN2 =LAYER_TAP_TOGGLE(1)
FN3 =LAYER_TAP_TOGGLE(3)

# LSFT4 = LAYER_MODS(4, MODS(LSHIFT))
# RSFT4 = LAYER_MODS(4, MODS(RSHIFT))

# Semicolon & Ctrl
# SCC = MODS_TAP(MODS(RCTRL), ';')

CALC = APPLAUNCH_CALCULATOR

VOLU = 0x80  # Keyboard Volume Up
VOLD = 0x81  # Keyboard Volume Down

keyboard.keymap = (
    # layer 0
    (
        ESC,   1,   2,   3,   4,   5,   6,   7,   8,   9,   0, '-', '=', BACKSPACE,
        TAB,   Q,   W,   E,   R,   T,   Y,   U,   I,   O,   P, '[', ']', '|',
        LCTRL,  A,   S, D,   F,   G,   H,   J,   K,   L, ';', '"',    ENTER,
        LSHIFT, Z,   X,   C,   V,  B,   N,   M, ',', '.', '/',         RSHIFT,
        LCTRL, LALT, LGUI,          SPACE,            RGUI,  L1, L2, GRAVE
    ),

    # layer 1
    (
        GRAVE,  F1,  F2,  F3,  F4,  F5,  F6,  F7,  F8,  F9, F10, F11, F12, DEL,
        ___, ___,  UP, ___, ___, ___, CALC, ___, INSERT, ___,PRTSCN,SCROLLLOCK,PAUSE,___,
        ___,LEFT,DOWN,RIGHT,___, ___, ___, ___, ___, ___, HOME, PGUP ,      ___,
        ___, ___, MENU, ___, ___, ___, VOLD,VOLU, MUTE, END, PGDN,       ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),

    # layer 2
    (
        NO , NO , NO , NO , NO , NO , NO , NO , NO , NO , NO , NO , NO , NO ,
        NO , NO , NO , NO , NO , NO , NO , NO , NO , NO , NO , NO , NO , NO ,
        NO , NO , NO , NO , NO , NO , NO , NO , NO , NO , NO , NO ,      NO ,
        NO , NO , NO , NO , NO , FN3, NO , NO , NO , NO , NO ,           NO ,
        NO , NO , NO ,                    FN2,               NO , NO , NO ,  NO 
    ),

    # layer 3
    (
        BT_TOGGLE,BT1,BT2, BT3,BT4,BT5,BT6,BT7, BT8, BT9, BT0, NO , NO , NO ,
        NO , NO , NO , NO , NO , NO ,NO ,USB_TOGGLE,NO ,NO ,SHUTDOWN ,NO ,NO , NO ,
        NO , NO , SUSPEND, NO , NO , NO , NO , NO , NO , NO , NO , NO ,      NO ,
        NO , NO , NO , NO , NO , MACRO(10) , NO , NO , NO , NO , NO ,           NO ,
        NO , NO , NO ,                FN3 ,               NO , NO , NO ,  NO 
    ),
)


def macro_handler(dev, n, is_down):
    if is_down:
        dev.send_text('You pressed macro #{}\n'.format(n))
    else:
        if n == 10:
            dev.send_text('Battary Lvl: {}%'.format(battery_level()))
        else:
            dev.send_text('You released macro #{}\n'.format(n))

def pairs_handler(dev, n):
    dev.send_text('You just triggered pair keys #{}\n'.format(n))


keyboard.macro_handler = macro_handler
keyboard.pairs_handler = pairs_handler

# Pairs: J & K, U & I
keyboard.pairs = [{35, 36}, {20, 19}]

keyboard.verbose = True

# hot fix ble name
bt_idx = int(keyboard.ble.name.replace("PYKB ",""))
keyboard.ble.name = "CosHiM KB-%02d" % bt_idx
keyboard.advertisement.complete_name = keyboard.ble.name


keyboard.run()