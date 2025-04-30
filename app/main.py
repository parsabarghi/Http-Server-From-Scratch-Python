import socket  # noqa: F401

responses = {
 "Resp-Ok" : b"HTTP/1.1 200 OK\r\n\r\n",
 "Resp-Notfound": b"HTTP/1.1 404 Not Found\r\n\r\n",
 "Resp-Badreq": b"HTTP/1.1 400 Bad Request\r\n"
}

# endpoints = {
#     "home": "/",
#     "echo": "/echo/"
# }

class HTTPRequest:
    __slots__ = ["method","path", "version", "headers", "body"]

    def __init__(self, method: str, path: str, version: str, headers: str, body: str):
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers
        self.body = body

    @classmethod
    def parse_reqline(cls, reqline: bytes):
        """handle parse the request line of HTTP"""

        try:

            req_lines = reqline.decode("utf-8").split("\r\n")
            if not req_lines:
                raise ValueError("Empty request line.")
            
            parts = req_lines[0].split()
            if len(parts) != 3: 
                raise ValueError("Invalid request line.")
            
            method, path, version = parts

            headers = {}
            i = 1
            while i < len(req_lines) and req_lines[i].strip():
                key, value = req_lines[i].split(": ", 1)
                headers[key] = value
                i += 1

            body = "\r\n".join(req_lines[i+1:]) if i+1 < len(req_lines) else ""
            

            return cls(method, path, version, headers, body)

        except Exception as e: 
            raise ValueError(f"Failed to parse request(HTTPRequest): {str(e)}")
        
    def __repr__(self): 
        return f"{__class__.__name__}: method: {self.method}, path: {self.path}, version: {self.version}, header:{self.headers}, body:{self.body}"
    
def main():
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("server is running...")
    while True:
        connection, address = server_socket.accept() # wait for client
        print(f"connect with {address}")

        with connection: 
            request_line = connection.recv(1024)
            try: 
                request = HTTPRequest.parse_reqline(request_line)
                print(request)
                if request.path == "/":
                    response = responses["Resp-Ok"]
                elif request.path.startswith("/echo"):
                    response = responses["Resp-Ok"]
                else:
                    response = responses["Resp-Notfound"]
                      
            except Exception as e: 
                print(f"exceptions error: {str(e)}")
                response = responses["Resp-Badreq"]
            
            connection.sendall(response)
                

            # if endpoints["home"] in request_line or endpoints["echo"] in request_line:
            #     connection.sendall(responses["Resp-Ok"])
            # else: 
            #     connection.sendall(responses["Resp-Notfound"])  

if __name__ == "__main__":
    main()
