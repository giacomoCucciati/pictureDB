<template>
  <b-container fluid>
    <b-container fluid>
      <b-row>
        <b-col cols="4">
          <b-row>
            <b-col cols="6">
              <TreeExample 
                ref="build-tag-tree"
                :treeDisplayData="editorTagList"
                v-on:delete-node="deleteTag"
                v-on:edit-node="editTag"
                v-on:create-node="createTag"
                v-on:checked-node="newSearchCheck"
                :tagTreeTitle='"Filtro"'
              />              
            </b-col>
            <b-col cols="6">
              <TreeExample 
                ref="select-tag-tree"
                :treeDisplayData="pictureTagList"
                v-on:checked-node="newPictureTagCheck"
                :tagTreeTitle='"Add tag"'
              />
              <b-button @click="savePicture()" variant="outline-primary">Save tags</b-button>
              <b-button @click="saveAllPictures()" variant="outline-primary">Save tags all</b-button>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <!-- some space -->
              <div class="withBigMargin"/>
              <hr>
              <div class="withBigMargin"/>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <div class="withMargin">
                <b-input-group prepend="Main Path" class="mt-3">
                  <b-form-input v-model="mainPath" placeholder="Enter main path"></b-form-input>
                  <b-input-group-append>
                    <b-button @click="saveMainPath()" variant="outline-primary">Save Main</b-button>
                  </b-input-group-append>
                </b-input-group>
              </div>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <!-- some space -->
              <div class="withBigMargin"/>
              <hr>
              <div class="withBigMargin"/>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-row>
                <b-col cols="8">
                  <b-form-file
                    v-model="chosenFileList"
                    :state="Boolean(chosenFileList)"
                    browse-text='Add folder'
                    
                    directory
                    multiple
                  ></b-form-file>
                </b-col>
                <b-col>
                  <b-button @click="editFolder()" :disabled='noFolderSelect' variant="outline-primary">Edit Folder</b-button>
                </b-col>
              </b-row>
              <b-row>
                <b-col class="text-left">
                  <b-form-group v-slot="{ ariaDescribedby }">
                    <!-- <b-form-radio-group
                      v-model="selectedFolder"
                      :options="folderList"
                      :aria-describedby="ariaDescribedby"
                      name="radios-stacked"
                      stacked
                      @input="uncheck()"
                    ></b-form-radio-group> -->
                    <b-form-checkbox-group
                      id="checkbox-group-1"
                      v-model="selectedFolderList"
                      :options="folderList"
                      :aria-describedby="ariaDescribedby"
                      name="flavour-1"
                      stacked
                    ></b-form-checkbox-group>
                  </b-form-group>
                </b-col>
              </b-row>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <!-- some space -->
              <div class="withBigMargin"/>
              <hr>
              <div class="withBigMargin"/>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <div class="withMargin">
                <!-- Using value -->
                <b-button v-b-modal="'my-modal'" >Delete DB</b-button>

                <!-- The modal -->
                <b-modal id="my-modal" @ok="deleteDB()">Do you really want to delete the full DB?</b-modal>
              </div>
            </b-col>
          </b-row>
        </b-col>
        <b-col cols="8">
          <b-row>
            <b-col>
              Number of pictures selected: {{pictureList.length}}
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="1">
              <div class="withMargin">
                <b-button @click="getPrevPicture()" :disabled="noPicturesDisable()" variant="outline-primary">-</b-button>
              </div>
            </b-col>
            <b-col cols="10">
              <div class="withMargin">
                <b-img :src="pictureUrl" fluid alt="Responsive picture" id="mypicture"></b-img>
              </div>
            </b-col>
            <b-col cols="1">
              <div class="withMargin">
                <b-button @click="getNextPicture()" :disabled="noPicturesDisable()" variant="outline-primary">+</b-button>
              </div>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <div class="withMargin">
                <b-button @click="removePicture()" variant="outline-primary">Remove Picture from DB</b-button>
              </div>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-container>
    <div>
      <b-modal ref="import-folder-modal" @ok="okImportModal()" title="Import folder">
        <div class="d-block text-center">
          <h4>{{selectedFolder}}</h4>
          <h3>La cartella e' gia' presente nel DB. Vuoi Applicare delle modifiche? (Rimuovi tags/aggiungi foto/cancella cartella)</h3>
        </div>
      </b-modal>
      <b-modal ref="edit-folder-modal" hide-footer title="Edit folder">
        <div class="d-block text-center">
          <h4>{{selectedFolder}}</h4>
        </div>
        <b-button class="mt-3" variant="outline-danger" block @click="launchEditFolder('clear-tags')">Rimuovi tags delle foto gia' presenti</b-button>
        <b-button class="mt-3" variant="outline-warning" block @click="launchEditFolder('add-pictures')">Aggiungi solo nuove foto</b-button>
        <b-button class="mt-3" variant="outline-warning" block @click="launchEditFolder('delete-folder')">Rimuovi folder e sue foto</b-button>
      </b-modal>
    </div>
  </b-container>
