# 📦️ EGDrive

[![Issues](https://img.shields.io/github/issues/th3c00lw0lf/EGDrive)](https://github.com/th3c00lw0lf/EGDrive/issues)  [![pypi](https://img.shields.io/pypi/v/EGDrive)](https://pypi.org/project/EGDrive/)

A simplified Google Drive API wrapper for Python.

EGDrive is a built on top of [PyDrive2](https://github.com/iterative/PyDrive2), it simplifies management of Google Drive using Python, it has a high level interface emulating Linux file management commands in an intuitive way.
## 🧑‍💻 Installation

Install EGDrive with pip

```bash
pip install EGDrive
```
    
## 📌 Features

- Intuitive Unix-like commands (ls, mkdir, rm ...) to manage Google Drive
- Access any file with it's absolute path, no more Google Drive ID's headaches.
- Built on top of [PyDrive2](https://github.com/iterative/PyDrive2), access [GoogleDrive](https://docs.iterative.ai/PyDrive2/pydrive2/#pydrive2.drive.GoogleDrive) and [GoogleAuth](https://docs.iterative.ai/PyDrive2/pydrive2/#pydrive2.drive.GoogleDrive) instances for more options.
- Lightweight.


## 🚀 Usage/Examples

### Authentication with Google Drive

Create a new project in Google's APIs Console, for that follow this guide in [here](https://docs.iterative.ai/PyDrive2/quickstart/#authentication).
To make the authentication automatic follow [this guide](https://docs.iterative.ai/PyDrive2/oauth/#automatic-and-custom-authentication-with-settings-yaml).

##### Initiate an EGDrive instance.
```python
from EGDrive import EGDrive

gdrive = EGDrive()
```

##### List files
The files that will be listed are the ones that your *Google Project has access to*, other files *won't* be managed by EGDrive.

```python
files = [file['title'] for file in gdrive.ls('root')]
for file in files:
    print(file)
```

##### Create a directory
If you try to create a directory that *already exists*, this function *won't create a new directory* with the same name and different id, instead it'll return the [`GoogleDriveFile`](https://docs.iterative.ai/PyDrive2/pydrive2/#pydrive2.files.GoogleDriveFile) instance for *the existing directory* in the drive, and if there are more than one, it'll return [`GoogleDriveFile`](https://docs.iterative.ai/PyDrive2/pydrive2/#pydrive2.files.GoogleDriveFile) for the first one that matches the name of the new directory.

```python
gdrive.mkdir("/Books")
```

##### Create even more directories
You can create as many directories as you want using mkdir , this works the same as the command `mkdir -p` in Linux.
*Please note that you should always use absolute paths!*
```python
gdrive.mkdir("/Books/Science") # equivalent to `mkdir -p Books/Science`
gdrive.mkdir("/Books/Litterature")
gdrive.mkdir("/Books/Science/Programming/JAVA")
gdrive.mkdir("/Books/Science/Programming/Python/3/")
```

##### Create an empty file
Creates a new file and returns it's [`GoogleDriveFile`](https://docs.iterative.ai/PyDrive2/pydrive2/#pydrive2.files.GoogleDriveFile) instance. if the file already exists it'll return the [`GoogleDriveFile`](https://docs.iterative.ai/PyDrive2/pydrive2/#pydrive2.files.GoogleDriveFile) instance of the existing file.
```python
gdrive.touch("/Documents/empty.txt")
```

##### Check if a file exists
```python
if gdrive.exists("/path/to/file"): print("File exists!")
else: print("File not found!")
```

##### Remove files and directories
Removing files by default moves them to Trash where they'll be permanently deleted after 30 days.

```python
# move to Trash
gdrive.rm("/Books/Science/Programming/JAVA")
# delete permanently
gdrive.rm("/Books/Litterature", permanently=True)
```

##### Download a file
```python
gdrive.download("/Books/Science/physics.pdf", "/home/user/Downloads/physics.pdf")
```

##### Upload a file
```python
gdrive.upload("/home/user/Videos/mrbean.mp4", "/Videos/mrbean.mp4")
```

##### Get access to PyDrive2 [`GoogleDrive`](https://docs.iterative.ai/PyDrive2/pydrive2/#pydrive2.drive.GoogleDrive) and [`GoogleAuth`](https://docs.iterative.ai/PyDrive2/pydrive2/#pydrive2.Auth.GoogleAuth) instances
```python
gdrive.drive # GoogleDrive instance
gdrive.gauth # GoogleAuth instance
```
## 📝 TODO

- Add progress info for uploading/downloading files.
- Add support for file operations: copy, move.
- Implement support for relative paths.
- ...

## 🩹 Known Issues

You tell me 👽️.


## 🔧 Contributing

Contributions are always welcome!
