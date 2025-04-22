import socket  # noqa: F401

responses = {
 "ok" : b"HTTP/1.1 200 OK\r\n\r\n",

}

def main():
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("server is running...")
    connection, address = server_socket.accept() # wait for client

    with connection:
        connection.sendall(responses["ok"])


if __name__ == "__main__":
    main()
