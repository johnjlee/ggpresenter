# ggPresenter.py
# Copyright 2008 John J. Lee
#
# This is the script that gets installed on your phone. Make sure to 
# populate the "devices" dictionary with your computer's Bluetooth
# address for easy use.

import e32
import appuifw
import socket
import key_codes

e32.ao_yield()

devices = { u"YOUR-COMPUTER": u"00:00:00:00:00:00" }


def query_for_host_and_port(default_port = 1):
    """Returns a 2-tuple of (unicode string) BT address and (int)
    port. Returns (None, None) on failure or cancel."""

    # Ask for the hostname:
    bt_choices = devices.keys()
    bt_choices.append(u"Enter manually")
    choice = appuifw.popup_menu(bt_choices, u"Choose server's BT address:")

    # If the user's choice was "enter manually", ask them to type
    # in the ID.
    if choice == (len(bt_choices) - 1):
        host = appuifw.query(u"Input server's BT address:", 'text', u"00:00:00:00:00:00")
        if host == None:
            return (None, None)
    else:
        host = devices.values()[choice]

    # Now ask for the port:
    port_input = appuifw.query(u"Input server's port:", 'number', default_port)
    if port_input == None:
        return (None, None)
    else:
        port_input = int(port_input)

    return (host, port_input)
    
    


class ggPresenterApp:
    def __init__(self):
        self.lock = e32.Ao_lock()

        self.old_title = appuifw.app.title
        self.exit_flag = False
        self.server_sock = None
        self.server_addr = None
        self.server_port = None
        self.has_connection = False
        
        appuifw.app.title = u"ggPresenter"
        appuifw.app.exit_key_handler = self.abort
        appuifw.app.body = appuifw.Canvas(self.handle_redraw,
                                          self.handle_event,
                                          self.handle_resize)
        appuifw.app.menu = [ (u"Connect to server", self.handle_connect),
                             (u"Exit", self.close) ]
        
    def loop(self):
        self.redraw()
        self.lock.wait()
        while not self.exit_flag:
            self.refresh()
            self.lock.wait()
                
    def close(self):
        appuifw.app.menu = []
        appuifw.app.body = None
        appuifw.app.exit_key_handler = None
        appuifw.app.title = self.old_title
        if (self.server_sock != None):
            self.server_sock.close()

    def abort(self):
        self.exit_flag = True
        self.lock.signal()

    def handle_redraw(self, region):
        self.redraw()

    def handle_resize(self, size):
        self.redraw()

    def redraw(self):
        appuifw.app.body.clear()
        appuifw.app.body.text((10, 30),
                              unicode("Connected to %s" % self.server_addr))
        appuifw.app.body.text((10, 40),
                              unicode("on port %s" % self.server_port))

    def handle_connect(self):
        try:
            (host, port) = query_for_host_and_port(3)
            if (host == None or port == None):
                return

            if self.has_connection:
                self.has_connection = False
                if self.server_sock != None:
                    self.server_sock.close()
            self.server_addr = host
            self.server_port = port
            self.server_sock = socket.socket(socket.AF_BT, socket.SOCK_STREAM)
            self.server_sock.connect((self.server_addr, self.server_port))
            appuifw.note(u"Connection successful!", "info")
            self.has_connection = True
        except:
            appuifw.note(u"Connection failed!", "info")
            self.server_sock = None
            self.server_addr = None
            self.has_connection = False
            self.redraw()
        self.redraw()
        
    def handle_event(self, dict):
        if self.has_connection:
            if (dict['type'] == appuifw.EEventKeyUp):
                if (dict['scancode'] - 48 >= 0 and
                    dict['scancode'] - 48 <= 9):
                    self.send_message(str(dict['scancode'] - 48))
                elif dict['scancode'] == key_codes.EScancodeUpArrow:
                    self.send_message("up")
                elif dict['scancode'] == key_codes.EScancodeDownArrow:
                    self.send_message("down")
                elif dict['scancode'] == key_codes.EScancodeLeftArrow:
                    self.send_message("left")
                elif dict['scancode'] == key_codes.EScancodeRightArrow:
                    self.send_message("right")
                elif dict['scancode'] == key_codes.EScancodeSelect:
                    self.send_message("select")
                elif dict['scancode'] == key_codes.EScancodeBackspace:
                    self.send_message("backspace")
                elif dict['scancode'] == key_codes.EScancodeHash:
                    self.send_message("#")
                elif dict['scancode'] == key_codes.EScancodeStar:
                    self.send_message("*")
                elif dict['scancode'] == key_codes.EScancodeEdit:
                    self.send_message("edit")
        
        self.redraw()

    def send_message(self, key):
        if (self.server_sock != None):
            try:
                self.server_sock.send(str(key))
            except:
                appuifw.note(u"Lost connection!", "info")
                self.has_connection = False
                self.server_sock.close()
                self.server_sock = None
                self.server_addr = None
                self.server_port = None
        
def main():
    app = ggPresenterApp()
    try:
        app.loop()
    finally:
        app.close()

if __name__ == "__main__":
    main()
