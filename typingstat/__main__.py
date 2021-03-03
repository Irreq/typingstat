#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
A tool for displaying typing statistics

[WARNING]

This is a keylogger, and it can display
everything typed on the keaboard, including passwords.
If you do not wan't to see typed words,
you start the program without any log flags.
"""

import curses
import argparse
import configparser
import random
import time
from math import floor
from fractions import Fraction

import config
from layout import keyboard_layout
from keylogger import Keylogger


__version__ = "0.2"


def refresh():
    """initiate all variables"""
    config.typing = {
        'error_count': 0,  # Number of times you've pressed 'Delete' or 'BkSpc'
        'error_percentage': 0,
        'error_ratio': "",

        'word_count': 1,
        'word_buffer': "",  # Keys will be added to build a word
        'word_time': [],  # When the words were typed
        'word_mean_length': 0,
        'word_longest': [],  # Only if you log your typed words
        'word_per_minute': 0,

        'key_strokes': 0,
        'key_abc_count': 0,  # Number of alphabetical keys pressed
        'key_query': [time.time()],
        'key_query_total': [50],  # What would be used to get mean wpm
        'key_per_second': 0,
        # Contains the keys from you keyboard
        'key_common_keys': {i: 0 for i in keyboard_layout.keys()},
        'key_common': [],  # Only if you log typed keys
        'key_current_key': "",
        'key_current_code': 0,
        'key_current_seconds': 0,
        'key_previous': "",
        'key_spaces_count': 1,
    }

def set_args():
    """get arguments"""
    config_parser = configparser.ConfigParser()
    config_parser.read('setup.ini')
    parser = argparse.ArgumentParser(
        description="Display your systemwide typing stats. \n\
                    Press 'q' to exit.",
        epilog="Made to display typing information in order \
        to type quicker and more precise."
    )

    parser.add_argument('-v', '-V', action='version',
                        version='%(prog)s ' + __version__)
    parser.add_argument('-e', '--event', type=str, help="Which keyboard event \
                        to follow", required=False,
                        default=config_parser.get('keyboard', 'event'))
    parser.add_argument('--language', type=str,
                        help="Your keyboard language", required=False,
                        default=config_parser.get('keyboard', 'language'))
    parser.add_argument('--alphabet', type=str,
                        help="Your keyboard alphabet", required=False,
                        default=config_parser.get('keyboard', 'alphabet'))
    parser.add_argument('-d', '--delay', type=int,
                        help="Time until the previous state is removed, eg. \
                        if 'delay'=5, your wpm will reset if you don't type \
                        within 5 seconds.", required=False,
                        default=config_parser.getint('program', 'delay'))
    parser.add_argument('-r', '--rate', type=int, help="Refresh-rate",
                        required=False,
                        default=config_parser.getint('program', 'rate'))
    parser.add_argument('-c', '--color', type=str, help="Change color",
                        required=False,
                        default=config_parser.get('program', 'color'))
    parser.add_argument('--rows', type=int, help="Number of rows to display \
                        when logging", required=False,
                        default=config_parser.getint('logging', 'rows'))
    parser.add_argument('-l', '--log', type=bool, help="Log frequent typed words",
                        required=False,
                        default=config_parser.getboolean('logging', 'log'))
    parser.add_argument('-s', '--save', type=str, help="File to store history \
                        for later", required=False,
                        default=config_parser.get('logging', 'save'))

    args = parser.parse_args()

    config.setup = {
        'event': args.event,
        'language': args.language,
        'alphabet': args.alphabet,
        'delay': args.delay,
        'rate': args.rate,
        'color': args.color,
        'rows': args.rows,
        'log': args.log,
        'save': args.log
    }


set_args()

screen = curses.initscr()
width = 0
height = 0
origin_x = 0
origin_y = 0


def setcolor():
    """color selection"""
    colors = {
        "red": 1,
        "green": 2,
        "yellow": 3,
        "blue": 4,
        "magenta": 5,
        "cyan": 6,
        "white": 7,
        "orange": 9,
        "random": random.randint(1, 255)
    }

    if config.setup['color'] is not None and config.setup['color'].lower() in colors.keys():
        curses.init_pair(1, 0, -1)
        curses.init_pair(2, colors[config.setup['color']], -1)
        curses.init_pair(3, 0, colors[config.setup['color']])
    else:
        pass


def addstr(y, x, string, color):
    try:
        screen.addstr(origin_y + y, origin_x + x, string, color)
    except Exception:
        return


def win_resize():
    """window resize function"""
    global width, height, origin_x, origin_y, last_t
    screen.clear()
    height, width = screen.getmaxyx()
    origin_x = floor(width / 2) - 34
    origin_y = floor(height / 2) - 4
    last_t = None


screen.keypad(1)
curses.curs_set(0)
curses.start_color()
curses.use_default_colors()

# if no arguments use these values
curses.init_pair(1, 0, -1)
curses.init_pair(2, 5, -1)
curses.init_pair(3, 0, 5)
curses.noecho()
curses.cbreak()
screen.timeout(0)

setcolor()
win_resize()


def kill():
    """exit the program"""
    config.running = False
    curses.endwin()





def ouput():
    """output various data"""
    addstr(-11, 3, "--------------- Typingstat ---------------", curses.color_pair(2))
    addstr(-9, 7, "Status", curses.color_pair(2))
    addstr(-9, 32, "Log", curses.color_pair(2))
    addstr(-7, 3, "Error ratio:", curses.color_pair(2))
    addstr(-6, 3, f"{config.typing['error_ratio']}"+" "*30, curses.color_pair(2))
    addstr(-4, 3, "Error percentage:", curses.color_pair(2))
    addstr(-3, 3, str(config.typing['error_percentage'])+"%"+" "*5, curses.color_pair(2))
    addstr(-1, 3, "Strokes:", curses.color_pair(2))
    addstr(0, 3, str(config.typing['key_strokes'])+" "*5, curses.color_pair(2))
    addstr(2, 3, "Avg Length:", curses.color_pair(2))
    addstr(3, 3, str(config.typing['word_mean_length'])+" "*5, curses.color_pair(2))
    addstr(5, 3, "Speed:", curses.color_pair(2))
    addstr(6, 3, str(config.typing['key_per_second'])+"KPS"+" "*5, curses.color_pair(2))
    addstr(8, 3, "Speed:", curses.color_pair(2))
    addstr(9, 3, str(config.typing['word_per_minute'])+"WPM"+" "*5, curses.color_pair(2))
    addstr(11, 3, "Key value:", curses.color_pair(2))
    addstr(12, 3, str(config.typing['key_current_key'])+" "*10, curses.color_pair(2))
    addstr(14, 3, "Key id:", curses.color_pair(2))
    addstr(15, 3, str(config.typing['key_current_code'])+" "*5, curses.color_pair(2))

    if config.setup['log']:
        addstr(-7, 25, "Common keys:", curses.color_pair(2))
        addstr(2, 25, "Longest words:", curses.color_pair(2))
        for pos in range(len(config.typing['key_common'])):
            id = config.typing['key_common'][pos][1]
            val = config.typing['key_common'][pos][0]
            n = 20 - len(id) - len(val)
            addstr(-6+pos, 25, val+" "*n+id, curses.color_pair(2))

        start = 0
        for pos in range(len(config.typing['word_longest'])):
            word = '"'+config.typing['word_longest'][pos]+'"'
            splitted = [word[k*20:(k+1)*20] for k in range(int(len(word)/20)+1)]
            for i, sp in enumerate(splitted):
                addstr(3+pos+i+start, 25, sp+" "*(20-len(sp)), curses.color_pair(2))
            start += len(splitted)
    screen.refresh()


def calc_error():
    """calculate current errors"""
    config.typing['error_percentage'] = round(100*config.typing['error_count'] / (config.typing['key_abc_count']+config.typing['error_count']), 2)
    config.typing['error_ratio'] = Fraction(config.typing['error_count'] / config.typing['key_strokes']).limit_denominator(50)


def calc_break():
    """calculate what to happen during a break"""
    if config.typing['key_current_key'] == "Space":
        config.typing['key_spaces_count'] += 1

    if config.typing['word_buffer'] != "":
        config.typing['word_count'] += len(config.typing['word_buffer'])
        if len(config.typing['word_time'])>0:
            # flush the 'old' words to get a more temporal typing speed
            if len(config.typing['word_time']) > config.setup['rows']:
                config.typing['word_time'] = config.typing['word_time'][-config.setup['rows']:]

            """
            Only add wpm if words takes less than 'config.setup['delay']'
            seconds to type. Therefore, the slowest you can type is
            60 / 'config.setup['delay']' WPM, but change this value if you
            feel like you need more time to type.
            """
            if config.typing['key_current_seconds']-config.typing['word_time'][-1] < config.setup['delay']:
                config.typing['word_time'].append(config.typing['key_current_seconds'])
                config.typing['word_per_minute'] = round(60 * len(config.typing['word_time']) / (config.typing['word_time'][-1]-config.typing['word_time'][0]), 2)
            else:
                config.typing['word_time'] = [config.typing['key_current_seconds']]
        else:
            config.typing['word_time'].append(config.typing['key_current_seconds'])

        # longest words
        config.typing['word_longest'].append(config.typing['word_buffer'])
        if len(config.typing['word_longest']) > config.setup['rows']:
            config.typing['word_longest'] = sorted(config.typing['word_longest'], key=len)[::-1][:config.setup['rows']]

    config.typing['word_mean_length'] = 1 + int(config.typing['word_count'] / config.typing['key_spaces_count'])
    config.typing['word_buffer'] = ""


def calc_word():
    """determine if its a word"""
    # to only recognize "real words"
    if config.typing['key_previous'] in config.setup['alphabet']+" SpaceEnter":
        config.typing['key_abc_count'] += 1
        calc_error()
        # will not count holding down on keyboard as a word
        if config.typing['key_current_key']*3 != config.typing['word_buffer'][-3:]:
            config.typing['word_buffer'] += config.typing['key_current_key']


def calc_kps():
    """calculate keys per second"""
    # Reset if keypress is a certain amount of time away
    if config.typing['key_current_seconds']-config.typing['key_query'][-1] > config.setup['delay']:
        config.typing['key_query'] = [config.typing['key_current_seconds']]

    else:
        config.typing['key_query'].append(config.typing['key_current_seconds'])
        config.typing['key_query'] = config.typing['key_query'][-config.setup['rows']:]

        kps = int(1 / ((config.typing['key_query'][-1]-config.typing['key_query'][0]) / config.setup['rows']))
        config.typing['key_query_total'].append(kps)

        # shorten the list
        config.typing['key_query_total'] = config.typing['key_query_total'][-config.setup['rows']:]

        mean = round(sum(config.typing['key_query_total']) / len(config.typing['key_query_total']), 2)
        config.typing['key_per_second'] = mean


def landing(key, code, seconds):
    """main logic function"""
    config.typing['key_strokes'] += 1
    config.typing['key_common_keys'][code] += 1
    config.typing['key_current_key'] = key
    config.typing['key_current_code'] = code
    config.typing['key_current_seconds'] = seconds

    if config.typing['key_current_key'] in ["Space", "Enter", "Esc"]:
        calc_break()

    elif config.typing['key_current_key'] in config.setup['alphabet']:
        calc_word()

    elif config.typing['key_current_key'] in ["Delete", "BkSpc"]:
        config.typing['error_count'] += 1
        calc_error()

    if config.typing['key_current_key'] == "Q" and config.typing['key_previous'] == "Right Ctrl":
        kill()
        return

    if config.typing['key_current_key'] == "R" and config.typing['key_previous'] == "Right Ctrl":
        refresh()
        return

    calc_kps()
    config.typing['key_previous'] = config.typing['key_current_key']
    keys = sorted(config.typing['key_common_keys'], key=config.typing['key_common_keys'].get, reverse=True)[:config.setup['rows']]
    config.typing['key_common'] = [[str(keyboard_layout[i]),"("+str(config.typing['key_common_keys'][i])+")"] for i in keys]

    ouput()


refresh()

logger = Keylogger(config.setup['event'], layout=keyboard_layout)
logger.start(callback=landing)
