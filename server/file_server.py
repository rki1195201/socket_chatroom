

########################################################

#Chatroom socket - CISB310 network project
#Student Name: HO MAN CHON & HO SIO HIN
#Stduent ID:   DB526683	   & DB525031

########################################################

#file_server.py
#file system server side

import sys, socket, select, re, os

if __name__ == "__main__":

	CONN_LIST = []																# socket list
	host = ''																	# file server DNS server
	port = 9213																	# DNS port

	file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)				# build TCP socket
	file_socket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )			# reuse the port after unexpect close
	file_socket.bind((host,port))												# bind socket and address
	file_socket.listen(10)														# wait client
	CONN_LIST.append(file_socket)												# add server into socket list

	while True:

		read, write, error = select.select(CONN_LIST,[],[])						# wait event in socket list

		for sock in read:														
			if sock == file_socket:															# event from server socket means new client connected
				conn, addr = file_socket.accept()											# get new client's address and create communication socket
				CONN_LIST.append(conn)														# add this socket to list
				print " Client (%s, %s) has connected the file system. " % addr
				conn.send("Welcome server\n")
			
			else:
				message = sock.recv(1024)													# if event from client

				# identify three significant command by using regular expression - upload, ls, and download
				pattern_upload = re.compile('#upload'+' '+r'[a-zA-z0-9]+'+'.txt'+'#')		
				match_upload = pattern_upload.match(message)
				pattern_ls = re.compile(r'#ls#')
				match_ls = pattern_ls.match(message)
				pattern_download = re.compile('#download'+' '+r'[a-zA-z0-9]+'+'.txt'+'#')
				match_download = pattern_download.match(message)

				# upload command match
				if match_upload:									
					filename = message[8:-1]							# get the filename, the command pattern is : upload XXXX.txt
					try:
						sock.send("Start to upload")
						with open(filename,'wb') as f:					# create the file and read data to this file
							print "file opened"
							while True:
								print "receiving data..."
								data = sock.recv(1024)					# get the file data
								print "data: \n"+ data
								if not data: 
									break
								pattern = re.compile(r'Done sending')	# identify whether done sending
								match = pattern.match(data)
								if match:
									break
								f.write(data)							# read all data into this file
						f.close()
						print "Successfully get the file."
						sock.send("Thank you for sending data.\n")
					
					except:
						sock.close()									# error then close
						CONN_LIST.remove(sock)
						print "error sock close"

				if match_ls:											# if command is ls
					sock.send("You can download those txt file.\n")		
					dirs = os.listdir(os.getcwd())						# run the terminal command ls
					for files in dirs:									
						if files.endswith(".txt"):						# get all txt file
							sock.send(files+" ")						# and send all filename which in server
					sock.send('Done')

				if match_download:										# command download
					filename = message[10:-1]							# get the file name which client want to download, the pattern is : download XXX.txt
					print filename

					try:
						FILE = open(filename,'rb')						# read the file
						l = FILE.read(1024)
						while l:
							sock.send(l)								# send the file data until done
							print "Sent"+repr(l)
							l = FILE.read(1024)
						FILE.close()
						print "Done sending"
		
	
					except:
						print "No such file or directory: " + "'" + filename + "'"

					sock.send('Done downloading')




	file_socket.close()
