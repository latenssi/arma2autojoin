import subprocess
import os 
import sys 
import time
from Server import Server


class Arma2AutoJoin:
	
	server_mon = None
	
	def __init__(self, host=None, port=None, mod = r"@dayz_epoch"):
		self.host = host
		self.port = port
		self.mod = mod
		if self.host and self.port:
			self.server_mon = Server(host, port)
			
	def connect(self, host, port, mod):
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
		
		subprocess.call(startup)
	
	def monitor(self, auto_connect=True):
		while True:
			self._query()
			max_players = int(self.server_mon.info['maxplayers'])
			cur_players = int(self.server_mon.info['numplayers'])
			print("Players: %d/%d" % (cur_players, max_players), end='\r')
			if auto_connect and cur_players < max_players:
				break
			time.sleep(5)
		
		if auto_connect:
			self.connect(host=self.host, port=self.port, mod=self.mod)
			
	def _query(self):
		while True:
			try:
				self.server_mon.query()
			except:
				print("Server not respoding. Retrying..")
			else:
				break
		
def main(host, port):
	aaj = Arma2AutoJoin(host=host, port=port)
	aaj.monitor()
	
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