import subprocess
import os

def main():
	arma_path = r"C:\Program Files (x86)\Steam\steamapps\common\Arma 2"
	arma_exe = r"arma2.exe"
	oa_path = r"C:\Program Files (x86)\Steam\steamapps\common\arma 2 operation arrowhead"
	oa_exe = r"ArmA2OA.exe"
	mod = r"@DayZ_Epoch"
	params = [r"-high", r"-cpuCount=4", r"-exThreads=7", r"-maxmem=2047", r"-noPause", r"-nosplash", r"-skipintro", r"-world=empty"]
	network = [r"-connect=193.111.140.42", r"-port=2302"]
	startup = [r"{0}".format(os.path.join(arma_path, arma_exe)), r"-mod={0}".format(os.path.join(oa_path, mod))]
	startup.extend(params)
	startup.extend(network)
	subprocess.call(startup)

if __name__ == "__main__":
    main()