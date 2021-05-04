from pymongo import MongoClient
import copy
import json
from PIL import Image
import io
import base64
from os.path import join
from bson.objectid import ObjectId

class MongoInterface:

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['picturedb']
        if not 'tags' in self.db.collection_names():
            self.db.create_collection('tags')
        self.tagsTable = self.db['tags']
        if not 'folders' in self.db.collection_names():
            self.db.create_collection('folders')
        self.foldersTable = self.db['folders']
        if not 'pictures' in self.db.collection_names():
            self.db.create_collection('pictures')
        self.picturesTable = self.db['pictures']

    def savePicture(self, folderName, pictureName, selectedTags):
      picture = self.picturesTable.find_one({'folder': folderName, 'picture': pictureName})
      if picture==None:
        newEntry = {'folder': folderName, 'picture': pictureName, 'tags':selectedTags}
        self.picturesTable.insert_one(newEntry)
      else:
        newtags = { "$set": { "tags": selectedTags} }
        self.picturesTable.update_one({'folder': folderName, 'picture': pictureName}, newtags)
    
    def removePicture(self, selectedPicture):
      if 'pictureId' in selectedPicture:
        self.picturesTable.delete_many({"_id":selectedPicture['pictureId']})
      else:
        self.picturesTable.delete_many({"folder":selectedPicture['dir'], "picture":selectedPicture['filename']})


    def updatePictureTags(self, picId, selectedTags):
      picture = self.picturesTable.find_one(ObjectId(picId))
      if picture==None:
        print('Error in updatePictureTags')
      newtags = { "$set": { "tags": selectedTags} }
      self.picturesTable.update_one({"_id":picId}, newtags)

    def getTagList(self):
      tagList = []
      for tag in self.tagsTable.find():
        tagList.append({'tagName': tag['tagName'], 'tagGroup':tag['tagGroup']})
      return tagList

    def insertNewTag(self, tagName, tagGroup):
      tag = self.tagsTable.find_one({'tagName': tagName, 'tagGroup': tagGroup})
      if tag==None:
        newEntry = {'tagName': newTagName, 'tagGroup': newTagGroup}
        self.tagsTable.insert_one(newEntry)
    
    def removeTag(self, tagName, tagGroup):
      self.tagsTable.delete_many({'tagName': tagName, 'tagGroup': tagGroup})  
    
    def getPictureTagsByFolder(self, folderName, pictureName):
      pictureTags = []
      picture = self.picturesTable.find_one({'folder':folderName, 'picture': pictureName})
      if picture!=None:
        pictureTags = picture['tags']
      return pictureTags

    def insertNewFolder(self, newFolderName):
      tag = self.foldersTable.find_one({'folderName': newFolderName})
      if tag==None:
        newEntry = {'folderName': newFolderName}
        self.foldersTable.insert_one(newEntry)

    def removeFolder(self, folderName):
      self.foldersTable.delete_many({'folderName': folderName})

    def getFolderList(self):
      folderList = []
      for folder in self.foldersTable.find():
        folderList.append(folder['folderName'])
      return folderList
    
    def getPictureByTag(self, searchTagList):
      buildList = []
      for tag in searchTagList:
        buildList.append({"tags":tag})
      pictures = [str(id) for id in self.picturesTable.find({"$and":buildList}).distinct('_id')]
      return pictures

    def getPictureById(self, picId):
      return self.picturesTable.find_one(ObjectId(picId))

    def buildPicture(self, folder, filename):
      img = Image.open(join(folder, filename))
      img_io = io.BytesIO()
      img.save(img_io, 'JPEG', quality=30)
      img_io.seek(0)
      return base64.b64encode(img_io.read()).decode("utf-8")
    
    def deleteDb(self):
      self.foldersTable.delete_many({})
      self.tagsTable.delete_many({})
      self.picturesTable.delete_many({})