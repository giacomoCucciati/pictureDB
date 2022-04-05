<template>
  <b-container fluid>
    <b-container fluid>
      <b-row>
        <b-col cols="4">
          <b-row>
            <b-col cols="6">
              <TreeExample 
                :treeDisplayData="tagList"
                v-on:delete-node="deleteTag"
                v-on:edit-node="editTag"
                v-on:create-node="createTag"
                :checkedTags='searchTags'
                :tagTreeTitle='"Tag Editor"'
              />
              <!-- <div class="withMargin">
                <b-button-group>
                  <b-button v-for="group in tagGroups" :key="group" @click="showModal(group)" variant="success">{{group}}</b-button>
                </b-button-group>
              </div>
              <div class="withMargin">          
                <b-form-tags v-model="searchTags" no-outer-focus>
                  <template v-slot="{ tags, tagVariant, removeTag }">                  
                    <div class="d-inline-block">
                      <b-form-tag
                        v-for="tag in tags"
                        @remove="removeTag(tag)"
                        :key="tag"
                        :title="tag"
                        :variant="tagVariant"
                      >{{ tag }}</b-form-tag>
                    </div>
                  </template>
                </b-form-tags>
              </div>
            </b-col>
            <b-col cols="6"> -->
              
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
                <b-form-group label="Folder options">
                  <b-form-input v-model="selectedFolder" placeholder="Enter folder"></b-form-input>
                </b-form-group>
                <b-button @click="importFolder()" variant="outline-primary">Import Folder</b-button>
                <b-button @click="editFolder()" variant="outline-primary">Edit Folder</b-button>
              </div>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form-group v-slot="{ ariaDescribedby }">
                <b-form-radio-group
                  v-model="selectedFolder"
                  :options="folderList"
                  :aria-describedby="ariaDescribedby"
                  name="radios-stacked"
                  stacked
                ></b-form-radio-group>
              </b-form-group>
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
          <!-- <b-row>
            <b-col>
              <div class="withMargin">
                <b-button-group>
                  <b-button v-for="group in tagGroups" :key="group" @click="showPictureModal(group)">{{group}}</b-button>
                </b-button-group>
              </div>
              <div class="withMargin">          
                <b-form-tags v-model="selectedTags" no-outer-focus>
                  <template v-slot="{ tags, tagVariant, removeTag }">                  
                    <div class="d-inline-block">
                      <b-form-tag
                        v-for="tag in tags"
                        @remove="removeTag(tag)"
                        :key="tag"
                        :title="tag"
                        :variant="tagVariant"
                      >{{ tag }}</b-form-tag>
                    </div>
                  </template>
                </b-form-tags>
              </div>
            </b-col>
          </b-row> -->
          <b-row>
            <b-col>
              <div class="withMargin">
                <b-button v-b-modal="'picture-modal'" variant="outline-primary">Add Tags to Picture</b-button>
                <b-button @click="removePicture()" variant="outline-primary">Remove Picture from DB</b-button>
              </div>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-container>
    <!-- <div>
      <b-modal 
        ref="tag-modal" 
        ok-only 
        no-close-on-esc 
        no-close-on-backdrop
        @ok="handleOk"
      >
        <template #modal-header="">
          <h5>Tags in {{selectedGroup}}</h5>
        </template>
        <b-container>
          <b-row>
            <b-col>
              <div class="withMargin">
                <b-form-group
                  v-slot="{ ariaDescribedby }"
                >
                  <b-form-checkbox-group
                    v-model="searchTags"
                    :options="tagListForModal"
                    :aria-describedby="ariaDescribedby"
                    name="buttons-1"
                    buttons
                    button-variant="outline-primary"
                  ></b-form-checkbox-group>
                </b-form-group>
              </div>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <div class="withBigMargin"/>
              <hr>
              <div class="withBigMargin"/>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <div class="withMargin">
                <b-form-input v-model="insertTagName" placeholder="Enter tag"></b-form-input>
              </div>
            </b-col>
            <b-col>
              <div class="withMargin">
                <b-button @click="changeTagList('add-tag', selectedGroup)" variant="outline-primary">Add Tag</b-button>
                <b-button @click="changeTagList('remove-tag', selectedGroup)" variant="outline-primary">Remove Tag</b-button>
              </div>
            </b-col>
          </b-row>
        </b-container>
      </b-modal>
    </div> -->
    <div>
      <b-modal id="picture-modal" @ok="savePicture()">
        <b-container>
          <b-row>
            <b-col>
              <div class="withMargin">
                <TreeExample 
                  :treeDisplayData="tagList"
                  :checkedTags='selectedTags'
                  :tagTreeTitle='"Tag Editor"'
                />
              </div>
            </b-col>
          </b-row>
        </b-container>
      </b-modal>
    </div>
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
import '@riophae/vue-treeselect/dist/vue-treeselect.css'
import axios from 'axios'
import TreeExample from "../components/TreeTag";

