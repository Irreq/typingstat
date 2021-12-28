#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# File name: typingstat/demos/viewer.py
# Description: View statistics about your typing in the terminal
# Author: irreq (irreq@protonmail.com)
# Date: 28/12/2021

# Import the module
from typingstat import Typingstat, __version__

# Initiate the class
ts = Typingstat()

def format_output(result):
    """Format output to preserve consistence in output"""

    formatted = "WPM: %-3s " % result["wpm"]
    formatted += "KPS: %-3s " % result["kps"]
    formatted += "Error: %%-3s " % result["error"]
    formatted += "Strokes: %d " % result["strokes"]

    return formatted

print("Below are your typingstat estimates:")
print("Start typing!", end="\r")

# To gracefully exit if you press Ctrl+C
while not ts.kill_now:
    result = ts.poll()
    # result = {
    # "kps": int(),
    # "wpm": int(),
    # "error": int(),
    # "strokes": int()
    # } or None

    # No need to output if poll returned 'None', which could
    # be a result of no key has been pressed
    if result is not None:
        # No need to output if the poll retrieved same result as last
        if result != ts.previous_poll:
            formatted = format_output(result)
            print(formatted, end="\r")

print("\n\nTypingstat v%s - https://www.github.com/Irreq/typingstat\n\nBye!" % (__version__))
