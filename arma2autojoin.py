import subprocess
import os 
import sys 
import time
import configparser
import argparse
from Server import Server

CONF_FILE = "arma2autojoin.cfg"

class Arma2AutoJoin:
	
	server_mon = None
	
	def __init__(self, host, port, mod, arma_path, oa_path, cpucount=None, exthreads=None, maxmem=None):
		self.host = host
		self.port = port
		self.mod = mod
		self.arma_path = arma_path
		self.oa_path = oa_path
		self.cpucount = cpucount
		self.exthreads = exthreads
		self.maxmem = maxmem
		
	def connect(self):
		os.chdir(self.oa_path)
		exe_str = r"expansion\beta\arma2oa.exe"
		mod_str = r"-mod=%s;EXPANSION;ca" % self.arma_path
		mod2_str = r"-mod=Expansion\beta;Expansion\beta\Expansion;%s" % self.mod
		params = [
			r"-high", 
			r"-noPause", 
			r"-nosplash", 
			r"-skipintro", 
			r"-world=empty",
		]
		
		if self.cpu_count:
			params.append(r"-cpuCount=%d" % self.cpucount)
		
		if self.ext_hreads:
			params.append(r"-exThreads=%d" % self.exthreads)
			
		if self.max_mem:
			params.append(r"-maxmem=%d" % self.maxmem)
			
		network = [r"-connect=%s" % self.host, r"-port=%d" % self.port]
		
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
			self.connect()
			
	def _query(self):
		if not self.server_mon and (self.host and self.port):
			self.server_mon = Server(self.host, self.port)
			
		while True:
			try:
				self.server_mon.query()
			except:
				print("Server not respoding. Retrying..")
			else:
				break
		
def main(host=None, port=None):
	config = configparser.RawConfigParser()
	config.read(CONF_FILE)
	
	if host:
		config.set('Server', 'host', host)
		
	if port:
		config.set('Server', 'port', port)
	
	with open(CONF_FILE, 'w') as configfile:
		config.write(configfile)
	
	
	
	aaj = Arma2AutoJoin(
		config.get('Server', 'host'),
		config.getint('Server', 'port'),
		config.get('Settings', 'mod'),
		config.get('Folders', 'arma_path'),
		config.get('Folders', 'oa_path'),
		cpucount=config.get('Settings', 'cpucount'),
		exthreads=config.get('Settings', 'exThreads'),
		maxmem=config.get('Settings', 'maxmem'),
		)
	aaj.monitor()
	
if __name__ == "__main__":
	try:
		hostport = str(sys.argv[1])
		hostport = hostport.split(':')
		host = hostport[0]
		port = int(hostport[1])
	except:
		port = None
		try:
			host = str(sys.argv[1])
		except:
			host = None

	main(host=host, port=port)