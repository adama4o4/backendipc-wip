"""
Wrapper for file class, to be implemented 
"""

class Reader:

	def __init__(self, filename):
		self.__fil = open(filename, "r")

	def read(self, r):
		return self.__fil.read(r)
	def reset(self):
		return self.__fil.seek(0, 0)

"""
Scanns machine (localhost/127.0.0.1) for open pipes, to be impemented
"""		
class Scanner:
	def __init__(self):
		raise NotImplementedError
