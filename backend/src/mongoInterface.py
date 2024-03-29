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
        if not 'tags' in self.db.list_collection_names():
            self.db.create_collection('tags')
        self.tagsTable = self.db['tags']
        if not 'folders' in self.db.list_collection_names():
            self.db.create_collection('folders')
        self.foldersTable = self.db['folders']
        if not 'pictures' in self.db.list_collection_names():
            self.db.create_collection('pictures')
        self.picturesTable = self.db['pictures']

###################################################
#                   Tag Section                   #
###################################################

    def createTag(self, tagGroup, newtagName):
      tag = self.tagsTable.find_one({'tagName': newtagName})
      if tag==None:
        newEntry = {'tagName': newtagName, 'tagGroup': tagGroup}
        self.tagsTable.insert_one(newEntry)
    
    def removeTag(self, tagName):
      print(self.picturesTable.find({'tags':tagName}))
      self.tagsTable.delete_many({'tagName': tagName})  

    def editTag(self, tagName, newName):
      tag = self.tagsTable.find_one({'tagName': newName})
      if tag==None:
        print(self.picturesTable.find({'tags':tagName}))
        newvalues = { "$set": { "tagName": newName } }
        self.tagsTable.update_one({'tagName': tagName}, newvalues)

    def savePicture(self, folderName, pictureName, selectedTags, overwrite=True):
      picture = self.picturesTable.find_one({'folder': folderName, 'filename': pictureName})
      print('savePicture',picture)
      if picture==None:
        newEntry = {'folder': folderName, 'filename': pictureName, 'tags':selectedTags}
        self.picturesTable.insert_one(newEntry)
      elif overwrite:
        self.updatePictureTags(picture['_id'], selectedTags)
    
    def removePicture(self, selectedPictureId):
      self.picturesTable.delete_many({"_id":ObjectId(selectedPictureId)})

    def updatePictureTags(self, picId, selectedTags):
      picture = self.picturesTable.find_one(ObjectId(picId))
      if picture==None:
        print('Error in updatePictureTags')
      newtags = { "$set": { "tags": selectedTags} }
      print('updatePictureTags newtags', newtags)
      self.picturesTable.update_one({"_id":ObjectId(picId)}, newtags)
      picture = self.picturesTable.find_one(ObjectId(picId))
      print('after update', picture)

    def getTagList(self):
      tagList = []
      for tag in self.tagsTable.find():
        tagList.append({'tagName': tag['tagName'], 'tagGroup':tag['tagGroup']})
      return tagList

    def insertMainPath(self, mainPath):
      folder = self.foldersTable.find_one({ 'mainFolder': { "$exists": True } })
      if folder==None:
        newEntry = {'mainFolder': mainPath}
        self.foldersTable.insert_one(newEntry)
      else:
        print("HEREEEEEEEEEEEEE")
        newpath = { "$set": { "mainFolder": mainPath} }
        self.foldersTable.update_one({'_id': folder['_id']}, newpath)

    def getMainPath(self):
      result = self.foldersTable.find_one({ 'mainFolder': { "$exists": True } })
      if result != None:
        return result['mainFolder']
      return None

    def insertNewFolder(self, newFolderName):
      folder = self.foldersTable.find_one({'folderName': newFolderName})
      if folder==None:
        newEntry = {'folderName': newFolderName}
        self.foldersTable.insert_one(newEntry)

    def deleteFolder(self, folderName, deletePictures=True):
      self.foldersTable.delete_one({'folderName': folderName})
      if deletePictures:
        self.picturesTable.delete_many({"folder":folderName})

    def getFolderList(self):
      folderList = []
      for folder in self.foldersTable.find({ 'folderName': { "$exists": True } }):
        folderList.append(folder['folderName'])
      return folderList
    
    def getPictureByTag(self, searchTagList):
      buildList = []
      if len(searchTagList) > 0:
        for tag in searchTagList:
          buildList.append({"tags":tag})
        pictures = [str(id) for id in self.picturesTable.find({"$and":buildList}).distinct('_id')]
      else:
        print("mongoInterface::getPictureByTag Get pictures with no tag")
        pictures = [str(id) for id in self.picturesTable.find({"tags":[]}).distinct('_id')]
      return pictures

    def getPictureByTagAndFolder(self, searchTagList, searchFolder):
      find = {}
      buildList = []
      for tag in searchTagList:
        buildList.append({"tags":tag})
      if searchFolder != "":
        mainPath = self.getMainPath()
        if mainPath != None:
          buildList.append({"folder":join(mainPath, searchFolder)})
      if len(buildList) > 0:
        find = {"$and":buildList}
      else: 
        find = {"tags":[]}
      print("find",find)
      pictures = [str(id) for id in self.picturesTable.find(find).distinct('_id')]
      return pictures

    def getPictureById(self, picId):
      return self.picturesTable.find_one(ObjectId(picId))

    def buildPicture(self, folder, filename):
      img = Image.open(join(folder, filename))
      img_io = io.BytesIO()
      if filename.lower().endswith('jpeg') or filename.lower().endswith('jpg'):
        img.save(img_io, 'JPEG', quality=10)
      elif filename.lower().endswith('png'):
        img.save(img_io, 'PNG', quality=10)
      else: 
        raise Exception("Wrong picture format!")
      img_io.seek(0)
      return base64.b64encode(img_io.read()).decode("utf-8")
    
    def deleteDb(self):
      self.foldersTable.delete_many({})
      self.tagsTable.delete_many({})
      self.picturesTable.delete_many({})