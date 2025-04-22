import socket  # noqa: F401

responses = {
 "ok" : b"HTTP/1.1 200 OK\r\n\r\n",
 "not found": b"HTTP/1.1 404 Not Found\r\n\r\n"
}

def main():
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("server is running...")
    connection, address = server_socket.accept() # wait for client

    with connection:
        print(f"connect with {address}")
        while True:
            data = connection.recv(1024)
            if data == b"/":
                connection.sendall(responses["ok"])
            else: 
                connection.sendall(responses["not found"])  

if __name__ == "__main__":
    main()
