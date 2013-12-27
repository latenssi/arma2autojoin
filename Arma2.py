class Arma2:
	arma_path = ""
	oa_path = ""
	def __init_(self):
		arma_path = r"C:\Program Files (x86)\Steam\steamapps\common\Arma 2"
		oa_path = r"C:\Program Files (x86)\Steam\steamapps\common\arma 2 operation arrowhead"
	
		os.chdir(oa_path)
	
		exe_str = r"expansion\beta\arma2oa.exe"
		mod_str = r"-mod=%s;EXPANSION;ca" % arma_path
		mod2_str = r"-mod=Expansion\beta;Expansion\beta\Expansion;%s" % mod
		params = [r"-high", r"-cpuCount=4", r"-exThreads=7", r"-maxmem=2047", r"-noPause", r"-nosplash", r"-skipintro", r"-world=empty"]
		network = [r"-connect=%s" % host, r"-port=%d" % port]