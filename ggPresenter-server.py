# ggPresenter-server.py
# Copyright 2008 John J. Lee
#
# This can do one of two things:
# If you're using xpdf, you can use the remote capabilities to send it
# commands. So you supply the xpdf server name on the command line. Make
# sure to check that the command that is actually being sent (at the bottom
# of the loop) is the xpdf command and not an xdotool command.
#
# If you don't want to use xpdf, you can just rig it to emulate any
# keystroke (it uses xdotool to do that). You will need to have
# xdotool installed. When doing this, the xpdf-server commandline
# argument is ignored.

import bluetooth
import sys
import os


def usage(name):
    print "%s <XPDF_SERVER_NAME>" % name

def xdotool_command(command):
    return "xdotool key %s" % command

def xpdf_command(server, command):
    return "xpdf -remote %s -exec %s" % (server, command)
    
if (len(sys.argv) < 2) or (sys.argv[1] == None):
    usage(sys.argv[0])
    sys.exit()

xpdf_server = sys.argv[1]

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 3

print "Listening for connection on port %d..." % port
server_sock.bind(("", port))
server_sock.listen(1)

(client_sock, address) = server_sock.accept()
print "Accepted connection from ", address

while True:
    data = client_sock.recv(1024)
    print "received [%s]" % data
    if (data == "0"):
        break
    elif (data == "1"):
        break
    elif (data == "2"):
        break
    elif (data == "3"):
        break
    elif (data == "4"):
        break
    elif (data == "5"):
        break
    elif (data == "left"):
        os.system(xdotool_command("space"));
#        os.system(xpdf_command(xpdf_server, "nextPage"))
    elif (data == "right"):
        os.system(xdotool_command("BackSpace"));
#        os.system(xpdf_command(xpdf_server, "prevPage"))
    

client_sock.close()
server_sock.close()
