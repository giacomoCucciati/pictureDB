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


@apirouter.route('/getTagList',methods=['GET'])
def getTagList():
  print("Begin getTagList")
  tagList = mongo_interface.getTagList()
  print(tagList)
  print("End getTagList")
  return jsonify({'msg':'ciao','tagList':tagList})

@apirouter.route('/savePicture',methods=['POST'])
def savePicture():
  global mongo_interface
  print("Begin savePicture")
  params = request.get_json(force=True)
  if params['selectedPicture']['method'] == 'by-folder':
    print(params['selectedPicture']['dir'], params['selectedPicture']['filename'], params['selectedTags'])
    mongo_interface.savePicture(params['selectedPicture']['dir'], params['selectedPicture']['filename'], params['selectedTags'])
  if params['selectedPicture']['method'] == 'by-tag':
    print(params['selectedPicture']['pictureId'], params['selectedTags'])
    mongo_interface.updatePictureTags(params['selectedPicture']['pictureId'], params['selectedTags'])
  print("End savePicture")
  return jsonify({'msg':'ciao'})

@apirouter.route('/removePicture',methods=['POST'])
def removePicture():
  global mongo_interface
  print("Begin removePicture")
  params = request.get_json(force=True)
  print(params['selectedPicture'])
  mongo_interface.removePicture(params['selectedPicture'])
  print("End removePicture")
  return jsonify({'msg':'ciao'})

@apirouter.route('/insertNewTag',methods=['POST'])
def insertNewTag():
  global mongo_interface
  print("Begin insertNewTag")
  params = request.get_json(force=True)
  mongo_interface.insertNewTag(params['newTagName'])
  print("End insertNewTag")
  return jsonify({'msg':'ciao'})

@apirouter.route('/removeTag',methods=['POST'])
def removeTag():
  global mongo_interface
  print("Begin removeTag")
  params = request.get_json(force=True)
  mongo_interface.removeTag(params['tagName'])
  print("End removeTag")
  return jsonify({'msg':'ciao'})

@apirouter.route('/getPictureTags',methods=['POST'])
def getPictureTags():
  global mongo_interface
  print("Begin getPictureTags")
  params = request.get_json(force=True)
  pictureTags = []
  print(params['selectedPicture'])
  if params['selectedPicture']['method'] == 'by-folder':
    pictureTags = mongo_interface.getPictureTagsByFolder(params['selectedPicture']['dir'], params['selectedPicture']['filename'])
  if params['selectedPicture']['method'] == 'by-tag':
    picture = mongo_interface.getPictureById(params['selectedPicture']['pictureId'])
    pictureTags = picture['tags']
  print("End getPictureTags")
  return jsonify({'msg':'ciao', 'pictureTags':pictureTags})

@apirouter.route('/insertNewFolder',methods=['POST'])
def insertNewFolder():
  global mongo_interface
  print("Begin insertNewFolder")
  params = request.get_json(force=True)
  mongo_interface.insertNewFolder(params['newFolder'])
  print("End insertNewFolder")
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
  
  if params['selectedPicture']['method'] == 'by-folder':
    image = mongo_interface.buildPicture(params['selectedPicture']['dir'], params['selectedPicture']['filename'])
    return jsonify({'msg':'ciao', 'picture': image})
  if params['selectedPicture']['method'] == 'by-tag':
    picture = mongo_interface.getPictureById(params['selectedPicture']['pictureId'])
    print(picture)
    image = mongo_interface.buildPicture(picture['folder'], picture['picture'])
    return jsonify({'msg':'ciao', 'picture': image})
  else:
    return jsonify({'msg':'ciao'})
    
@apirouter.route('/getPicturesByTag',methods=['POST'])
def getPicturesByTag():
  global mongo_interface
  params = request.get_json(force=True)
  pictureList = mongo_interface.getPictureByTag(params['searchTagList'])
  print(pictureList)
  picture = mongo_interface.getPictureById(pictureList[0])
  print(picture)
  image = mongo_interface.buildPicture(picture['folder'], picture['picture'])
  return jsonify({'msg':'ciao', 'picture': image, 'dir':picture['folder'], 'filename': picture['picture'], 'pictureList': pictureList})

@apirouter.route('/getPictureList',methods=['POST'])
def getPictureList():
  global mongo_interface
  params = request.get_json(force=True)
  method = params['chriterion']
  if method == 'by-folder':
    imageExtensionAccepted = ['jpeg']
    params = request.get_json(force=True)
    print(params['selectedFolder'])
    filesInFolder = []
    imagesInFolder = []
    
    for (dirpath, dirnames, filenames) in walk(params['selectedFolder']):
      #filesInFolder.extend([join(dirpath,f) for f in filenames])
      for filename in filenames:
        filesInFolder.append({'dir':dirpath, 'filename': filename, 'method': method})
      break # we stop the list at the first level of the directory (we don't look in subfolders)
    
    for myfile in filesInFolder:
      if imghdr.what(join(myfile['dir'],myfile['filename'])) in imageExtensionAccepted:
        imagesInFolder.append(myfile)
    
    return jsonify({'msg':'ciao', 'pictureList': imagesInFolder})
  
  if method == 'by-tag':
    pictureList = mongo_interface.getPictureByTag(params['searchTagList'])
    newPictureList = []
    for pic in pictureList:
      newPictureList.append({'pictureId': pic, 'method':method})
    
    return jsonify({'msg':'ciao', 'pictureList': newPictureList})
  
  return jsonify({'msg':'ciao'})

@apirouter.route('/deleteDb',methods=['GET'])
def deleteDb():
  global mongo_interface
  mongo_interface.deleteDb()
  return jsonify({'msg':'ciao'})