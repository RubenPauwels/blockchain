import socket
import lib

def client_thread(conn, ip):
    input_from_client = lib.read_connection(conn)

    #vysl = res.encode("utf8")  # encode the result string
    #conn.sendall(vysl)  # send it to client
    conn.close()  # close connection
    print('Connection ' + ip + ':' + lib.portNumber+ " ended")


def start_server():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created')

    ipaddress = "127.0.0.1"
    try:
        soc.bind((ipaddress, lib.portNumber))
        print('Socket bind complete')
    except socket.error as msg:
        import sys
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    #Start listening on socket
    soc.listen(10)
    print('Socket now listening')

    # for handling task in separate jobs we need threading
    from threading import Thread

    # this will make an infinite loop needed for
    # not reseting server for every client
    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print('Accepting connection from ' + ip + ':' + port)
        try:
            Thread(target=client_thread, args=(conn, ip)).start()
        except:
            print("Terible error!")
            import traceback
            traceback.print_exc()
    soc.close()

start_server()