from pymongo import MongoClient
import copy
import json

class MongoInterface:

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['picturedb']
        if not 'tags' in self.db.collection_names():
            self.db.create_collection('tags')
        self.tagsTable = self.db['tags']
        if not 'pictures' in self.db.collection_names():
            self.db.create_collection('pictures')
        self.picturesTable = self.db['pictures']

    def savePicture(self, pictureName, selectedTags):
      print(pictureName, selectedTags)
      
      picture = self.picturesTable.find_one({'picture': pictureName})
      if picture==None:
        newEntry = {'picture': pictureName, 'tags':selectedTags}
        self.picturesTable.insert_one(newEntry)
      else:
        newtags = { "$set": { "tags": selectedTags} }
        self.picturesTable.update_one({'picture': pictureName}, newtags)
      print(self.picturesTable.find_one({'picture': pictureName}))

    def getTagList(self):
      tagList = []
      for tag in self.tagsTable.find():
        tagList.append(tag['tagName'])
      return tagList

    def insertNewTag(self, newTagName):
      print(newTagName)
      tag = self.tagsTable.find_one({'tagName': newTagName})
      if tag==None:
        newEntry = {'tagName': newTagName}
        self.tagsTable.insert_one(newEntry)
    
    def getPictureTags(self, pictureName):
      print('pictureName',pictureName)
      pictureTags = []
      picture = self.picturesTable.find_one({'picture': pictureName})
      if picture!=None:
        pictureTags = picture['tags']
      return pictureTags
