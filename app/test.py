import unittest
from main import responses, HttpRequest, HttpResponse



class TestHttpRequest(unittest.TestCase):
    def test_valid_parse(self):
        req_line = b"GET / HTTP/1.1\r\n\r\n"
        req = HttpRequest.parse_reqline(req_line)
        self.assertEqual(req.method, "GET")
        self.assertEqual(req.path, "/")
        self.assertEqual(req.version, "HTTP/1.1")
        self.assertEqual(req.body, "")
        self.assertEqual(req.headers, {})