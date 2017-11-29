import base64, os

class SessionStore:

	def __init__(self):
		# dictionary
		self.sessionData = {}
		return

	def createSession(self):
		# generates string
		newSessionId = self.generateSessionId()
		# Creates a session as a key in empty dict
		self.sessionData[newSessionId] = {}
		# Returns String sessionId
		return newSessionId

	def getSession(self, sessionId):
		#checks if session with id exists
		if sessionId in self.sessionData:
		# return the data of the sessionId which is the User_id
		# or the string sessionId
			return self.sessionData[sessionId]
		else:
			return None

	def generateSessionId(self):
		r = os.urandom(32)
		return base64.b64encode(r).decode("utf-8")

def main():

	session = SessionStore()

main()
