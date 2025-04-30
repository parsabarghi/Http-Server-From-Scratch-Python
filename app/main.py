import socket  # noqa: F401

responses = {
 200: b"HTTP/1.1 200 OK\r\n",
 404: b"HTTP/1.1 404 Not Found\r\n",
 400: b"HTTP/1.1 400 Bad Request\r\n"
}

# endpoints = {
#     "home": "/",
#     "echo": "/echo/"
# }

class HttpRequest:
    __slots__ = ["method","path", "version", "headers", "body"]

    def __init__(self, method: str, path: str, version: str, headers: str, body: str):
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers
        self.body = body

    @classmethod
    def parse_reqline(cls, reqline: bytes)-> "HttpRequest":
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
            raise ValueError(f"Failed to parse request(HttpRequest): {str(e)}")
        
    def __repr__(self): 
        return f"{__class__.__name__}: method: {self.method!r}, path: {self.path!r}, version: {self.version!r}, header:{self.headers!r}, body:{self.body!r}"
    
class HttpResponse:
    __slots__ = ["status", "header","body"]

    def __init__(self, status: bytes, header: bytes, body:bytes):
        self.status = status
        self.header = header
        self.body = body

    def to_bytes(self) -> bytes: 
        """convert response to bytes for transmission"""
        return self.status + self.header + b"\r\n" + self.body
   
    @classmethod
    def build_response(cls, http_req: HttpRequest) -> "HttpResponse":
        """building http response"""

        # handle "/"
        if http_req.path == "/" and http_req.method == "GET":
            body = b"Hello, World"
            header = (
                b"Content-Type: text/plain\r\n"
                b"Content-Length: " + str(len(body)).encode() + b"\r\n"
            )
            status = responses[200]

        # handle "/echo/*"
        elif http_req.path.startswith("/echo") and http_req.method == "GET":
            body = http_req.path[len("/echo/"):].encode("utf-8")
            header = (
                b"Content-Type: text/plain\r\n"
                b"Content-Length: " + str(len(body)).encode() + b"\r\n"
            )
            status = responses[200]

        # handle not found
        else:
            body = b""
            header = b""
            status = responses[404]

        
        return cls(status, header, body)
    

    def __repr__(self):
        return f"{__class__.__name__}: status: {self.status!r}, header: {self.header!r}, body: {self.body!r} "
        




def main():
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("server is running...")
    while True:
        connection, address = server_socket.accept() # wait for client
        print(f"connect with {address}")

        with connection: 
            request_line = connection.recv(1024)
            try: 
                request = HttpRequest.parse_reqline(request_line)
                print(request)
                response = HttpResponse.build_response(request)
                print(response)
                connection.sendall(response.to_bytes())
                
                      
            except Exception as e: 
                print(f"exceptions error: {str(e)}")
                connection.sendall(responses[400])
                
            
                

            # if endpoints["home"] in request_line or endpoints["echo"] in request_line:
            #     connection.sendall(responses["Resp-Ok"])
            # else: 
            #     connection.sendall(responses["Resp-Notfound"])  

if __name__ == "__main__":
    main()
