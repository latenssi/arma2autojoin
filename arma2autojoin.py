import subprocess
import os 
import socket
import struct
from Server import Server

def main():
	#host = r"193.111.140.42"
	host = r"144.76.99.229"
	port = 2302
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
	
	#subprocess.call(startup)
	
	s = Server(host, port)
	s.query()
	max_players = int(s.info['maxplayers'])
	cur_players = int(s.info['numplayers'])
	print("%d/%d" % (cur_players, max_players))
	
if __name__ == "__main__":
    main()