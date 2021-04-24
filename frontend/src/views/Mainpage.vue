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
                <b-form-group
                  label="Picture tags"
                  v-slot="{ ariaDescribedby }"
                >
                  <b-form-checkbox-group
                    v-model="selectedTags"
                    :options="tagList"
                    :aria-describedby="ariaDescribedby"
                    name="buttons-1"
                    buttons
                    button-variant="outline-primary"
                  ></b-form-checkbox-group>
                </b-form-group>
              </div>
            </b-col>
          </b-row>
        </b-col>
        <b-col cols="4">
          <b-row>
            <b-col>
              <div class="withMargin">
                <b-form-group
                  label="Search by tag"
                  v-slot="{ ariaDescribedby }"
                >
                  <b-form-checkbox-group
                    v-model="searchTags"
                    :options="tagList"
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
              <div class="withMargin">
                <b-form-group label="Search in folder" v-slot="{ ariaDescribedby }">
                  <b-form-radio-group
                    id="btn-radios-3"
                    v-model="selectedFolder"
                    :options="folderList"
                    :aria-describedby="ariaDescribedby"
                    name="radio-btn-stacked"
                    @change="selectFolder()"
                    buttons
                    stacked
                  ></b-form-radio-group>
                </b-form-group>
              </div>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <div class="withMargin">
                <b-button @click="savePicture()" variant="outline-primary">Save Picture and Tags</b-button>
                <b-button @click="removePicture()" variant="outline-primary">Remove Picture Tags</b-button>
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
                <b-button @click="addTag()" variant="outline-primary">Add Tag</b-button>
                <b-button @click="removeTag()" variant="outline-primary">Remove Tag</b-button>
              </div>
            </b-col>
            <b-col>
              <div class="withMargin">
                <b-form-input v-model="newTagName" placeholder="Enter new tag"></b-form-input>
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
                <b-form-group
                  label="Folder list"
                >
                  <b-form-input v-model="selectedFolder" placeholder="Enter folder"></b-form-input>
                </b-form-group>
                <b-button @click="addFolder()" variant="outline-primary">Add Folder</b-button>
                <b-button @click="removeFolder()" variant="outline-primary">Remove Folder</b-button>
              </div>
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
      newTagName: "",
      tagList: [],
      selectedFolder: "",
      folderList: [],
      pictureNumber: 0,
      selectedPicture: "",
      pictureList: []
    }
  },
  watch: {
    selectedPicture: function (val) {
      if (val != "") {
        this.getPictureTags(this.selectedFolder, val)
      } else {
        this.selectedTags.length = 0
      } 
    },

    searchTags: function () {
      this.selectedFolder = "",
      this.getPictureList('by-tag')
    }
  },
  methods: {

    noPicturesDisable: function() {
      if (this.pictureList.length === 0) {
        return true
      }
      return false
    },

    savePicture: function () {

      if (this.selectedPicture != "") {
        let options = {
          selectedTags:     this.selectedTags,
          selectedPicture:  this.selectedPicture,
        }
        axios.post('/api/savePicture', options).then(response => {
          console.log('savePicture response: ', response.data.msg)
        })
      }
    },

    removePicture: function () {

      if (this.removePicture != "") {
        let options = {
          selectedPicture:  this.selectedPicture,
        }
        axios.post('/api/removePicture', options).then(response => {
          console.log('removePicture response: ', response.data.msg)
        })
      }
    },

    addTag: function() {
      this.newTagName = this.newTagName.trim()
      if (this.newTagName !== "") {
        let options = {
          newTagName: this.newTagName
        }
        axios.post('/api/insertNewTag', options).then(response => {
          console.log('insertNewTag response: ', response.data.msg)
          this.getTagList()
        })
      }
    },

    removeTag: function() {
      let options = {
        tagName: this.newTagName
      }
      axios.post('/api/removeTag', options).then(response => {
        console.log('removeTag response: ', response.data.msg)
        this.getTagList()
      })
    },

    getTagList: function() {
      axios.get('/api/getTagList').then(response => {
        console.log('getTagList response: ', response.data.msg)
        let tagListFromDB = response.data.tagList
        this.tagList.length = 0
        this.selectedTags.length=0
        for (let i in tagListFromDB) {
          this.tagList.push({text: tagListFromDB[i], value: tagListFromDB[i]})
        }
      })
    },

    getPictureTags: function() {
      let options = {
        selectedPicture: this.selectedPicture
      }
      axios.post('/api/getPictureTags',options).then(response => {
        console.log('getPictureTags response: ', response.data.msg)
        this.selectedTags = response.data.pictureTags
      })
    },

    addFolder: function() {
      let options = {
        newFolder: this.selectedFolder
      }
      axios.post('/api/insertNewFolder',options).then(response => {
        console.log('addFolder response: ', response.data.msg)
        this.getFolderList()
      })
    },

    removeFolder: function() {
      let options = {
        badFolder: this.selectedFolder
      }
      axios.post('/api/removeFolder',options).then(response => {
        console.log('removeFolder response: ', response.data.msg)
        this.getFolderList()
      })
    },

    recreateFolderList: function(newList) {
      this.folderList.length = 0
      for (let i in newList) {
          this.folderList.push({text: newList[i], value: newList[i]})
      }
      this.selectedFolder = ""
      this.pictureUrl = ""
    },

    getFolderList: function() {
      axios.get('/api/getFolderList').then(response => {
        console.log('getFolderList response: ', response.data.msg)
        this.recreateFolderList(response.data.folderList)
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

    selectFolder: function() {
      this.getPictureList('by-folder')
    },

    nextPictureNumber: function() {
      console.log(this.pictureList.length)
      if (this.pictureNumber + 1 == this.pictureList.length) this.pictureNumber = 0
      else this.pictureNumber += 1
    },

    prevPictureNumber: function() {
      if (this.pictureNumber - 1 < 0) this.pictureNumber = this.pictureList.length - 1
      else this.pictureNumber -= 1
    },

    getPictureList: function(byMethod) {
      this.pictureNumber = 0
      this.pictureList.length = 0
      this.selectedPicture = ""
      this.pictureUrl = ""
      this.selectedTags.length = 0
      if (byMethod == 'by-folder') {
        this.searchTags.length = 0
        if (this.selectedFolder != "") {
          let options = {
            chriterion: byMethod,
            selectedFolder: this.selectedFolder
          }
          axios.post('/api/getPictureList', options).then(response => {
            
            this.pictureList = response.data.pictureList
            console.log('getPictureList response: ', response.data.msg)
            if (this.pictureList.length > 0) {
              this.getPicture()
            }
          })
        }
      }
      if (byMethod == 'by-tag') {
        this.selectedFolder = ""
        if (this.searchTags.length > 0) {
          let options = {
            chriterion: byMethod,
            searchTagList: this.searchTags
          }
          axios.post('/api/getPictureList', options).then(response => {
            
            this.pictureList = response.data.pictureList
            console.log('getPictureList response: ', response.data.msg)
            if (this.pictureList.length > 0) {
              this.getPicture()
            }
          })
        }
      }
    },

    getPicture: function() {
      console.log('getPicture', this.pictureNumber)
      this.selectedPicture = this.pictureList[this.pictureNumber]
      console.log('getPicture', this.selectedPicture)
      let options = {
        selectedPicture: this.selectedPicture
      }

      axios.post('/api/getPicture', options).then(response => {
        console.log('getPicture response: ', response.data.msg)
        if (Object.keys(response.data).includes('picture')) {
          // You can use following line if you do base64.b64encode on server side
          this.pictureUrl = 'data:;base64,' + response.data.picture;  
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
        this.selectedPicture = ""
        this.pictureUrl = ""
        this.selectedTags.length = 0
      })
    }

  },
  mounted () {
    this.getTagList()
    this.getFolderList()
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