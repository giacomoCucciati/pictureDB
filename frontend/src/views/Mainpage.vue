<template>
  <div>
    <b-container class="bv-example-row">
      <b-row>
        <b-col cols="6">
          <b-row>
            <b-col cols="1">
              <b-button @click="getPrevPicture()" variant="outline-primary">-</b-button>
            </b-col>
            <b-col cols="10">
              <div>
                <b-img :src="pictureUrl" fluid alt="Responsive picture" id="mypicture"></b-img>
              </div>
            </b-col>
            <b-col cols="1">
              <b-button @click="getNextPicture()" variant="outline-primary">+</b-button>
            </b-col>
          </b-row>
          <b-row>
            <b-col>              
              <div>
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
        <b-col cols="6">
          <b-row>
            <b-col>
              <div>
                <b-button @click="savePicture()" variant="outline-primary">Save Picture and Tags</b-button>
              </div>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-button @click="addTag()" variant="outline-primary">Add Tag</b-button>
            </b-col>
            <b-col>
              <b-form-input v-model="newTagName" placeholder="Enter new tag"></b-form-input>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              Folders
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form-input v-model="selectedFolder" placeholder="Enter folder"></b-form-input>
              <b-button @click="addFolder()" variant="outline-primary">Add Folder</b-button>
              <b-button @click="removeFolder()" variant="outline-primary">Remove Folder</b-button>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form-group label="Folder list" v-slot="{ ariaDescribedby }">
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
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <div>
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
        </b-col>
      </b-row>
    </b-container>
  </div>
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
      this.getPictureTags(this.selectedFolder, val)
    },

    searchTags: function () {
      this.getPictureList('by-tag')
    }
  },
  methods: {
    savePicture: function () {
      if (this.selectedPicture != "" && this.selectedFolder != "") {
        let options = {
          selectedTags: this.selectedTags,
          folderName:   this.selectedFolder,
          pictureName:  this.selectedPicture
        }
        axios.post('/api/savePicture', options).then(response => {
          console.log('savePicture response: ', response.data.msg)
        })
      }
    },

    addTag: function() {
      let options = {
        newTagName: this.newTagName
      }
      axios.post('/api/insertNewTag', options).then(response => {
        console.log('insertNewTag response: ', response.data.msg)
        this.getTagList()
      })
    },

    getTagList: function() {
      axios.get('/api/getTagList').then(response => {
        console.log('getTagList response: ', response.data.msg)
        let tagListFromDB = response.data.tagList
        this.tagList.length = 0
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
      if (byMethod == 'by-folder') {
        if (this.selectedFolder != "") {
          let options = {
            chriterion: byMethod,
            selectedFolder: this.selectedFolder
          }
          axios.post('/api/getPictureList', options).then(response => {
            
            this.pictureList = response.data.pictureList
            console.log('getPictureList response: ', response.data.msg)
            if (this.pictureList.length > 0) {
              this.pictureNumber = 0
              this.getPicture()
            }
          })
        }
      }
      if (byMethod == 'by-tag') {
        if (this.searchTags.length > 0) {
          let options = {
            chriterion: byMethod,
            searchTagList: this.searchTags
          }
          axios.post('/api/getPictureList', options).then(response => {
            
            this.pictureList = response.data.pictureList
            console.log('getPictureList response: ', response.data.msg)
            if (this.pictureList.length > 0) {
              this.pictureNumber = 0
              this.getPicture()
            }
          })
        }
      }
    },

    getPicture: function() {
      this.selectedPicture = this.pictureList[this.pictureNumber]
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
</style>