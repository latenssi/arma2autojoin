import subprocess
import os 

def main():
	arma_path = r"C:\Program Files (x86)\Steam\steamapps\common\Arma 2"
	oa_path = r"C:\Program Files (x86)\Steam\steamapps\common\arma 2 operation arrowhead"
	
	os.chdir(oa_path)
	
	executable = r"expansion\beta\arma2oa.exe"
	mod = r"-mod=%s;EXPANSION;ca" % arma_path
	mod2 = r"-mod=Expansion\beta;Expansion\beta\Expansion;@dayz_epoch"
	params = [r"-high", r"-cpuCount=4", r"-exThreads=7", r"-maxmem=2047", r"-noPause", r"-nosplash", r"-skipintro", r"-world=empty"]
	network = [r"-connect=193.111.140.42", r"-port=2302"]
	
	startup = []
	startup.append(executable)
	startup.append(mod)
	startup.append(mod2)
	startup.extend(params)
	startup.extend(network)
	
	print "Starting DayZ Epoch.."
	
	subprocess.call(startup)

if __name__ == "__main__":
    main()