"""
Wrapper for file class
"""

class Reader:

	def __init__(self, name="text.dat"):
		try:
			self.__fil = open(name, "r+")
		except:
			self.__fil = open(name, "w+")
			self.__fil.close()
			self.__fil = open(name, "r+")
	def read(self, r):
		return self.__fil.read(r)
	def write(self, dat):
		self.__fil.write(dat)
	def reset(self):
		return self.__fil.seek(0, 0)
"""
Scanns machine (localhost/127.0.0.1) for open pipes, to be impemented
"""		
class Scanner:
	def __init__(self):
		raise NotImplementedError
