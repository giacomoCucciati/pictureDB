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
  print("Begin savePicture")
  params = request.get_json(force=True)
  print(params['selectedPictureId'], params['selectedTags'])
  mongo_interface.updatePictureTags(params['selectedPictureId'], params['selectedTags'])
  print("End savePicture")
  return jsonify({'msg':'ciao'})

@apirouter.route('/removePicture',methods=['POST'])
def removePicture():
  print("Begin removePicture")
  params = request.get_json(force=True)
  print(params['selectedPictureId'])
  mongo_interface.removePicture(params['selectedPictureId'])
  print("End removePicture")
  return jsonify({'msg':'ciao'})

@apirouter.route('/changeTagList',methods=['POST'])
def changeTagList():
  print("Begin changeTagList")
  params = request.get_json(force=True)
  if params['action'] == 'add-tag':
    mongo_interface.insertNewTag(params['tagName'], params['tagGroup'])
  if params['action'] == 'remove-tag':
    mongo_interface.removeTag(params['tagName'], params['tagGroup'])
  print("End changeTagList")
  return jsonify({'msg':'ciao'})

@apirouter.route('/getPictureTags',methods=['POST'])
def getPictureTags():
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
  print("Begin importFolder")
  params = request.get_json(force=True)
  print(params['directive'])
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
    if params['directive'] == 'new-folder':
      mongo_interface.savePicture(image['dir'], image['filename'], [])
    if params['directive'] == 'clear-tags':
      mongo_interface.savePicture(image['dir'], image['filename'], [])
    if params['directive'] == 'keep-tags':
      mongo_interface.savePicture(image['dir'], image['filename'], [], overwrite=False)

  print("End importFolder")
  return jsonify({'msg':'ciao'})

@apirouter.route('/getFolderList',methods=['GET'])
def getFolderList():
  print("Begin getFolderList")
  folderList = mongo_interface.getFolderList()
  print("End getFolderList")
  return jsonify({'msg':'ciao', 'folderList':folderList})

@apirouter.route('/getPicture',methods=['POST'])
def getPicture():
  imageExtensionAccepted = ['jpeg']
  print("Begin getPicture")
  params = request.get_json(force=True)
  picture = mongo_interface.getPictureById(params['selectedPictureId'])
  print(picture)
  image = mongo_interface.buildPicture(picture['folder'], picture['filename'])
  return jsonify({'msg':'ciao', 'picture': image})

@apirouter.route('/getPictureList',methods=['POST'])
def getPictureList():
  params = request.get_json(force=True)
  pictureList = mongo_interface.getPictureByTag(params['searchTagList'])
  return jsonify({'msg':'ciao', 'pictureList': pictureList})
  
@apirouter.route('/deleteDb',methods=['GET'])
def deleteDb():
  mongo_interface.deleteDb()
  return jsonify({'msg':'ciao'})