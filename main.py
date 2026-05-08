import sys, getopt, os
import time
import threading
import socket
import numpy as np
from extern import Reader


PFLAG = "PFLAG"
FLAG = "FLAG"
STOPSERV = "STOPSERV"
PING = 3
STOP = 4

HELPSTRING = "\nUsage:\n\t-h: name of host to establish pipe on\n\t-p: port to establish pipe on\n\t-i: file data to send through pipe\n\t--help: display this message\n\t--stop-server: send stop flag to server"
BUFF = 2048

def strExit():
    print(HELPSTRING)
    exit(0)

"""
Function both sends the ping flag, and sends stop flag
"""

def pingStop(addr, which):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(addr)
    except:
        return 0
    data = s.recv(BUFF)
    s.sendall((PFLAG.encode() if which == PING else STOPSERV.encode()))
    s.close()
    return (1 if data[:len(FLAG)].decode() == FLAG else 0)


"""
Resets server connection, waits, and returns new connection socket object
"""

def resetServ(sin, conn):
    conn.close()
    sin.listen(1)
    co, addr = sin.accept()
    co.sendall((FLAG + str(os.getpid())).encode())
    return co

"""
Server loop, prints message sent from client and disconnects, except in the case of a ping where it
simply disconnects
"""

def serv(add):

    si = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    si.bind(add)
    print("Pipe established on " + add[0] + ":" + str(add[1]))
    si.listen(1)
    con, addr = si.accept()
    con.sendall((FLAG + str(os.getpid())).encode())
    ad, po = con.getpeername()
    data = con.recv(BUFF)
    while True:
        data = con.recv(BUFF)
        if data == STOPSERV.encode():
            si.close()
            con.close()
            break
        elif data == PFLAG.encode():
            con = resetServ(si, con)
            continue
        print(ad + ":" + str(po) + ": " + data.decode())
        con = resetServ(si, con)

def main():

    """
    Host and port to open/connect to pipe on, defaults to local on port 28000
    """
    inFile = ""
    hostname = "127.0.0.1"
    port = 28000
    
    try:
        args, vals = getopt.getopt(sys.argv[1:], "h:p:i:", longopts=["help", "stop-server"])
        if len(sys.argv) > 2 and "-i" not in np.array(args)[:, 0] and "--stop-server" not in np.array(args)[:, 0]:
            print("requires input file, see usage below")
            raise getopt.error

    except getopt.error:
        strExit()

    for arg, val in args:
        if arg == "-h":
            hostname = val
        elif arg == "-p":
            port = int(val)
        elif arg == "--help":
            strExit()
        elif arg == '--stop-server':
            pingStop((hostname, port), STOP)
            exit(0)
        elif arg == "-i":
            inFile = val

    isClient = pingStop((hostname, port), PING)
    if not inFile and isClient:
            print("requires input file, see usage below")
            strExit()

    f = Reader()
    ADDRESS = (hostname, port)
    """
    Dual client/server functionality, dependent on the result of the ping
    """

    if not isClient:
        """
        KeyboardInterrupt exception to be implemented, currently terminates through calling main after
        server has started with --stop-server terminal arguement
        """
        if inFile:
            print("No pipe detected to send file data through, continuing as server")

        thread = threading.Thread(target=lambda: serv(ADDRESS))
        thread.start()
        thread.join()
        
    else:

        """
        Reads from file for data coming through channels (to be implemented)
        """

        inF = Reader(inFile)

        print("Pipe detected on " + hostname + ":" + str(port) + "\n")
        time.sleep(2)
        sin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sin.connect(ADDRESS)
        data = sin.recv(BUFF)
        opid = int(data[len(FLAG):])
        data = inF.read(BUFF)
        sin.sendall(data.encode())

if __name__ == "__main__":
    main()
