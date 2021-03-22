from flask import Blueprint, jsonify
from flask_socketio import emit, join_room, leave_room
from flask import request
from . import socketio

apirouter = Blueprint("router", __name__)

@apirouter.route('/test',methods=['GET'])
def getTest():
  print("sono qui")
  return  jsonify({'msg':'ciao',})

