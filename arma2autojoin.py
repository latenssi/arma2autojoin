import subprocess
import os 
import sys 
import time
import configparser
import re
from random import randint
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
		self.server_mon = Server(self.host, self.port)
		
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
		
		if self.cpucount:
			params.append(r"-cpuCount=%s" % self.cpucount)
		
		if self.exthreads:
			params.append(r"-exThreads=%s" % self.exthreads)
			
		if self.maxmem:
			params.append(r"-maxmem=%s" % self.maxmem)
			
		network = [r"-connect=%s" % self.host, r"-port=%d" % self.port]
		
		startup = []
		startup.append(exe_str)
		startup.append(mod_str)
		startup.append(mod2_str)
		startup.extend(params)
		startup.extend(network)
		
		subprocess.call(startup)
	
	def monitor(self, auto_connect=False):
		self.server_mon.connect()
		
		# Get initial info so we can print the hostname
		self._query()
		print("%s\n" % self.server_mon.info['hostname'])
		
		old_cur_players = 0
		
		while True:
			max_players = int(self.server_mon.info['maxplayers'])
			cur_players = int(self.server_mon.info['numplayers'])
			
			if old_cur_players != cur_players:
				old_cur_players = cur_players
				print("Players: %d/%d" % (cur_players, max_players), end='\r')
				
			if auto_connect and cur_players < max_players:
				break
				
			time.sleep(randint(1, 1))
			self._query()
			
		self.server_mon.close()
		
		if auto_connect:
			self.connect()
		
		
	def _query(self):

		while True:
			try:
				self.server_mon.query()
			except:
				print("Server not respoding. Retrying in 5 seconds..")
				time.sleep(5)
			else:
				break

		
def main(host=None, port=None):
	config = configparser.RawConfigParser()
	config.read(CONF_FILE)
	try:
		if host:
			config.set('Server', 'host', host)
			
		if port:
			config.set('Server', 'port', port)
		
		with open(CONF_FILE, 'w') as configfile:
			config.write(configfile)
	
	except configparser.NoSectionError:
		print ("No configuration file. Please copy the 'arma2autojoin.cfg.sample' and remove the '.sample'.")
		sys.exit(2)
	
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
		
	aaj.monitor(auto_connect=True)
	
if __name__ == "__main__":
	try:
		kwargs = re.match( r'(?P<host>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})(:(?P<port>\d+))?', sys.argv[1] ).groupdict()
	except (IndexError, AttributeError):
		kwargs = {'host': None, 'port': None}
	main(**kwargs)