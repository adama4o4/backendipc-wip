# backendipc-wip
DISCLAIMER: Project was created for educational purposes only, and has not been audited for security. Use at your own risk.

Requires: 
- Python 3.8+
- Numpy 2.0+

Install dependencies with:
pip install -r requirements.txt

Prototype of a simple cross-platform IPC tool, to create an enduring socket (or "pipe") with multiple channels through
which processes may be able to send data. Currently functions as a dual client/server implementation, built using only the python standard library.

How to run:
py main.py
py main.py -h 127.0.0.1
py main.py -p 50000

Output of py main.py --help:

Usage:
        -h: name of host to establish pipe on
        -p: port to establish pipe on
        --help: display this message
        --stop-server: send stop flag to server

When first run, if no server is found on the specified host and port (or if no host/port is specifed, defaults to 127.0.0.1:28000) the script starts a TCP/IPv4 server on given address.

If a server is detected, the user is prompted for a message that will be displayed on the server terminal.

To close the server, the main.py script is run with the --stop-server flag to send the stop flag to the server.

This project uses the following third party software:

- NumPy - BSD 3-Clause license

This project is licensed under the MIT license.

