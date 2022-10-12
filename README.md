
# 📦️ EGDrive

A simplified Google Drive API wrapper for Python.

EGDrive is a built on top of PyDrive2, it simplifies managment of Google Drive using Python, it has a high level interface emulating Linux file management commands in an intuitive way.
## Installation

Install EGDrive with pip

```bash
    pip install EGDrive
```
    
## 📌 Features

- Intuitive Unix-like commands (ls, mkdir, rm ...) to manage Google Drive
- Uses Unix path's format, no more Google Drive ID's headaches.
- Built on top of PyDrive2, access GoogleDrive and GoogleAuth instances for more options.
- Lightweight.


## 🚀 Usage/Examples

### Authentication with Google Drive

Create a new project in Google's APIs Console, for that follow this guide in [here](https://docs.iterative.ai/PyDrive2/quickstart/#authentication).
To make the authentication automatic follow [this guide](https://docs.iterative.ai/PyDrive2/oauth/#automatic-and-custom-authentication-with-settings-yaml).

### Usage Examples
 Initiate an EGDrive instance.

```python
from EGDrive import EGDrive

gdrive = EGDrive()
```

List files
```python
files = [file['title'] for file in gdrive.ls('root')]
for file in files:
    print(file)
```

Create a directory
```python
gdrive.mkdir("/Books")
```

Create even more directories
```python
gdrive.mkdir("/Books/Science")
gdrive.mkdir("/Books/Litterature")
gdrive.mkdir("/Books/Science/Programming/JAVA")
gdrive.mkdir("/Books/Science/Programming/Python/3/")
```
Remove files and directories
```python
# move to Trash
gdrive.rm("/Books/Science/Programming/JAVA")
# delete permanently
gdrive.rm("/Books/Litterature", permanently=True)
```
Download a file
```python
gdrive.download("/Books/Science/physics.pdf", "/home/user/Downloads/physics.pdf")
```
Upload a file
```python
gdrive.upload("/home/user/Videos/mrbean.mp4", "/Videos/mrbean.mp4")
```
Check if a file exists
```python
gdrive.exists("/path/to/file")
```
Create an empty file
```python
gdrive.touch("/Documents/empty.txt")
```
Get access to PyDrive2 GoogleDrive and GoogleAuth instances
```python
gdrive.drive # GoogleDrive instance
gdrive.gauth # GoogleAuth instance
```
## 🔧 Contributing

Contributions are always welcome!
