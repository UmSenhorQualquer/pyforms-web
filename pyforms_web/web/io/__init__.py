from pysettings import conf
from crequest.middleware import CrequestMiddleware

class open(object):
	def __init__(self, fpath, mode):
		self.f 	  = fpath
		self.mode = mode

		request 	 = CrequestMiddleware.get_request()
		user 		 = request.user
		self.storage = conf.MAESTRO_STORAGE_MANAGER.get(user)

		if   mode in ['w','wb']:
			self.bytesbuffer = BytesIO()
		elif mode in ['r', 'rb']:
			self.file = self.storage.get_file_handler(fpath)


	def __exit__(self, exc_type, exc_val, exc_tb): 
		if   mode in ['w','wb']:
			self.storage.put_file_contents(self.f, self.bytesbuffer)
		elif mode in ['r', 'rb']:
			self.file.close()


	def __enter__(self): 			return self.file
	def __str__(self): 				return self.f
	def __del__(self): 				self.file.close()
	def __iter__(self): 			return self
	def __next__(self): 			return self.next()
	def next(self): 
		res = self.file.readline()
		if len(res)==0: raise StopIteration
		return res
	def read(self, size=-1): 		return self.file.read(size)
	def readall(self): 				return self.file.readall()
	def write(self, b): 			return self.file.write(b)
	def readline(self, size=-1): 	return self.file.readline(size)
	def readlines(self, hint=-1): 	return self.file.readlines(hint)
	def close(self): 				self.file.close()