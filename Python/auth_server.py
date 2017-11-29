from http import cookies
from http.server import BaseHTTPRequestHandler, HTTPServer
from session_store import SessionStore
from auth_db import AuthDB
from urllib.parse import urlparse, parse_qs
from auth_db import AuthDB
import sys
import random
import json
import bcrypt


#TODO: Replace AuthDB, send_
gSessionStore = SessionStore()

class AuthServer(BaseHTTPRequestHandler):

    # METHODS

    def do_OPTIONS(self):
        # Send headers and acceptable methods that the agent can use?
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers_with_cors()

    def do_GET(self):
        self.load_cookie()
        self.load_session()

        resName, resId = self.parsePath()
        if resName == "pokemon":
            if resId:
                if 'user_id' in self.sessionData:
                    self.handlePokemonRetrieveAtIndex(resId)
                else:
                    self.send_401()
            else:
                if 'user_id' in self.sessionData:
                    self.handlePokemonRetrieve()
                else:
                    self.send_401()

        # SPLIT_PATH = self.path.split('/')
        # # list action:
        # try:
        #     id_number = SPLIT_PATH[2]
        #     if 'user_id' in self.sessionData:
        #         self.handlePokemonRetrieveAtIndex(id_number)
        #     else:
        #         self.send_401()
        #         return
        # except IndexError:
        #     pass
        #     #print('index error')
        #
        # if self.path.endswith('/pokemon'):
        #     if 'user_id' in self.sessionData:
        #         # retrieve action:
        #         self.handlePokemonRetrieve()
        #     else:
        #         self.send_401()
                #return
        else:
            self.send_404()

    def do_POST(self):
        self.load_cookie()
        self.load_session()

        # resName, resId = self.parsePath()
        # if resName == "users":
        #     if resID:
        #         self.send_404()
        #     else:
        #         self.register_user()
        # elif resName == "sessions":
        #     if resId:
        #         self.send_404()
        #     else:
        #         self.login_user()
        # elif resName == "pokemon":
        #     if 'user_id' in self.sessionData:
        #         self.handlePokemonCreate()
        #     else:
        #         self.send_401()
        # else:
        #     self.send_404()


        if self.path.endswith('/users'):
            parsed_path = self.path.split('/')
            #checks to make sure email is unique
            self.register_user()

        elif self.path.endswith('/sessions'):
            parsed_path = self.path.split('/')
            #checks email and password
            self.login_user()

        #create action:
        elif self.path.endswith('/pokemon'):
            if 'user_id' in self.sessionData:
                self.handlePokemonCreate()
            else:
                self.send_401()
        else:
            self.send_404()

    def do_DELETE(self):
        self.load_cookie()
        self.load_session()
        #delete action:
        SPLIT_PATH = self.path.split('/')
        try:
            id_number = SPLIT_PATH[2]
            if self.path.endswith(id_number):
                if 'user_id' in self.sessionData:
                    self.handlePokemonDeleteAtIndex(id_number)
                else:
                    self.send_401()
        except IndexError:
            print('index error')

    def do_PUT(self):
        self.load_cookie()
        self.load_session()
        # UPDATE ACTION:
        SPLIT_PATH = self.path.split('/')
        try:
            id_number = SPLIT_PATH[2]
            if self.path.endswith(id_number):
                if 'user_id' in self.sessionData:
                    self.handlePokemonUpdateAtIndex(id_number)
                else:
                    self.send_401()
        except IndexError:
            self.send_404()

    # ACTIONS

    def handlePokemonRetrieve(self):
        #list/getAll
        db = AuthDB()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers_with_cors()

        all_pokemon = db.getAllPokemon()
        self.wfile.write(json.dumps(all_pokemon).encode('utf-8'))

    def handlePokemonRetrieveAtIndex(self, indexID):
        # retrieve/GET(index)
        db = AuthDB()
        pokemon_by_id = db.getPokemonAtIndex(indexID)

        if pokemon_by_id != None:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers_with_cors()
            self.wfile.write(json.dumps(pokemon_by_id).encode('utf-8'))
        else:
            self.send_404()

    def handlePokemonCreate(self):
        # CREATE/POST
        db = AuthDB()
        db.createPokemon(self.parse_body())
        self.send_response(201)
        self.send_header("Content-Type", "application/json")
        self.end_headers_with_cors()

        # length = int(self.headers.get("Content-Length"))
        # data = self.rfile.read(length).decode("utf-8")
        # parsed_data = parse_qs(data)
        # print(data)
        # print(parsed_data)
        # new_pokemon = db.createPokemon(parsed_data)
        self.wfile.write(json.dumps(new_pokemon).encode('utf-8'))

    def handlePokemonDeleteAtIndex(self, indexID):
        # DELETE
        db = AuthDB()
        pDB = AuthDB()
        deleted_reference = pDB.getPokemonAtIndex(indexID)
        pokemon_to_delete = db.deletePokemonAtIndex(indexID)
        if pokemon_to_delete != None:
            self.send_response(200);
            self.send_header("Content-type", "application/json");
            self.end_headers_with_cors();
            self.wfile.write(json.dumps(deleted_reference).encode('utf-8'))
        else:
            self.send_404()

    def handlePokemonUpdateAtIndex(self, indexID):
        # update
        db = AuthDB()
        pokemon = db.getPokemonAtIndex(indexID)

        if pokemon:
            db.updatePokemonAtIndex(indexID, self.parse_body())
            self.send_response(204)
            self.end_headers_with_cors()
        else:
            self.send_404()
        # length = int(self.headers.get('Content-Length'))
        # data = self.rfile.read(length).decode("utf-8")
        # parsed_data = parse_qs(data)
        # #print(data)
        # #print(parsed_data)
        # update_pokemon = db.updatePokemonAtIndex(indexID, parsed_data)
        # #print(type(update_pokemon))
        # #print(update_pokemon)
        # if update_pokemon != None:
        #     self.send_response(204)
        #     self.send_header("Content-Type", "application/json")
        #     self.end_headers_with_cors()
        #     self.wfile.write(json.dumps(update_pokemon).encode('utf-8'))
        # else:
        #     self.send_404()

    def login_user(self):
        db = AuthDB()
        #parse body
        user_params = self.parse_body()
        #grab email and password
        user_email = user_params['email']
        user_password = user_params['password'].encode('utf-8')
        hashed = bcrypt.hashpw(user_password, bcrypt.gensalt())
        #authenticate email and verify hashed password
        user_data = db.authenticate_email(user_email)
        if user_data != None:
            db_password = user_data['password'].encode('utf-8')
            print(db_password)
            if bcrypt.checkpw(db_password, hashed):
                print("User succussfully authenticated!")
                self.sessionData['user_id'] = user_data['id']
                self.send_response(200)
                self.send_header('Content-Type', 'application/JSON')
                self.send_cookie()
                self.end_headers_with_cors()
                basic_data = db.get_user(self.sessionData['user_id'])
                self.wfile.write(json.dumps(basic_data).encode('utf-8'))
            else:
                self.send_422()
                print('That email alerady exists')
        else:
            self.send_401()

    def register_user(self):
        db = AuthDB()
        #created no response
        user_params = self.parse_body()
        print(50*('*'))
        print(user_params)
        print(50*('*'))
        #Hash the password and check to see if it matches
        user_password = user_params['password'].encode('utf-8')
        hashed = bcrypt.hashpw(user_password, bcrypt.gensalt())
        #store the hashed password in our database
        self.db_password = user_params['password']
        self.db_password = hashed
        #check if email is unique from our database
        user_email = user_params['email']
        print(50*('*'))
        print(user_email)
        print(50*('*'))

        valid = db.check_email(user_params, user_email)
        if valid == None:
            # self.send_response(422)
            # self.send_response(409)
            # self.send_header("Content-type", "text/HTML")
            # self.end_headers_with_cors()
            # self.wfile.write(bytes("<html><h4>409 Error: Email already exists</h4></html>", "utf-8"))
            self.send_422()

        else:
            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.send_cookie()
            self.end_headers_with_cors()
            print('email was unique, registration was succuessful')

    # HELPERS

    def load_session(self):
        # check for a session ID in a cookie
        # IF cookie exists:
        if 'sessionId' in self.cookie:
            self.sessionId = self.cookie['sessionId'].value
            self.sessionData = gSessionStore.getSession(self.sessionId)
            # try to load the session object using the SessionID
            # IF session data was retrieved:
            # yay! save/use it.
            if self.sessionData == None:
                self.sessionId = gSessionStore.createSession()
                self.sessionData = gSessionStore.getSession(self.sessionId)
                self.cookie['sessionId'] = self.sessionId
                #print(self.sessionId)
                #print(self.sessionData)
        # ELSE:
        # create a new session object, save/use it.
        # store the session ID in a cookie
        else:
            self.sessionId = gSessionStore.createSession()
            self.sessionData = gSessionStore.getSession(self.sessionId)
            self.cookie['sessionId'] = self.sessionId

    def load_cookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    def send_cookie(self):
        for morsel in self.cookie.values():
            # morsel is like a dictionary
            self.send_header("Set-Cookie", morsel.OutputString())

    def parse_body(self):
        length = int(self.headers.get("Content-Length"))
        data = self.rfile.read(length).decode("utf-8")
        parsed_data = parse_qs(data)
        for key in parsed_data:
            parsed_data[key] = parsed_data[key][0]
        return parsed_data

    def parsePath(self):
        if self.path.startswith("/"):
            parts = self.path[1:].split("/")
            resourceName = parts[0]
            resourceId = None
            if len(parts) > 1:
                resourceId = parts[1]
            return (resourceName, resourceId)
        return False

    def end_headers_with_cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Origin', self.headers["Origin"])
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.end_headers()
        return

    def send_404(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/HTML")
        self.end_headers_with_cors()
        self.wfile.write(bytes("<html><h4>404 Error: Not Found</h4></html>", "utf-8"))
        return

    def send_403(self):
        self.send_response(403)
        self.send_header("Content-Type", "text/HTML")
        self.end_headers_with_cors()
        self.wfile.write(bytes("<html><h4>403 Error authenticating</h4></html>", "utf-8"))
        return

    def send_401(self):
        self.send_response(401)
        self.send_header("Content-Type", "text/HTML")
        self.end_headers_with_cors()
        self.wfile.write(bytes("<html><h4>401: Unauthorized</h4></html>", "utf-8"))
        return

    def send_422(self):
        self.send_response(422)
        self.send_header("Content-Type", "text/html")
        self.end_headers_with_cors()
        self.wfile.write(bytes("<html><h4>422: Unprocessable Entity</h4></html>","utf-8"))

# def run():
#     db = AuthDB()
#     db.createUserTable()
#     db.createPokemonTable()
#     db = None # disconnect
#
#     port = 8080
#     if len(sys.argv) > 1:
#         port = int(sys.argv[1])
#
#     listen = ("0.0.0.0", port)
#     server = HTTPServer(listen, AuthServer)
#
#     print("Server listening on", "{}:{}".format(*listen))
#     server.serve_forever()

def run():
    listen = ("127.0.0.1", 8080)
    server = HTTPServer(listen, AuthServer)

    print("Listening...")
    server.serve_forever()

run()
