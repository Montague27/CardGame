#library for multiplayer game.
#The py file should be imported to the main script.

#JSON objects.
import json

#Socket: Controls the ports to be connected to/listened to
import socket

#I think there should be a coin fliiping or some sort of method to determine
#who goes first.
def coinflip:
	pass

#Make the JSON object for request
def serialize(request):
	if(type(request) is not dict):
		print "Please pass a dict as an action object."
	return (json.dumps(request));

#Deserialize message received
def deserialize(message):
	if(type(message) is not dict):
		print "Error: the message cannot be parsed"
	return (json.loads(message))

#A general socket object
class generalSocket(object):
	#constructor
	def __init__(self, serverIpAddr="127.0.0.1", port=8964, timeout=None):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._timeout = timeout
		self._conn = None
        	self._address = address
	        self._port = port
	#Printing Error messages: should be changed
	def _printDebug(message):
		print message
	#get private read-only properties
	def getAddress(self):
		return self._address
	def getPort(self):
		return self._port
	def getTimeout(self):
		return self._timeout
	def isConnected(self):
		return (self._conn == None)
	def sendData(self,data):
		if self.isConnected():
			self._conn.send(data);
		else return "Error"
	def recvData(self):
		data = self._conn.recv(8192)
	def closeSocket(self):
		self.socket.shutdown(SHUT_RDWR)
		self.socket.close()

class serverSocket(generalSocket):
	def __init__(self, serverIpAddr, port=8964, timeout=None):
		super(serverSocket,self).__init__(self.serverIpAddr, self.port, self.timeout)
	def startServer:
		self.socket.bind((self._address,self._port))
		self.socket.listen(1)
		self._conn, client = self.socket.accept()
		self._printDebug("Connection received from client "+client)
        	self._conn.settimeout(self.timeout)
	#closes the connection
	def closeServer:
		self._conn.shutdown(SHUT_RDWR)
		self._conn.close()
		self.closeSocket();
	#Tell the remote side that the connection is closing
	def closeRemote:
		self._conn.send(serialize({"action": "close"});

class clientSocket(generalSocket):
	def __init__(self,serverIpAddr,port=8964,timeout=None):
		super(clientSocket,self).__init__(self.serverIpAddr, self.port, self.timeout)
	def closeRemote:
		self.socket.send(serialize({"action": "close"});
	def connect(self,serverIpAddr):
		self.socket.connect((self._address,self.port))
	def closeClient:
		self.closeSocket();

"""
README:
To actually implement a multiplayer game, other than starting the sockets and connections, you will have to:
1. Start the game by determining the staring player
2. When it is not your turn, call up recvData to wait for data.
3. When it is your turn, make the moves and pack the move/changes in a dictionary. Call serialize to prepare the object for sending
4. Then send the object to your opponent, summarizing the action.
5. On the client side, carry out the action. When the action is not turn-end, keep reading from the remote size(i.e. go to 2)
6. Before closing the window (or leaving game in any ways) call closeRemote to tell the remote side to end.
"""
