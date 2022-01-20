import socket, time, sys

#define global address and buffer size
HOST = "localhost"
PORT = 8001
BUFFER_SIZE = 1024

#get ip
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def main():
    host = 'www.google.com'
    port = 80

    #create socket 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        #acts like server
        print("Starting proxy server")
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(2)

        while True:
            #connect proxy_start
            conn, addr = proxy_start.accept()
            print("Connected by", addr)
            
            #acts like client
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                remote_ip = get_remote_ip(host)

                #connect proxy_end
                proxy_end.connect((remote_ip, port))

                #send data and shutdown
                full_data = conn.recv(BUFFER_SIZE)
                print(f"Sending received data {full_data} to Google")
                proxy_end.sendall(full_data)
                proxy_end.shutdown(socket.SHUT_WR)

                data = proxy_end.recv(BUFFER_SIZE)
                print(f"Sending recieved data {data} to client")
                #send data back
                conn.send(data)

            conn.close()

if __name__ == "__main__":
    main()