</template>

<script>
import axios from 'axios'
import TreeExample from "../components/TreeTag";

export default {
  name: 'MainPage',
  components: { TreeExample },
  data () {
    return {
      pictureUrl: "",
      editorTagList: [],      // tag list for tag editor
      searchTags: [],         // tag list for search pictures
      pictureTagList: [],     // tag list for picture-modal
      selectedTags: [],       // list of tags to add to the picture
      tagGroups: [],
      selectedFolder: "",
      selectedFolderList: [],
      folderList: [],
      pictureNumber: 0,
      selectedPictureId: "",
      pictureList: [],
      mainPath: "",
      chosenFileList: undefined
    }
  },
  watch: {
    chosenFileList: function () {
      this.importFolder()
    },
    selectedFolderList: function () {
      if (this.selectedFolderList.length > 1) {
        this.selectedFolderList = [this.selectedFolderList[this.selectedFolderList.length-1]]
      }
      if (this.selectedFolderList.length === 1) {
        if (this.selectedFolderList[0] !== this.selectedFolder) {
          this.selectedFolder = this.selectedFolderList[0]
        }
      } else {
        this.selectedFolder = ""
      }
      console.log(this.selectedFolderList, this.selectedFolder)
    },
    selectedFolder: function () {
      this.getPictureList()
    }
  },
  computed: {
    noFolderSelect() {
      console.log('this.selectedFolder', this.selectedFolder)
      if (this.selectedFolder === "") return true
      return false 
    }
  },
  methods: {
    uncheck: function() {
      console.log('Myval')
    },

    // ###################################################
    // #                   Tag Section                   #
    // ###################################################

    deleteTag: function(nodeId) {
      console.log("deleteTag ", nodeId)
      let found = false
      for (let mainTagIndex in this.editorTagList) {
        for (let secondTagIndex in this.editorTagList[mainTagIndex].nodes) {
          const innerTag = this.editorTagList[mainTagIndex].nodes[secondTagIndex]
          if (innerTag.id == nodeId) {
            found = true
          }
        }
      }
      if(!found) {
        console.log('Child node not found. Are you trying to delete a parent node?')
      } else {
        alert("The tag will be deleted also from all the pictures using it")
        let options = {
          action: 'deleteTag',
          tagId: nodeId
        }
        axios.post('/api/changeTag', options).then(response => {
          console.log('deleteTag response: ', response.data.msg)
          this.getTagList()
        })
      }
    },
    editTag: function(nodeId, newName) {
      console.log("editTag ", nodeId, newName)
      let found = false
      for (let mainTagIndex in this.editorTagList) {
        for (let secondTagIndex in this.editorTagList[mainTagIndex].nodes) {
          const innerTag = this.editorTagList[mainTagIndex].nodes[secondTagIndex]
          if (innerTag.id == nodeId) {
            found = true
          }
        }
      }
      if(!found) {
        console.log('Child node not found. Are you trying to edit a parent node?')
      } else {
        alert("The tag will be changed in all the pictures using it")
        let options = {
          action: 'editTag',
          tagId: nodeId,
          newName: newName
        }
        axios.post('/api/changeTag', options).then(response => {
          console.log('editTag response: ', response.data.msg)
          this.getTagList()
        })
      }
    },
    createTag: function(parentNodeId, newname) {
      console.log("createTag ", parentNodeId, newname)
      
      for (let mainTagIndex in this.editorTagList) {
        const innerTag = this.editorTagList[mainTagIndex]
        if (innerTag.id == parentNodeId) {
          if (innerTag.nodes === undefined) {
            // the node doesn't have childs
            // I use $set to ensure that VueJs detect the change
            console.log('Disabled parent node creation')
            // this.$set(node, "nodes", [newNode]);
          } else {
            let options = {
              action: 'createTag',
              parentTagId: parentNodeId,
              newTagName: newname
            }
            axios.post('/api/changeTag', options).then(response => {
              console.log('createTag response: ', response.data.msg)
              this.getTagList()
            })
          }
        }
      }
    },

    newSearchCheck: function() {
      this.searchTags.splice(0)
      for (let mainTagIndex in this.editorTagList) {
        for (let secondTagIndex in this.editorTagList[mainTagIndex].nodes) {
          const innerTag = this.editorTagList[mainTagIndex].nodes[secondTagIndex]
          if (innerTag.state.checked) {
            this.searchTags.push(innerTag.id)
          }
        }
      }
      console.log("searchTags before getPictureList", this.searchTags)
      this.getPictureList()
    },

    newPictureTagCheck: function() {
      this.selectedTags.splice(0)
      for (let mainTagIndex in this.pictureTagList) {
        for (let secondTagIndex in this.pictureTagList[mainTagIndex].nodes) {
          const innerTag = this.pictureTagList[mainTagIndex].nodes[secondTagIndex]
          if (innerTag.state.checked) {
            this.selectedTags.push(innerTag.id)
          }
        }
      }
    },    
    
    // ###################################################
    // #                 Picture Section                 #
    // ###################################################

    noPicturesDisable: function() {
      if (this.pictureList.length === 0) {
        return true
      }
      return false
    },

    savePicture: function () {
      if (this.selectedPictureId != "") {
        let options = {
          selectedTags:     this.selectedTags,
          selectedPictureId:  this.selectedPictureId,
        }
        axios.post('/api/savePicture', options).then(response => {
          console.log('savePicture response: ', response.data.msg)
          this.getPictureList()
        })
      }
    },
    saveAllPictures: function () {
      if (this.pictureList.length !== 0) {
        console.log("lista",this.pictureList)
        let options = {
          selectedTags:     this.selectedTags,
          selectedListaPictureId:  this.pictureList,
        }
        axios.post('/api/saveAllPictures', options).then(response => {
          console.log('saveAllPictures response: ', response.data.msg)
          this.getPictureList()
        })
      }
    },

    removePicture: function () {
      if (this.selectedPictureId != "") {
        let options = {
          selectedPictureId:  this.selectedPictureId,
        }
        axios.post('/api/removePicture', options).then(response => {
          console.log('removePicture response: ', response.data.msg)
        })
      }
    },

    getTagList: function() {
      axios.get('/api/getTagList').then(response => {
        console.log('getTagList response: ', response.data.msg)
        let tagListFromDB = response.data.tagList
        this.tagGroups = response.data.tagGroups
        this.editorTagList.splice(0)
        this.pictureTagList.splice(0)
        this.selectedTags.splice(0)
        for (let index in this.tagGroups) {
          this.editorTagList.push({
            text: this.tagGroups[index],
            id: this.tagGroups[index],
            checkable: true,
            expandable: true,
            state: {checked: false, expanded: false, selected: false},
            nodes: []
          })
          console.log(this.editorTagList)
        }
        for (let i in tagListFromDB) {
          console.log(tagListFromDB[i])
          let groupIndex = undefined
          for (var index in this.editorTagList) {
            if (this.editorTagList[index].id == tagListFromDB[i]['tagGroup']) groupIndex = index
          }
          if (groupIndex == undefined) {
            console.error("Group tag not found: ", tagListFromDB[i]['tagGroup'])
          } else {
            this.editorTagList[groupIndex].nodes.push({
                id: tagListFromDB[i]['tagName'],
                text: tagListFromDB[i]['tagName'],
                expandable: false,
                state: {checked: false, expanded: false, selected: false}
              })
          }
        }
        this.pictureTagList = this.deepCopyFunction(this.editorTagList)
      })
    },

    getPictureTags: function() {
      let options = {
        selectedPictureId: this.selectedPictureId
      }
      axios.post('/api/getPictureTags',options).then(response => {
        console.log('getPictureTags response: ', response.data.msg)
        this.selectedTags = response.data.pictureTags

        for (let mainTagIndex in this.pictureTagList) {
          this.$refs["select-tag-tree"].$refs["my-tree"].collapseNode(this.pictureTagList[mainTagIndex].id);
          let expandIfOneCheck = false // we expand the node if there is at least one check
          for (let secondTagIndex in this.pictureTagList[mainTagIndex].nodes) {
            let innerTag = this.pictureTagList[mainTagIndex].nodes[secondTagIndex]
            if (this.selectedTags.includes(innerTag.id)) {
              innerTag.state.checked = true
              expandIfOneCheck = true
            } else {
              console.log('remove check of ',innerTag.id)
              innerTag.state.checked = false
            }
          }
          if (expandIfOneCheck) {
            //this.$refs["select-tag-tree"].$refs["my-tree"].expandNode(this.pictureTagList[mainTagIndex].id);
          }
        }
      })
    },

    importFolder: async function() {
      try {
        if (this.chosenFileList != undefined) {
          // Collect all directories
          let newImportFolderList = []
          for (let fileIndex in this.chosenFileList) {
            console.log(this.chosenFileList[fileIndex]["$path"])
            let charIndex = this.chosenFileList[fileIndex]["$path"].lastIndexOf("/")
            if (charIndex != -1) {
              let folder = this.chosenFileList[fileIndex]["$path"].substring(0, charIndex+1)
              let thefile = this.chosenFileList[fileIndex]["$path"].substring(charIndex+1)
              console.log(folder,thefile)
              newImportFolderList.push(folder)
            } else {
              throw new Error("No folder selected")
            }
          }
          console.log('newImportFolderList', newImportFolderList)
          if (newImportFolderList.length > 0){
            // reduce the list to unique values
            let uniqueList = newImportFolderList.filter((value, index, self) => {
              return self.indexOf(value) === index;
            });
            console.log('uniqueList', uniqueList)
            // check that each folder is properly defined
            const response = await this.checkFolderExistence(uniqueList)
            if (response.data.error !== '') {
              throw new Error(response.data.error)
            }
            // now import each folder
            var alreadyPresentList = []
            for (let importIndex in uniqueList) {
              let aFolder = uniqueList[importIndex]

              for (let i in this.folderList) {
                if (this.folderList[i]['value'] === aFolder) {
                  alreadyPresentList.push(aFolder)
                }
              }
              if ( !alreadyPresentList.includes(aFolder) ) {
                this.selectedFolder = aFolder
                this.launchEditFolder('new-folder')
              }              
            }
            if (alreadyPresentList.length > 0) {
              alert("These folders are already present in the data base. If you want to modify them use Edit Folder button: " + alreadyPresentList)
            }
          } else {
            throw new Error("Empty folder list!")
          }
        }
      } catch (error) {
        alert(error)
      }
    },
    
    checkFolderExistence: function(list) {
      return axios.post('/api/checkFolderExistence', {folderList: list})
    },

    editFolder: function() {
      this.$refs['edit-folder-modal'].show()
    },

    okImportModal: function() {
      this.$refs['edit-folder-modal'].show()
    },

    launchEditFolder: function(condition) {
      this.$refs['edit-folder-modal'].hide()
      let options = {
        newFolder: this.selectedFolder,
        directive: condition
      }
      axios.post('/api/editFolder',options).then(response => {
        console.log('importFolder response: ', response.data.msg)
        this.getFolderList()
        this.searchTags.splice(0)
        this.getPictureList()
      })
    },

    saveMainPath: function() {
      let options = {
        mainPath: this.mainPath,
      }
      axios.post('/api/saveMainPath',options).then(() => {
        this.updateAll()     
      })
    },

    getMainPath: function() {
      axios.get('/api/getMainPath').then((response) => {
        this.mainPath = response.data.mainFolder
      })
    },

    getFolderList: function() {
      axios.get('/api/getFolderList').then(response => {
        this.folderList.splice(0)
        for (let i in response.data.folderList) {
          this.folderList.push({text:response.data.folderList[i], value:response.data.folderList[i]})
        }
      })
    },

    getNextPicture: function() {
      this.nextPictureNumber()
      this.getPicture()
    },

    getPrevPicture: function() {
      this.prevPictureNumber()
      this.getPicture()
    },

    nextPictureNumber: function() {
      if (this.pictureNumber + 1 == this.pictureList.length) this.pictureNumber = 0
      else this.pictureNumber += 1
    },

    prevPictureNumber: function() {
      if (this.pictureNumber - 1 < 0) this.pictureNumber = this.pictureList.length - 1
      else this.pictureNumber -= 1
    },

    getPictureList: function() {
      this.pictureNumber = 0
      this.pictureList.splice(0)
      this.selectedPictureId = ""
      this.pictureUrl = ""
      this.selectedTags.splice(0)
      // if (this.searchTags.length > 0) {
      let options = {
        searchTagList: this.searchTags,
        searchFolder: this.selectedFolder
      }
      console.log(options)
      axios.post('/api/getPictureList', options).then(response => {
        this.pictureList = response.data.pictureList
        console.log('getPictureList response: ', response.data.msg)
        if (this.pictureList.length > 0) {
          this.getPicture()
        }
      })
      // }
    },

    getPicture: function() {
      this.selectedPictureId = this.pictureList[this.pictureNumber]
      let options = {
        selectedPictureId: this.selectedPictureId
      }
      axios.post('/api/getPicture', options).then(response => {
        console.log('getPicture response: ', response.data.msg)
        if (Object.keys(response.data).includes('picture')) {
          // You can use following line if you do base64.b64encode on server side
          this.pictureUrl = 'data:;base64,' + response.data.picture
          this.getPictureTags()
        } else {
          console.log('No picture found')
        }
      })
    },

    deleteDB: function() {
      axios.get('/api/deleteDb').then(response => {
        console.log('deleteDb response: ', response.data.msg)
        this.getTagList()
        this.getFolderList()
        this.pictureNumber = 0
        this.pictureList.splice(0)
        this.selectedPictureId = ""
        this.pictureUrl = ""
        this.selectedTags.splice(0)
        this.folderList.splice(0)
        this.selectedFolder = ""
      })
    },

    deepCopyFunction: function(inObject) {
      let outObject, value, key

      if (typeof inObject !== "object" || inObject === null) {
        return inObject // Return the value if inObject is not an object
      }

      // Create an array or object to hold the values
      outObject = Array.isArray(inObject) ? [] : {}

      for (key in inObject) {
        value = inObject[key]

        // Recursively (deep) copy for nested objects, including arrays
        outObject[key] = this.deepCopyFunction(value)
      }

      return outObject
    },

    updateAll() {
      this.getTagList()
      this.getFolderList()
      this.getPictureList()
      this.getMainPath()
    }

  },
  mounted () {
    this.updateAll()
    console.log('mounted')
  }
}
</script>

<style scoped>
div.withMargin {
  margin-top: 5px;
  margin-bottom: 5px;
  /* margin-right: 150px;
  margin-left: 80px; */
}
div.withBigMargin {
  margin-top: 20px;
  margin-bottom: 20px;
  /* margin-right: 150px;
  margin-left: 80px; */
}
</style>