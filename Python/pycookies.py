from http import cookies
from http.server import BaseHTTPRequestHandler, HTTPServer
from session_store import SessionStore

gSessionStore = SessionStore()

class MyRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.load_cookie()

        if self.path.startswith("/biteme"):
            if "counter" in self.cookie:
                counter = int(self.cookie["counter"].value)
            else:
                counter = 0
            self.cookie["counter"] = counter + 1

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_cookie()
            self.end_headers()
            self.wfile.write(bytes(self.cookie["counter"].value + " times bitten.", "utf-8"))

        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("404 Not Found", "utf-8"))

    def load_session(self):
        pass
        # check for a session ID in a cookie
        # IF cookie exists:
            # try to load the session object using the ID
            # IF session data was retrieved:
                # yay! save/use it.
            # ELSE:
                # create a new session object, save/use it.
                # store the session ID in a cookie
        # ELSE:
            # create a new session object, save/use it.
            # store the session ID in a cookie

    def load_cookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    def send_cookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

def run():
    listen = ("127.0.0.1", 8080)
    server = HTTPServer(listen, MyRequestHandler)

    print("Listening...")
    server.serve_forever()

run()
