

########################################################

#Chatroom socket - CISB310 network project
#Student Name: HO MAN CHON & HO SIO HIN
#Stduent ID:   DB526683	   & DB525031

########################################################

#file_client.py
#file system client side

import sys, socket, select, re, os

# print a header
def PrintCmd():
	sys.stdout.write("[Input command]: ")
	sys.stdout.flush()

# print help info
def help():
	print "\n Upload file to the server by: 		upload filename "
	print " Download file to the server by: 	download filename "
	print " List file in the server by: 		ls"
	print " List file in your pc by: 		lm \n"

# upload function
def upload(filename):
	try:
		FILE = open(filename,'rb')	# read the file 
		l = FILE.read(1024)			
		while l:
			s.send(l)				# send file to server until done
			print "Sent"+repr(l)
			l = FILE.read(1024)
		FILE.close()
		print "Done sending"
		
	except:
		print "No such file or directory: " + "'" + filename + "'"
	

if __name__ == "__main__":

	# command must correct else close the program
	if len(sys.argv) < 3:
		print "Usage: python file_client.py hostname port"
		sys.exit()
	help()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)							# set TCP socket
	main = socket.gethostname()														# get the client pc name
	host = sys.argv[1]																# get destination hostname
	port = int(sys.argv[2])															# get destination port

	try:
		s.connect((host,port))														# connect to the address
	except:
		print " Fail to connect server. "
		sys.exit()

	PrintCmd()

	while True:
	
		buff = [sys.stdin, s]														# socket list
		read, write, error = select.select( buff, [], [] )							# listen the socket event
		
		for sock in read:
			if sock == s:															# event form server socket
				data = sock.recv(1024)												# get some data
				if not data:
					print " Disconnected to the chatroom. "
					sys.exit()
				else:
					sys.stdout.write(data)											# print it
					PrintCmd()
			else:
				message = sys.stdin.readline()										# from client itself

				if message == 'help()\n':											# command help()
					help()

				# identify which command is
				pattern_upload = re.compile('upload'+' '+r'[a-zA-z0-9]+'+'.txt')
				match_upload = pattern_upload.match(message)
				pattern_ls = re.compile('ls')
				match_ls = pattern_ls.match(message)
				pattern_download = re.compile('download'+' '+r'[a-zA-z0-9]+'+'.txt')
				match_download = pattern_download.match(message)
				pattern_lsmy = re.compile('lm')
				match_lsmy = pattern_lsmy.match(message)

				# command upload match
				if match_upload:
					filename = message[7:-1]					# get the filename, command pattern: upload XXX.txt
					print filename
					s.send('#upload'+' '+filename+'#')			# send the identify code
					data = s.recv(1024)							# allow message from server
					print data
					upload(filename)							# upload the file
					s.send('Done sending')

				# command ls match
				if match_ls:
					s.send('#ls#')								# send the ls command
					while True:
						data = s.recv(4096)						# get the server file list 
						if not data: break
						print data								# print list
						pattern = re.compile(r'Done')
						match = pattern.search(data)			# if done, then break
						if match: 
							break

				# command lm - list client file list
				if match_lsmy:
					dirs = os.listdir(os.getcwd())				# terminal command ls in client pc
					for files in dirs:
						if files.endswith(".txt"):				# print all txt file
							print files+" "
			
				# command download match
				if match_download:
					filename = message[9:-1]					# get filename, command pattern: download XXX.txt
					print filename
					s.send('#download'+' '+filename+'#')		# send request
					print "start to download"
					try:
						with open(filename,'wb') as f:			# create the file from server
							print "file opened"
							while True:
								print "sending data..."
								data = s.recv(1024)				# get the file data
								
								if not data: 
									break
								print "data: \n"+ data
								pattern = re.compile(r'Done downloading')
								match = pattern.search(data)
								if match:
									break
								f.write(data)					# write data into the file
						f.close()
						print "Successfully get the file."
						
					except:
						sock.close()
						
						print "error sock close"
						
				PrintCmd()
				
				
				

