import bluetooth

"""
socketConfiguration

Creates the bluetooth socket connection between the server and client
Specify the hardware address of the server as well as the port
the two devices will be communicating on.

Arguments: None

Returns:
    sock -- The bluetooth socket
"""
def socketConfiguration():
    # RF Comm Socket Configuration Parameters
    bd_addr = "B8:27:EB:5B:2A:AA"
    port = 2

    # Start and Connect Socket
    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((bd_addr, port))

    print('socket Connection Successful')

    return sock