export default {
  name: 'MainPage',
  components: { TreeExample },
  data () {
    return {
      pictureUrl: "",
      selectedTags: [],
      searchTags: [],
      insertTagName: "",
      tagList: [],
      tagListForModal: [],
      tagGroups: [],
      selectedFolder: "",
      folderList: [],
      pictureNumber: 0,
      selectedPictureId: "",
      pictureList: [],
      selectedGroup: "",
    }
  },
  watch: {
    searchTags: function () {
      console.log('searchTags', this.searchTags)
      this.getPictureList()
    }
  },
  methods: {

    // ###################################################
    // #                   Tag Section                   #
    // ###################################################

    deleteTag: function(nodeId) {
      console.log("deleteTag ", nodeId)
      let found = false
      for (let mainTagIndex in this.tagList) {
        for (let secondTagIndex in this.tagList[mainTagIndex].nodes) {
          const innerTag = this.tagList[mainTagIndex].nodes[secondTagIndex]
          if (innerTag.id == nodeId) {
            // this.tagList[mainTagIndex].nodes.splice(secondTagIndex,1)
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
      for (let mainTagIndex in this.tagList) {
        for (let secondTagIndex in this.tagList[mainTagIndex].nodes) {
          const innerTag = this.tagList[mainTagIndex].nodes[secondTagIndex]
          if (innerTag.id == nodeId) {
            // innerTag.text = newName            
            // innerTag.id = newName
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
    createTag: function(parentNodeId) {
      console.log("createTag ", parentNodeId)
      
      for (let mainTagIndex in this.tagList) {
        const innerTag = this.tagList[mainTagIndex]
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
            }
            axios.post('/api/changeTag', options).then(response => {
              console.log('createTag response: ', response.data.msg)
              this.getTagList()
            })
          }
        }
      }
    },
    // open(target, cm) {
    //         console.log(target, cm);
    //         // other actions...
    //     },

    //     close(target, cm) {
    //         console.log(target, cm);
    //         // other actions...
    //     },
    // showModal: function(group) {
    //   this.buildGroupModal(group)
    //   this.$refs['tag-modal'].show()
    // },

    // showPictureModal: function(group) {
    //   this.buildGroupModal(group)
    //   this.$refs['picture-modal'].show()
    // },

    // buildGroupModal: function(group) {
    //   this.selectedGroup = group
    //   this.tagListForModal.splice(0)
    //   for (let i in this.tagList) {
    //     if (this.tagList[i]['group'] === group) {
    //       this.tagListForModal.push(this.tagList[i])
    //     }
    //   }
    // },

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
        console.log(options)
        // axios.post('/api/savePicture', options).then(response => {
        //   console.log('savePicture response: ', response.data.msg)
        // })
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
        this.tagList.splice(0)
        this.selectedTags.splice(0)
        this.insertTagName = ""
        for (let index in this.tagGroups) {
          this.tagList.push({
            text: this.tagGroups[index],
            id: this.tagGroups[index],
            checkable: true,
            nodes: []
          })
          console.log(this.tagList)
        }
        for (let i in tagListFromDB) {
          console.log(tagListFromDB[i])
          let groupIndex = undefined
          for (var index in this.tagList) {
            if (this.tagList[index].id == tagListFromDB[i]['tagGroup']) groupIndex = index
          }
          if (groupIndex == undefined) {
            console.error("Group tag not found: ", tagListFromDB[i]['tagGroup'])
          } else {
            this.tagList[groupIndex].nodes.push({
                id: tagListFromDB[i]['tagName'],
                text: tagListFromDB[i]['tagName'],
              })
          }
        }
      })
    },

    getPictureTags: function() {
      let options = {
        selectedPictureId: this.selectedPictureId
      }
      axios.post('/api/getPictureTags',options).then(response => {
        console.log('getPictureTags response: ', response.data.msg)
        this.selectedTags = response.data.pictureTags
      })
    },

    importFolder: function() {
      if (this.selectedFolder === "") {
        return
      }
      for (let i in this.folderList) {
        if (this.folderList[i]['value'] === this.selectedFolder) {
          this.$refs['import-folder-modal'].show()
          return
        }
      }
      this.launchEditFolder('new-folder')
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
      this.selectedFolder = ""
      // if (this.searchTags.length > 0) {
      let options = {
        searchTagList: this.searchTags
      }
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
    }

  },
  mounted () {
    this.getTagList()
    this.getFolderList()
    this.getPictureList()
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