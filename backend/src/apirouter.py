from flask import Blueprint, jsonify
from flask_socketio import emit, join_room, leave_room
from flask import request
from . import socketio
from .mongoInterface import MongoInterface

apirouter = Blueprint("router", __name__)
mongo_interface = MongoInterface()

@apirouter.route('/getTagList',methods=['GET'])
def getTagList():
  print("Begin getTagList")
  tagList = mongo_interface.getTagList()
  print(tagList)
  print("End getTagList")
  return  jsonify({'msg':'ciao','tagList':tagList})

@apirouter.route('/savePicture',methods=['POST'])
def savePicture():
  global mongo_interface
  print("Begin savePicture")
  params = request.get_json(force=True)
  mongo_interface.savePicture(params['pictureName'], params['selectedTags'])
  print("End savePicture")
  return  jsonify({'msg':'ciao'})

@apirouter.route('/insertNewTag',methods=['POST'])
def insertNewTag():
  global mongo_interface
  print("Begin insertNewTag")
  params = request.get_json(force=True)
  mongo_interface.insertNewTag(params['newTagName'])
  print("End insertNewTag")
  return  jsonify({'msg':'ciao'})

@apirouter.route('/getPictureTags',methods=['POST'])
def getPictureTags():
  global mongo_interface
  print("Begin getPictureTags")
  params = request.get_json(force=True)
  pictureTags = mongo_interface.getPictureTags(params['pictureName'])
  print("End getPictureTags")
  return  jsonify({'msg':'ciao', 'pictureTags':pictureTags})
