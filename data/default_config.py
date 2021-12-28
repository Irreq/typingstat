#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# File name: typingstat/data/config.py
# Description: Default configuration file for typingstat and typingstad daemon
# Author: irreq (irreq@protonmail.com)
# Date: 28/12/2021

# TODO:
# (keyboard) Fix dynamic layout mapping
# (keyboard) Fix dynamic language+alphabet selector
#
# Usage: (needs root access for keyboard)
#
# chmod +x typingstatd
# nohup /path/to/typingstatd &
#
# You can find the process and its process Id with this command:
#
# ps ax | grep typingstatd
#
# If you want to stop the execution, you can kill it with the kill command:
#
# kill PID


# #### USER MODIFY THIS ####

# I used this reference to map my keyboard:
# http://www.penticoff.com/nb/kbds/ibm104kb.htm
#
# It shows the keys and their corresponding values as integers with
# equal sign, but I converted it to a Swedish QWERTY-keyboard. Therefore,
# your keyboard might not work out of the box.
#
# Change the values below to fit your keyboard.

keyboard_layout = {
 1: "Esc",
 2: "1",
 3: "2",
 4: "3",
 5: "4",
 6: "5",
 7: "6",
 8: "7",
 9: "8",
10: "9",
11: "0",
12: "+",
13: "´",
14: "BkSpc",
15: "Tab",
16: "Q",
17: "W",
18: "E",
19: "R",
20: "T",
21: "Y",
22: "U",
23: "I",
24: "O",
25: "P",
26: "Å",
27: "¨",
28: "Enter",
29: "Left Ctrl",
30: "A",
31: "S",
32: "D",
33: "F",
34: "G",
35: "H",
36: "J",
37: "K",
38: "L",
39: "Ö",
40: "Ä",
41: "`",
42: "Left Shift",
43: "''",
44: "Z",
45: "X",
46: "C",
47: "V",
48: "B",
49: "N",
50: "M",
51: ",",
52: ".",
53: "-",
54: "Right Shift",
55: "Pad *",
56: "Left Alt",
57: "Space",
58: "Caps",
59: "F1",
60: "F2",
61: "F3",
62: "F4",
63: "F5",
64: "F6",
65: "F7",
66: "F8",
67: "F9",
68: "F10",
69: "NumLock",
70: "ScrollLock",
71: "Pad 7",
72: "Pad 8",
73: "Pad 9",
74: "Pad Minus",
75: "Pad 4",
76: "Pad 5",
77: "Pad 6",
78: "Pad Plus",
79: "Pad 1",
80: "Pad 2",
81: "Pad 3",
82: "Pad 0/Ins",
83: "Pad ./Del",
# 84: "PrtScr/SysRq",
85: "",
86: "<",
87: "F11",
88: "F12",
89: "",
# 90: "Pause/Break",
# 91: "Insert",
# 92: "Home",
# 93: "PgUp",
94: "Gray /",
# 95: "Delete",
96: "Pad Enter",
97: "Right Ctrl",
98: "Pad /",
99: "PrtScr/SysRq",
100: "Right Alt",
# 101: "Left Arrow",
102: "Home",
103: "Up Arrow",
104: "PgUp",
105: "Left Arrow",
106: "Right Arrow",
107: "End",
108: "Down Arrow",
109: "PgDn",
110: "Insert",
111: "Delete",

119: "Pause/Break",

125: "Left Super",
126: "Right Super",
127: "Menu",}

# The event for the keylogger to use. To list available events, type:
# 'ls /dev/input/by-id' and choose your keyboard.
# Eg, event = "/dev/input/by-id/usb-Dell_Dell_USB_Keyboard-event-kbd"
# The program will if event is 'None' try to find a keyboard on its own. It
# might be a problem if multiple keybaords are presents as there is no logic
# behind which keyboard will be chosen.
# event = None
# event = "/dev/input/by-id/usb-Dell_Dell_USB_Keyboard-event-kbd"
event = "/dev/input/by-id/usb-CHICONY_Compaq_USB_Keyboard-event-kbd"
language = "sv"

# Keys when tapped will count as 'typing a word' for WPM estimation. Change this
# to what you prefer. I left out numbers as I do not count them as words, and I
# added the nordic characters: Å, Ä and Ö as I use them frequently in words.
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
# If you wan't to log your typing, change 'log' to a valid path.
# Eg, "~/.cache/typing.log"
log = False
# Change the default key to decrease the risk of data being gathered by the wrong
# person.
key = "sdf87s8df"

# If you wanna see messages from typingstat
debug = False

# #### ADVANCED OPTIONS ####
# Do not modify these unless you know what you are doing.
pidfile = "/tmp/typingstatd.pid"
udp_ip = "localhost"
udp_port = 12345
