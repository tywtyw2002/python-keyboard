import struct


def find_device(devices, usage_page, usage):
    for device in devices:
        if (
            device.usage_page == usage_page
            and device.usage == usage
            and hasattr(device, "send_report")
        ):
            return device
    raise ValueError("Not found")


class HID:
    def __init__(self, devices):
        self.keyboard = find_device(devices, usage_page=0x1, usage=0x06)
        self.consumer_control = find_device(devices, usage_page=0x0C, usage=0x01)
        # self.mouse = find_device(devices, usage_page=0x1, usage=0x02)

        self.consumer_report = bytearray(2)

        # report[0] modifiers
        # report[1] unused
        # report[2:] regular keys
        self.report = bytearray(8)
        self.report_keys = memoryview(self.report)[2:]

        for device in devices:
            if (
                device.usage_page == 0x1
                and device.usage == 0x6
                and hasattr(device, "report")
            ):
                self._leds = device
                break
        else:
            self._leds = None

    def press(self, *keycodes):
        for keycode in keycodes:
            if 0xE0 <= keycode and keycode < 0xE8:
                self.report[0] |= 1 << (keycode & 0x7)
                continue

            for c in self.report_keys:
                if c == keycode:
                    break
            else:
                for i in range(6):
                    if self.report_keys[i] == 0:
                        self.report_keys[i] = keycode
                        break
        self.keyboard.send_report(self.report)

    def release(self, *keycodes):
        for keycode in keycodes:
            if 0xE0 <= keycode and keycode < 0xE8:
                self.report[0] &= ~(1 << (keycode & 0x7))
                continue

            for i in range(6):
                if self.report_keys[i] == keycode:
                    self.report_keys[i] = 0

        self.keyboard.send_report(self.report)

    def send(self, *keycodes):
        self.press(*keycodes)
        for i in range(8):
            self.report[i] = 0
        self.keyboard.send_report(self.report)

    def send_consumer(self, keycode):
        struct.pack_into("<H", self.consumer_report, 0, keycode)
        self.consumer_control.send_report(self.consumer_report)

    def release_all(self):
        self.send_consumer(0)
        for i in range(8):
            self.report[i] = 0
        self.keyboard.send_report(self.report)

    @property
    def leds(self):
        if self._leds:
            return self._leds.report[0]
        return None