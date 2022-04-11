from flask import Blueprint, jsonify
from flask import request
from .mongoInterface import MongoInterface
import src.appUtils as appUtils


apirouter = Blueprint("router", __name__)
mongo_interface = MongoInterface()
tag_groups = ['Persone','Luoghi','Anno','Varie']

###################################################
#                   Tag Section                   #
###################################################

@apirouter.route('/getTagList',methods=['GET'])
def getTagList():
  print("Begin getTagList")
  tagList = mongo_interface.getTagList()
  print("End getTagList")
  return jsonify({'msg':'ciao', 'tagGroups':tag_groups, 'tagList':tagList})

@apirouter.route('/changeTag',methods=['POST'])
def changeTag():
  print("Begin changeTag")
  params = request.get_json(force=True)
  print(params)
  if params['action'] == "deleteTag":
    mongo_interface.removeTag(params['tagId'])
  if params['action'] == "editTag":
    mongo_interface.editTag(params['tagId'],params['newName'])
  if params['action'] == "createTag":
    mongo_interface.createTag(params['parentTagId'])
  print("End changeTag")
  return jsonify({'msg':'ciao'})

###################################################
#                 Folder Section                  #
###################################################

@apirouter.route('/getFolderList',methods=['GET'])
def getFolderList():
  print("Begin getFolderList")
  folderList = mongo_interface.getFolderList()
  print("End getFolderList")
  return jsonify({'msg':'ciao', 'folderList':folderList})

###################################################
#                Picture Section                  #
###################################################

@apirouter.route('/getPictureList',methods=['POST'])
def getPictureList():
  params = request.get_json(force=True)
  pictureList = mongo_interface.getPictureByTag(params['searchTagList'])
  return jsonify({'msg':'ciao', 'pictureList': pictureList})

@apirouter.route('/getPicture',methods=['POST'])
def getPicture():
  imageExtensionAccepted = ['jpeg']
  print("Begin getPicture")
  params = request.get_json(force=True)
  picture = mongo_interface.getPictureById(params['selectedPictureId'])
  print(picture)
  image = mongo_interface.buildPicture(picture['folder'], picture['filename'])
  return jsonify({'msg':'ciao', 'picture': image})

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

@apirouter.route('/savePicture',methods=['POST'])
def savePicture():
  print("Begin savePicture")
  params = request.get_json(force=True)
  print(params['selectedPictureId'], params['selectedTags'])
  mongo_interface.updatePictureTags(params['selectedPictureId'], params['selectedTags'])
  print("End savePicture")
  return jsonify({'msg':'ciao'})

# @apirouter.route('/removePicture',methods=['POST'])
# def removePicture():
#   print("Begin removePicture")
#   params = request.get_json(force=True)
#   print(params['selectedPictureId'])
#   mongo_interface.removePicture(params['selectedPictureId'])
#   print("End removePicture")
#   return jsonify({'msg':'ciao'})

# @apirouter.route('/changeTagList',methods=['POST'])
# def changeTagList():
#   print("Begin changeTagList")
#   params = request.get_json(force=True)
#   if params['action'] == 'add-tag':
#     mongo_interface.insertNewTag(params['tagName'], params['tagGroup'])
#   if params['action'] == 'remove-tag':
#     mongo_interface.removeTag(params['tagName'], params['tagGroup'])
#   print("End changeTagList")
#   return jsonify({'msg':'ciao'})


@apirouter.route('/saveMainPath',methods=['POST'])
def saveMainPath():
  params = request.get_json(force=True)
  print(params['mainPath'])
  mongo_interface.insertMainPath(params['mainPath'])
  return {'msg':'salvato'}

@apirouter.route('/getMainPath',methods=['GET'])
def getMainPath():
  mainFolder = mongo_interface.getMainPath()
  return {'mainFolder':mainFolder}

@apirouter.route('/editFolder',methods=['POST'])
def importFolder():
  print("Begin importFolder")
  params = request.get_json(force=True)
  print(params)

  if params['directive'] == 'new-folder':
    mongo_interface.insertNewFolder(params['newFolder'])
    mainFolder = mongo_interface.getMainPath()
    imagesInFolder = appUtils.getPicturesByFolder(mainFolder, params['newFolder'])
    for image in imagesInFolder:
      mongo_interface.savePicture(image['dir'], image['filename'], [])

  if params['directive'] == 'clear-tags':
    for image in imagesInFolder:
      mongo_interface.savePicture(image['dir'], image['filename'], [])
  
  if params['directive'] == 'add-pictures':
    for image in imagesInFolder:
      mongo_interface.savePicture(image['dir'], image['filename'], [], overwrite=False)

  if params['directive'] == 'delete-folder':
    mongo_interface.deleteFolder(params['newFolder'], deletePictures=True)

  print("End importFolder")
  return jsonify({'msg':'ciao'})

@apirouter.route('/checkFolderExistence',methods=['POST'])
def checkFolderExistence():
  print("Begin checkFolderExistence")
  options = {'msg':'', 'error':''}
  params = request.get_json(force=True)
  theList = params['folderList']
  mainPath = mongo_interface.getMainPath()
  
  if mainPath == None:
    options['error'] = 'Main path is not set'
  else:
    problemList = []
    for innerFolder in theList:
      if not appUtils.checkFolderExistence(mainPath,innerFolder):
        problemList.append(innerFolder)
    if len(problemList) > 0:
      options['error'] = 'Found some bad paths: ' + ','.join(problemList)
    else:
      options['msg'] = 'ok'
  return jsonify(options)

  
@apirouter.route('/deleteDb',methods=['GET'])
def deleteDb():
  mongo_interface.deleteDb()
  return jsonify({'msg':'ciao'})