import sqlite3
import json

def dict_factory(curr, row):
    d = {}
    for idx, col in enumerate(curr.description):
        d[col[0]] = row[idx]
    return d

class AuthDB:

    def __init__(self):
        self.conn = sqlite3.connect("../users.db")
        self.conn.row_factory = dict_factory
        self.curr = self.conn.cursor()
    def create_user(self, data):
        self.curr.execute("INSERT INTO users (f_name, l_name, email, password) VALUES (?,?,?,?)", [data['f_name'][0], data['l_name'][0], data['email'][0], data['password'][0]])
        self.conn.commit()
    #checks to verify the email is unique before creating the user
    def check_email(self, data, email):
        self.curr.execute("SELECT * FROM users WHERE email=(?)", [email])
        row = self.curr.fetchone()
        if row != None:
            print('That email already exists')
            return None
        else:
            self.create_user(data)
            return data
    #verifies the email to be logged in actually exists
    def authenticate_email(self, email):
        self.curr.execute("SELECT * FROM users WHERE email=(?)", [email])
        row = self.curr.fetchone()
        if row != None:
            return row
        else:
            return None
    #gets basic user data from the user_id stored in the sessionId cookie?
    def get_user(self, user_id):
        self.curr.execute("SELECT f_name, l_name, email FROM users WHERE id=(?)", [user_id])
        row = self.curr.fetchone()
        return row


###################
###Pokemon Table###
###################

    def createPokemon(self, data):
        self.curr.execute("INSERT INTO pokemon (name, gender, type, size, strength, weakness) VALUES (?, ?, ?, ?, ?, ?)", [data['name'][0],data['gender'][0],data['type'][0],data['size'][0],data['strength'][0],data['weakness'][0]])
        self.conn.commit()
        return data
	#get all
    def getAllPokemon(self):
	    self.curr.execute("SELECT * FROM pokemon")
	    rows = self.curr.fetchall()
	    myList= []
	    for row in rows:
	    	myList.append(row)
	    return myList
	#get{id}
    def getPokemonAtIndex(self, index):
        self.curr.execute("SELECT * FROM pokemon WHERE id=(?)", [index])
        row = self.curr.fetchone()
        if row != None:
            print(json.dumps(row))
            self.conn.commit()
            self.curr.close()
            return row
        else:
            return None
	#delete
    def deletePokemonAtIndex(self, index):
        self.curr.execute("DELETE FROM pokemon WHERE id=(?)", [index])
        row = self.curr.fetchall()
        #print(row)
        if row != None:
            self.conn.commit()
            self.conn.close()
            return row
        else:
            return None
	#update
    def updatePokemonAtIndex(self, index, data):
        self.curr.execute('UPDATE pokemon SET name=?, gender=?, type=?, size=?, strength=?, weakness=? WHERE id=?', (data['name'][0],data['gender'][0],data['type'][0],data['size'][0],data['strength'][0],data['weakness'][0],index))
        #print(json.dumps(rows))
        self.curr.execute("SELECT * FROM pokemon where id=(?)",[index])
        pokemon = self.getPokemonAtIndex(index)
        #print(test)
        if pokemon != None:
            self.conn.commit()
            self.conn.close()
            return pokemon
        else:
            return None

def main():
    test = AuthDB()

    myDict = {'fname':['Jeff'], 'lname': ['Haberle'], 'email': ['jeffrey.haberle@gmail.com'], 'password': ['CharlieBrown']}
    test.createUser(myDict)

if __name__ == "__main__": main()
