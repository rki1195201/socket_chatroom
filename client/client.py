

########################################################

#Chatroom socket - CISB310 network project
#Student Name: HO MAN CHON & HO SIO HIN
#Stduent ID:   DB526683	   & DB525031

########################################################

#client.py
#chatroom client side

import sys, socket, select

# Print client computer name such as " [You]: "
def PrintName():
	sys.stdout.write("[" + main + "]: ")
	sys.stdout.flush()											# for input buffer

if __name__ == "__main__":

	# Client must input correct number of argument 
	if len(sys.argv) < 3:
		print "Usage: python client.py hostname port"
		sys.exit()

	# Create TCP socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	main = socket.gethostname()									# Get the client pc name
	host = sys.argv[1]											# set the destination hostname
	port = int(sys.argv[2])										# set the destination port

	try:
		s.connect((host,port))									# connect to the server
	except:
		print " Fail to connect server. "						# if error exit the system
		sys.exit()

	PrintName()					

	# Catch the server socket broadcast and send out the message
	while True:
	
		buff = [sys.stdin, s]									# socket list
		read, write, error = select.select( buff, [], [] )		# listen for the socket list
		
		for sock in read:										# identify select() form server socket or sys.stdin
			if sock == s:										# if form server, this is broadcast
				data = sock.recv(4096)							# receive the broadcast message
				if not data:									
					print " Disconnected to the chat room. "
					sys.exit()
				else:
					sys.stdout.write(data)						# if data is exist, print the data in chatroom
					PrintName()
			else:												# data form client - sys.stdin
				message = sys.stdin.readline()					# read the data
				s.send(message)									# and send to server
				PrintName()
				
				
				

