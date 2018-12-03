

########################################################

#Chatroom socket - CISB310 network project
#Student Name: HO MAN CHON & HO SIO HIN
#Stduent ID:   DB526683	   & DB525031

########################################################

#server.py
#chatroom server side

import sys, socket, select

# send the message to all socket connect by client
def broadcast(sock, message):
	for socket in CONN_LIST:							# client sock list
		if socket != main_socket and socket != sock:	# Not send back to the client who send the data out
			try:
				socket.sendall(message)					# send
			except:
				socket.close()
				CONN_LIST.remove(socket)


if __name__ == "__main__":

	CONN_LIST = []										# connect list
	host = ''											# set the DNS server
	port = 44452										# set the port

	main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)			# build the TCP socket
	main_socket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )		# reuse the port after unexpect close
	main_socket.bind((host,port))											# bind the socket and address
	main_socket.listen(10)													# wait client
	CONN_LIST.append(main_socket)											# add main server in socket list

	while True:
	
		read, write, error = select.select(CONN_LIST,[],[])					# wait socket event

		for sock in read:													
			if sock == main_socket:											# if event from server that means there is new client connected
				conn, addr = main_socket.accept()							# get new client's address and create communication socket
				CONN_LIST.append(conn)										# add this socket to socket list
				print " Client (%s, %s) has connected. " % addr
				broadcast(conn, "\n (%s, %s) entered room. \n" % addr )	
			
			else:
				try:
					data = sock.recv(4096)									# if event from client, get the msg
					if data:
						broadcast(sock, data)								# and broadcast the msg
				except:
					print "(%s, %s) is offline. " % addr
					broadcast(sock, "\n (%s, %s) has leaved room. \n" % addr )
					sock.close()
					CONN_LIST.remove(sock)

	main_socket.close()

