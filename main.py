import sys, getopt
import time
import threading
import socket


PFLAG = "PFLAG"
FLAG = "FLAG"
STOPSERV = "STOPSERV"
PING = 3
STOP = 4

HELPSTRING = "\nUsage:\n\t-h: name of host to establish pipe on\n\t-p: port to establish pipe on\n\t--help: display this message\n\t--stop-server: send stop flag to server"
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
    return (1 if data.decode() == FLAG else 0)


"""
Resets server connection, waits, and returns new connection socket object
"""

def resetServ(sin, conn):
    conn.close()
    sin.listen(1)
    co, addr = sin.accept()
    co.sendall(FLAG.encode())
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
    con.sendall(FLAG.encode())
    ad, po = con.getpeername()
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

"""
Main function 
"""

def main():

    """
    Host and port to open/connect to pipe on, defaults to local on port 28000
    """

    hostname = "127.0.0.1"
    port = 28000
    isEnd = False
    
    try:
        args, vals = getopt.getopt(sys.argv[1:], "h:p:", longopts=["help", "stop-server"])

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
            isEnd = True
    if isEnd:
        pingStop((hostname, port), STOP)
        exit(0)

    ADDRESS = (hostname, port)

    """
    Dual client/server functionality, dependent on the result of the ping
    """

    if not pingStop(ADDRESS, PING):
        """
        KeyboardInterrupt exception to be implemented, currently terminates through calling main after
        server has started with --stop-server terminal arguement
        """
        thread = threading.Thread(target=lambda: serv(ADDRESS))
        thread.start()
        thread.join()
        
    else:

        """
        Currently takes input from terminal, reading from file to be implemented (see extern.py)
        """

        print("Pipe detected on " + hostname + ":" + str(port) + "\n")
        time.sleep(2)
        sin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sin.connect(ADDRESS)
        data = input("Msg:")
        sin.sendall(data.encode())
        data = sin.recv(BUFF)

if __name__ == "__main__":
    main()
