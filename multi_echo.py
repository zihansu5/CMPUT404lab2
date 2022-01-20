import socket, time
from multiprocessing import Process

HOST = "localhost"
PORT = 8001
BUFFER_SIZE = 1024

def handle_echo(addr, conn):
    print("Connected by", addr)
            
    #recieve data, wait a bit, then send it back
    full_data = conn.recv(BUFFER_SIZE)
    time.sleep(0.5)
    conn.sendall(full_data)
    conn.close()

def main():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #allow reused address
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)

        print("Listening...")

        while True:
            conn, addr = s.accept()
            #start a Process darmon for handling multiple connections
            p = Process(target=handle_echo, args=(addr, conn))
            p.daemon = True
            p.start()
            print("Started process ", p)

if __name__ == "__main__":
    main()


