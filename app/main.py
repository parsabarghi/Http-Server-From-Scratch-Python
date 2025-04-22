import socket  # noqa: F401

responses = {
 "ok" : b"HTTP/1.1 200 OK\r\n\r\n",
 "not found": b"HTTP/1.1 404 Not Found\r\n\r\n"
}

def main():
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("server is running...")
    while True:
        connection, address = server_socket.accept() # wait for client
        print(f"connect with {address}")

        with connection: 
            data = connection.recv(1024).split(b"\r\n")[0]
            if data == b"GET / HTTP/1.1":
                connection.sendall(responses["ok"])
            else: 
                connection.sendall(responses["not found"])  

if __name__ == "__main__":
    main()
