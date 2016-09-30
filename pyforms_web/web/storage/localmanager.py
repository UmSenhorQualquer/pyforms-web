import os, shutil, subprocess
from django.utils 					import timezone
from pyforms_web.web.storage.remotefile import RemoteFile

from pysettings import conf

def get_thumb(fileinfo, size=32):
	if fileinfo.type=='dir': return "/static/icons/folder{0}.png".format(size)

	file_extension = os.path.splitext( fileinfo.fullpath )[1]

	if 	file_extension=='.avi' or \
		file_extension=='.mpg' or \
		file_extension=='.mp4': return '/static/icons/movie%d.png' % size

	if 	file_extension=='.png' or \
		file_extension=='.jpg' or \
		file_extension=='.jpeg':
		return '/static/icons/image%d.png' % size
	
	return '/static/icons/file%d.png' % size




class LocalStorageManager(object):

	def __init__(self, user): self._user = user

	def __parseFile(self, f):
		fileobj = RemoteFile()
		fileobj.filename 		= os.path.basename(f)
		fileobj.fullpath 		= f.replace(self.user_path,'').replace('\\','/')
		fileobj.size 			= os.path.getsize(f)
		fileobj.lastmodified 	= os.stat(f).st_mtime 
		fileobj.type 			= 'dir' if os.path.isdir(f) else 'file'
		fileobj.small_thumb 	= get_thumb(fileobj, 32)
		fileobj.big_thumb 		= get_thumb(fileobj, 180)
		fileobj.download_link 	= 'javascript:openFolder("{0}")'.format(fileobj.fullpath) if fileobj.type=='dir' else ""
		fileobj.open_link 		= 'javascript:openFolder("{0}")'.format(fileobj.fullpath) if fileobj.type=='dir' else ""
		return fileobj

	@property
	def user_path(self):
		userpath = conf.PYFORMS_USERS_AREA_PATH
		if not os.path.isdir(userpath): os.mkdir(userpath)
		return userpath

	def __user_path(self, path):
		return os.path.join(self.user_path, path[1:] if path[0]=='/' else path)
		
	def put_file_contents(self, remote_path, data):
		infile = open(self.__user_path(remote_path), 'wb')
		buff = data.read()
		while len(buff)>0:
			infile.write(buff)
			buff = data.read()
		infile.close()
		return True

	def put_file(self, remote_path, local_source_file, **kwargs):
		shutil.copy2(local_source_file, self.__user_path(remote_path) )
		return True

	def get_file_handler(self, path):
		infile = open(self.__user_path(path), 'rb')
		return infile

	def delete(self, path):
		if os.path.isfile( self.__user_path(path) ):
			os.remove( self.__user_path(path) )
		else:
			os.rmdir( self.__user_path(path) )
		return True

	def list(self, path):
		for f in os.listdir( self.__user_path(path) ):
			yield self.file_info( os.path.join(path, f) )

	def file_info(self, path):
		return self.__parseFile( self.__user_path(path) )
		

	def mkdir(self, path):
		os.mkdir( self.__user_path( path) )
		return True

	def public_link(self, path): return self.__user_path(path)

	def public_download_link(self, path): return self.__user_path(path)
		