#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# File name: typingstat/communicate.py
# Description: Main file for communication with typingstat daemon
# Author: irreq (irreq@protonmail.com)
# Date: 28/12/2021

import socket
import signal

from . import var

class GracefulKiller:
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        self.kill_now = True

class Typingstat(GracefulKiller):
    def __init__(self, udp_ip=var.config.udp_ip, udp_port=var.config.udp_port, debug=var.config.debug, **kwargs):
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.debug = debug
        self.config = kwargs
        self.sock = False
        self.timeout_count = 0

        # The previous successful poll Eg, 'None' is discarded
        self.previous_poll = None
        self.previous_poll_2 = None

        self.connect()

        if self.is_socket_closed(self.sock):
            self.sock = False

        super().__init__()


    def is_socket_closed(self, sock):
        try:
            # Will try to read bytes without blocking and also without removing them from buffer (peek only)
            data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
            if len(data) == 0:
                return True
        except BlockingIOError:
            return False  # Socket is open and reading from it would block
        except ConnectionResetError:
            return True  # Socket was closed for some other reason
        except Exception as e:
            if self.debug:
                print("Unexpected exception when checking if a socket is closed, %s") % str(e)
            return False
        return False


    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # [Errno 98] Address already in use, https://stackoverflow.com/questions/4465959/python-errno-98-address-already-in-use
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.udp_ip, self.udp_port))
        except Exception as e:
            if self.debug:
                print(e)
            self.sock = False

    def poll(self):
        data = None
        if not self.is_socket_closed(self.sock):
            self.sock.settimeout(5)
            try:
                # buffer size is 1024 bytes
                data, addr = self.sock.recvfrom(1024)
                data = data.decode("utf8")
                self.timeout_count = 0
            except:
                if self.debug:
                    print("Nothing received for %ds. Is the daemon running?" % (self.timeout_count * 5))
                self.timeout_count += 1
            self.sock.settimeout(None)
            if data is not None:
                data = data.split(",")
                skel = ("kps", "wpm", "error", "strokes")
                data = {k:int(data[i]) for i, k in enumerate(skel)}

                self.previous_poll = self.previous_poll_2
                self.previous_poll_2 = data

        return data
