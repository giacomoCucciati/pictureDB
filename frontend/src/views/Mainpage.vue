<template>
  <b-container>
    <b-container>
      <b-row>
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
          <b-row>
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
          </b-row>
           <b-row>
            <b-col>
              <div class="withMargin">
                <b-button @click="savePicture()" variant="outline-primary">Save Picture and Tags</b-button>
                <b-button @click="removePicture()" variant="outline-primary">Remove Picture from DB</b-button>
              </div>
            </b-col>
          </b-row>
        </b-col>
        <b-col cols="4">
          <b-row>
            <b-col>
              <div class="withMargin">
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
                <b-button v-b-modal="'my-modal'">Delete DB</b-button>

                <!-- The modal -->
                <b-modal id="my-modal" @ok="deleteDB()">Do you really want to delete the full DB?</b-modal>
              </div>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-container>
    <div>
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
              <!-- some space -->
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
    </div>
    <div>
      <b-modal ref="picture-modal" ok-only>
        <b-container>
          <b-row>
            <b-col>
              <div class="withMargin">
                <b-form-group
                  v-slot="{ ariaDescribedby }"
                >
                  <b-form-checkbox-group
                    v-model="selectedTags"
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
        </b-container>
      </b-modal>
    </div>
    <div>
      <b-modal ref="import-folder-modal" hide-footer title="Import folder">
        <div class="d-block text-center">
          <h3>La cartella e' gia' presente nel DB...</h3>
        </div>
        <b-button class="mt-3" variant="outline-danger" block @click="launchImportFolder('clear-tags')">Rimuovi tags delle foto gia' presenti</b-button>
        <b-button class="mt-3" variant="outline-warning" block @click="launchImportFolder('keep-tags')">Aggiungi solo nuove foto</b-button>
      </b-modal>
    </div>
  </b-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MainPage',
  data () {
    return {
      slide: 0,
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
      selectedGroup: ""
    }
  },
  watch: {
    searchTags: function () {
      this.getPictureList()
    }
  },
  methods: {
    showModal: function(group) {
      this.buildGroupModal(group)
      this.$refs['tag-modal'].show()
    },

    showPictureModal: function(group) {
      this.buildGroupModal(group)
      this.$refs['picture-modal'].show()
    },

    buildGroupModal: function(group) {
      this.selectedGroup = group
      this.tagListForModal.length = 0
      for (let i in this.tagList) {
        if (this.tagList[i]['group'] === group) {
          this.tagListForModal.push(this.tagList[i])
        }
      }
    },

    handleOk: function() {
      this.insertTagName = ""
      this.tagListForModal.length = 0
    },

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

    changeTagList: function(action, tagGroup) {
      this.insertTagName = this.insertTagName.trim()
      if (this.insertTagName !== "") {
        let options = {
          tagName: this.insertTagName,
          tagGroup: tagGroup,
          action: action
        }
        axios.post('/api/changeTagList', options).then(response => {
          console.log('changeTagList response: ', response.data.msg)
          this.getTagList()
        })
      }
    },

    getTagList: function() {
      axios.get('/api/getTagList').then(response => {
        console.log('getTagList response: ', response.data.msg)
        let tagListFromDB = response.data.tagList
        this.tagGroups = response.data.tagGroups
        this.tagList.length = 0
        this.selectedTags.length = 0
        this.insertTagName = ""
        this.tagListForModal.length = 0
        for (let i in tagListFromDB) {
          this.tagList.push({text: tagListFromDB[i]['tagName'], value: tagListFromDB[i]['tagName'], group: tagListFromDB[i]['tagGroup']})
        }
        if (this.selectedGroup !== "") {
          for (let i in this.tagList) {
            if (this.tagList[i]['group'] === this.selectedGroup) {
              this.tagListForModal.push(this.tagList[i])
            }
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
      for (let i in this.folderList) {
        if (this.folderList[i]['value'] === this.selectedFolder) {
          this.$refs['import-folder-modal'].show()
          return
        }
      }
      this.launchImportFolder('new-folder')
    },

    launchImportFolder: function(condition) {
      this.$refs['import-folder-modal'].hide()
      let options = {
        newFolder: this.selectedFolder,
        directive: condition
      }
      axios.post('/api/importFolder',options).then(response => {
        console.log('importFolder response: ', response.data.msg)
        this.getFolderList()
        this.searchTags.length = 0
        this.getPictureList()
      })
    },

    getFolderList: function() {
      axios.get('/api/getFolderList').then(response => {
        this.folderList.length = 0
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
      this.pictureList.length = 0
      this.selectedPictureId = ""
      this.pictureUrl = ""
      this.selectedTags.length = 0
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
        this.pictureList.length = 0
        this.selectedPictureId = ""
        this.pictureUrl = ""
        this.selectedTags.length = 0
        this.folderList.length = 0
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