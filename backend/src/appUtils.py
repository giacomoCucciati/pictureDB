from os import walk
from os.path import join
from os.path import isdir
import imghdr

def getPicturesByFolder(mainPath, folder):

  imageExtensionAccepted = ['jpeg']
  filesInFolder = []
  imagesInFolder = []

  fullFolder = join(mainPath,folder)
  for (dirpath, dirnames, filenames) in walk(fullFolder):
    #filesInFolder.extend([join(dirpath,f) for f in filenames])
    for filename in filenames:
      filesInFolder.append({'dir':dirpath, 'filename': filename})
    break # we stop the list at the first level of the directory (we don't look in subfolders)
  
  for myfile in filesInFolder:
    if imghdr.what(join(myfile['dir'],myfile['filename'])) in imageExtensionAccepted:
      imagesInFolder.append(myfile)

  return imagesInFolder

def checkFolderExistence(mainPath,innerFolder):
  fullFolder = join(mainPath,innerFolder)
  return isdir(fullFolder)
