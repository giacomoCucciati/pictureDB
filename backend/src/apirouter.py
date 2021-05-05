from flask import Blueprint, jsonify
from flask_socketio import emit, join_room, leave_room
from flask import request
from flask import send_from_directory, send_file
from . import socketio
from .mongoInterface import MongoInterface
from os import walk
from os.path import join
import imghdr


apirouter = Blueprint("router", __name__)
mongo_interface = MongoInterface()
tag_groups = ['Persone','Luoghi','Anno','Varie']

@apirouter.route('/getTagList',methods=['GET'])
def getTagList():
  print("Begin getTagList")
  tagList = mongo_interface.getTagList()
  print("End getTagList")
  return jsonify({'msg':'ciao', 'tagGroups':tag_groups, 'tagList':tagList})

@apirouter.route('/savePicture',methods=['POST'])
def savePicture():
  global mongo_interface
  print("Begin savePicture")
  params = request.get_json(force=True)
  print(params['selectedPictureId'], params['selectedTags'])
  mongo_interface.updatePictureTags(params['selectedPictureId'], params['selectedTags'])
  print("End savePicture")
  return jsonify({'msg':'ciao'})

@apirouter.route('/removePicture',methods=['POST'])
def removePicture():
  global mongo_interface
  print("Begin removePicture")
  params = request.get_json(force=True)
  print(params['selectedPictureId'])
  mongo_interface.removePicture(params['selectedPictureId'])
  print("End removePicture")
  return jsonify({'msg':'ciao'})

@apirouter.route('/insertNewTag',methods=['POST'])
def insertNewTag():
  global mongo_interface
  print("Begin insertNewTag")
  params = request.get_json(force=True)
  mongo_interface.insertNewTag(params['tagName'], params['tagGroup'])
  print("End insertNewTag")
  return jsonify({'msg':'ciao'})

@apirouter.route('/removeTag',methods=['POST'])
def removeTag():
  global mongo_interface
  print("Begin removeTag")
  params = request.get_json(force=True)
  mongo_interface.removeTag(params['tagName'], params['tagGroup'])
  print("End removeTag")
  return jsonify({'msg':'ciao'})

@apirouter.route('/getPictureTags',methods=['POST'])
def getPictureTags():
  global mongo_interface
  print("Begin getPictureTags")
  params = request.get_json(force=True)
  pictureTags = []
  print(params['selectedPictureId'])
  
  picture = mongo_interface.getPictureById(params['selectedPictureId'])
  pictureTags = picture['tags']
  print("End getPictureTags")
  return jsonify({'msg':'ciao', 'pictureTags':pictureTags})

@apirouter.route('/importFolder',methods=['POST'])
def importFolder():
  global mongo_interface
  print("Begin importFolder")
  params = request.get_json(force=True)
  mongo_interface.insertNewFolder(params['newFolder'])
  # Now save all folder images in DB
  imageExtensionAccepted = ['jpeg']
  params = request.get_json(force=True)
  filesInFolder = []
  imagesInFolder = []
  
  for (dirpath, dirnames, filenames) in walk(params['newFolder']):
    #filesInFolder.extend([join(dirpath,f) for f in filenames])
    for filename in filenames:
      filesInFolder.append({'dir':dirpath, 'filename': filename})
    break # we stop the list at the first level of the directory (we don't look in subfolders)
  
  for myfile in filesInFolder:
    if imghdr.what(join(myfile['dir'],myfile['filename'])) in imageExtensionAccepted:
      imagesInFolder.append(myfile)

  for image in imagesInFolder:
    mongo_interface.savePicture(image['dir'], image['filename'], [])

  print("End importFolder")
  return jsonify({'msg':'ciao'})

@apirouter.route('/removeFolder',methods=['POST'])
def removeFolder():
  global mongo_interface
  print("Begin removeFolder")
  params = request.get_json(force=True)
  mongo_interface.removeFolder(params['badFolder'])
  print("End removeFolder")
  return jsonify({'msg':'ciao'})

@apirouter.route('/getFolderList',methods=['GET'])
def getFolderList():
  global mongo_interface
  print("Begin getFolderList")
  folderList = mongo_interface.getFolderList()
  print("End getFolderList")
  return jsonify({'msg':'ciao', 'folderList':folderList})

@apirouter.route('/getPicture',methods=['POST'])
def getPicture():
  global mongo_interface
  imageExtensionAccepted = ['jpeg']
  print("Begin getPicturesFromFolder")
  params = request.get_json(force=True)
  picture = mongo_interface.getPictureById(params['selectedPictureId'])
  print(picture)
  image = mongo_interface.buildPicture(picture['folder'], picture['filename'])
  return jsonify({'msg':'ciao', 'picture': image})

@apirouter.route('/getPictureList',methods=['POST'])
def getPictureList():
  global mongo_interface
  params = request.get_json(force=True)
  pictureList = mongo_interface.getPictureByTag(params['searchTagList'])
  return jsonify({'msg':'ciao', 'pictureList': pictureList})
  
@apirouter.route('/deleteDb',methods=['GET'])
def deleteDb():
  global mongo_interface
  mongo_interface.deleteDb()
  return jsonify({'msg':'ciao'})