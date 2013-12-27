import subprocess
import os 
import sys 
import time
from Server import Server

def main(host, port):

	mod = r"@dayz_epoch"
	
	arma_path = r"C:\Program Files (x86)\Steam\steamapps\common\Arma 2"
	oa_path = r"C:\Program Files (x86)\Steam\steamapps\common\arma 2 operation arrowhead"
	
	os.chdir(oa_path)
	
	exe_str = r"expansion\beta\arma2oa.exe"
	mod_str = r"-mod=%s;EXPANSION;ca" % arma_path
	mod2_str = r"-mod=Expansion\beta;Expansion\beta\Expansion;%s" % mod
	params = [r"-high", r"-cpuCount=4", r"-exThreads=7", r"-maxmem=2047", r"-noPause", r"-nosplash", r"-skipintro", r"-world=empty"]
	network = [r"-connect=%s" % host, r"-port=%d" % port]
	
	startup = []
	startup.append(exe_str)
	startup.append(mod_str)
	startup.append(mod2_str)
	startup.extend(params)
	startup.extend(network)
	
	# Initialize the Server
	s = Server(host, port)

	print("\nConnecting to %s at port %d..\n" % (host, port))
	while True:
		try:
			s.query()
		except:
			print("Server not respoding. Retrying..")
		else:
			print("Connected.")
			break
			
	print("\n%s\n" % s.info['hostname'])
	
	while True:
		max_players = int(s.info['maxplayers'])
		cur_players = int(s.info['numplayers'])
		print("Players: %d/%d" % (cur_players, max_players), end='\r')
		if cur_players < max_players:
			print("\nJoining the server..")
			
			# Start the game and connect to the server
			subprocess.call(startup)
			
			break
			
		time.sleep(5)
		s.query()
		
	print("\nShutting down..")
	
if __name__ == "__main__":
	try:
		hostport = str(sys.argv[1])
		hostport = hostport.split(':')
		host = hostport[0]
		port = int(hostport[1])
	except:
		print("Invalid arguments. Use 'python arma2autojoin.py host:port'") 
		sys.exit(2)
		
	main(host, port)