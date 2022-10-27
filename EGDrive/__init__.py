from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import GoogleDriveFile, ApiRequestError
import logging
from rich.logging import RichHandler
import os

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=False)]
)

logger = logging.getLogger("gdrive_logger")
logger.setLevel(logging.DEBUG)

class EGDrive:

	"""Main EGDrive class
	
	Attributes:
	    drive (GoogleDrive): pydrive2 GoogleDrive instance.
	    gauth (GoogleAuth): pydrive2 GoogleAuth instance.
	"""
	
	def __init__(self):
		"""Create an instance of EGDrive.
		"""
		self.gauth = GoogleAuth()
		self.gauth.LocalWebserverAuth()
		self.drive = GoogleDrive(self.gauth)
		logger.debug("authentication successful")

	def __mkdir(self, title : str, parents : list = []) -> GoogleDriveFile:
		"""Make a directory EGDrive instance.
		
		Args:
		    title (str): Directory title.
		    parents (list, optional): Directory parents.
		
		Returns:
		    GoogleDriveFile: Google Drive File instance of the created folder.
		"""
		if len(parents) == 0: parents = ['root']
		for parent in parents:
			logger.debug(f"checking if `{title}` exists in `{parent}`")
			if title in [file['title'] for file in self.ls(folder_id=parent)]:
				logger.debug(f"directory `{title}` already exists")
				directory = self.drive.CreateFile({'id': self.title_to_id(title, parent)})
				directory.FetchMetadata()
				return directory
				
		
		logger.debug(f"creating directory `{title}` with parents `{parents}`")
		metadata = {
			'title': title, 
			'parents': [{'id': parents[i]} for i in range(len(parents))], 
			'mimeType': 'application/vnd.google-apps.folder'
		}
		directory = self.drive.CreateFile(metadata)
		directory.Upload()
		
		return directory

	def get_user(self) -> dict:
		"""Returns information about the current authenticated user.
		
		Returns:
		    dict: Information about the current authenticated user.
		"""
		return self.drive.GetAbout()['user']

	def title_to_id(self, title : str, parent_id : str = 'root') -> str:
		"""Retrieves the `id` of the file or folder named `title` located in `parent_id`
		
		Args:
		    title (str): The title of the file or folder.
		    parent_id (str, optional): The id of the parent directory.
		
		Returns:
		    str: The GDrive ID of the file `title`
		
		Raises:
		    FileNotFoundError: If the file doesn't exits on GDrive
		"""
		foldered_list = self.drive.ListFile({'q':  f"'{parent_id}' in parents and trashed=false"}).GetList()
		
		for file in foldered_list:
			if(file['title'] == title):
				return file['id']
		
		raise FileNotFoundError

	def id_to_title(self, id : str) -> str:
		"""Retrieves the `title` of the file or folder with id `id` located in `parent_id`
		
		Args:
		    id (str): The title of the file or folder.

		Returns:
		    str: The title of the file with id `id`
		
		Raises:
		    FileNotFoundError: If the file doesn't exits on GDrive
		"""
		try:	
			file = self.drive.CreateFile({'id': id});
			file.FetchMetadata()
		except ApiRequestError:
			raise FileNotFoundError

		return file['title']

		
	def path_to_id(self, path : str) -> str:
		"""Retrieves the `id` of the absolute path `path`
		
		Args:
		    path (str): An absolute path in GDrive, in POSIX format (eg: /path/to/dest/)
		
		Returns:
		    str: The GDrive ID to access `path`
		"""
		if path == 'root': return 'root'
		path = path.replace('root/', '')
		
		directories = filter(lambda element: len(element) > 0, path.split("/"))
		id = 'root'
		
		for d in directories:
			id = self.title_to_id(d, id)
		
		return id

	def fetch_metadata(self, id : str) -> GoogleDriveFile: 
		"""Retrieves metadata of the file `id`
		
		Args:
		    id (str): the id of the file you want to get it's metadata
		
		Returns:
		    str: GoogleDrivFile instance of the file with id `id`
		"""

		gdfile = self.drive.CreateFile({'id': id})
		gdfile.FetchMetadata()
		return gdfile

	def id_to_path(self, id : str) -> str:
		"""Retrieves the absolute path of the file with `id`
		
		Args:
		    id (str): A valid GDrive file ID.
		
		Returns:
		    str: The absolute path of the file with `id`
		"""

		gdfile = self.fetch_metadata(id)
		parent = gdfile['parents'][0]
		path = [gdfile['title']]


		is_root = parent['isRoot']

		while not is_root:
			path = [self.id_to_title(parent['id'])] + path
			parent = self.fetch_metadata(parent['id'])['parents'][0]
			is_root = parent['isRoot']

		path = ['/root'] + path

		return '/'.join(path)


	def mkdir(self, path : str, parent_id : str = None) -> list:
		"""Create the `path` directory(ies), if they do not already exist.
		
		Args:
		    path (str): Path of directories (eg. /path/to/example/)
		    parent_id (str, optional): Parent directory which'll contain `path`
		
		Returns:
		    list: A list of created folders.
		"""
		directories = filter(lambda element: len(element) > 0, path.split("/"))
		
		parents = []
		if parent_id: parents = [parent_id]
		
		logger.info(f"creating path `{path}` with parents `{parents}`")
		
		gdrive_files = []
		
		for directory_title in directories:
			directory = self.__mkdir(directory_title, parents)
			parents = [directory['id']]
			
			gdrive_files.append(directory)
			
		return gdrive_files

	def ls(self, path : str = None, folder_id : str = None, maxdepth : int = 0) -> list:
		"""List directory contents (the current directory by default).
		
		Args:
		    path (str, optional): Path to list (ignored if folder_id is provided).
		    folder_id (str, optional): Folder's GDrive ID.
		    maxdepth (int, optional): Maximum depth to list (default=0).
		
		Returns:
		    list: A list of GoogleDriveFile instantces representing the directory contents. 
		"""
		assert folder_id != None or path != None
		
		if (0 > maxdepth): return []
		
		if folder_id == None:
			folder_id = self.path_to_id(path)
			
		if maxdepth == 0:
			return self.drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
		
		files = self.drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
		folders_to_scan = [file for file in files if file['mimeType'] == 'application/vnd.google-apps.folder']
		
		for folder in folders_to_scan:
			logger.info(f"list {folder['title']}")
			files += self.ls(folder_id=folder['id'], maxdepth=maxdepth-1)
		
		return files
			
	def rm(self, path, permanently=False) -> None:
		"""Remove files or directories
		
		Args:
		    path (TYPE): File or directory to move to Trash.
		    permanently (bool, optional): Permanently delete, disabled by default.
		"""
		id = self.path_to_id(path)
		if id:
			file = self.drive.CreateFile({'id': id})
			if permanently:
				file.Delete()
			else:
				file.Trash()

	def cp(self, src_path: str, dst_path: str) -> GoogleDriveFile:
		"""Copies file from `src_path` to `dst_path`, can't copy folders yet.
		
		Args:
		    path (str, optional): Path to list (ignored if folder_id is provided).
		    folder_id (str, optional): Folder's GDrive ID.
		    maxdepth (int, optional): Maximum depth to list (default=0).
		
		Returns:
		    list: A list of GoogleDriveFile instantces representing the directory contents. 
		"""
		
		src_gdfile = self.fetch_metadata(self.path_to_id(src_path))
		dirname = os.path.dirname(dst_path)
		basename = os.path.basename(dst_path)

		if self.exists(dst_path):
			target_folder = self.fetch_metadata(self.path_to_id(dst_path))
			return src_gdfile.Copy(target_folder)

		elif self.exists(dirname):
			target_folder = self.fetch_metadata(self.path_to_id(dirname))
			return src_gdfile.Copy(target_folder, basename)

		else:
			raise FileNotFoundError

	def exists(self, path : str) -> bool:
		"""Test whether a path exists.
		
		Args:
		    path (str): Path to test if it exits.
		
		Returns:
		    bool: True if `path` exists, False otherwise.
		"""
		try:
			id = self.path_to_id(path)
			return True
		except FileNotFoundError:
			return False
		
	def touch(self, file_path : str) -> GoogleDriveFile:
		"""Create an empty file.
		
		Args:
		    file_path (str): File to create.
		
		Returns:
		    GoogleDriveFile: Google Drive File instance of the created file.
		"""
		file_name = os.path.basename(file_path)
		dir_name = os.path.dirname(file_path)
		
		try:
			if self.exists(file_path):
				return self.drive.CreateFile({'id': self.path_to_id(file_path)})

			dir_id = self.path_to_id(dir_name)
			file = self.drive.CreateFile({'title': file_name, 'parents': [{'id': dir_id}]})
			file.Upload()
			return file

		except FileNotFoundError:
			logger.error(f"remote path `{dir_name}` doesn't exist")
			return None
			
	def upload(self, local_path : str, remote_path : str) -> GoogleDriveFile:
		"""Upload a file to GDrive.
		
		Args:
		    local_path (str): The local file path.
		    remote_path (str): The remote file path.
		
		Returns:
		    GoogleDriveFile: Google Drive File instance of the uploaded file.
		
		Raises:
		    FileNotFoundError: Raised if the local file doesn't exist or if the remote file path is invalid.
		"""
		if not os.path.exists(local_path):
			logger.error(f"local path `{local_path}` doesn't exist")
			raise FileNotFoundError
			
		file_object = self.touch(remote_path)
		if not file_object: raise FileNotFoundError
		file_object.SetContentFile(local_path)
		file_object.Upload()
		
		return file_object

	def download(self, remote_path : str, local_path : str) -> GoogleDriveFile:
		"""Download a file from GDrive
		
		Args:
		    remote_path (str): Remote file path.
		    local_path (str): Path where to download the desired file.
		
		Returns:
		    GoogleDriveFile: Google Drive File instance of the downloaded file.
		"""
		try:
			file_id = self.path_to_id(remote_path)
			file = self.drive.CreateFile({'id': file_id})
			file.GetContentFile(local_path)
			return file
			
		except FileNotFoundError:
			logger.error(f"remote path `{remote_path}` doesn't exist")

		return None