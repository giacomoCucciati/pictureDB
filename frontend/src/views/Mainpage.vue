<template>
  <div>
    Pippo {{firstvar}}
    <b-container class="bv-example-row">
      <b-row>
        <b-col cols="6">
          <div>
            <b-img :src="imageUrl" fluid alt="Responsive image"></b-img>
          </div>
        </b-col>
        <b-col cols="6">
          <b-row>
            <b-col>
              <div>
                <b-form-file v-model="fileList" class="mt-3" multiple plain></b-form-file>
              </div>
            </b-col>
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
              <div>
                <b-form-group
                  label="Button-group style checkboxes"
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
      firstvar: 'Pluto',
      imageUrl: "",
      fileList: [],
      selectedTags: [],
      newTagName: "",
      tagList: []
    }
  },
  watch: {
    fileList: function (val) {
      if (val.length > 0) {
        this.getPictureTags(val[0].name)
        this.imageUrl = URL.createObjectURL(val[0])
      }
    }
  },
  methods: {
    savePicture: function () {
      if (this.fileList.length > 0) {
        let options = {
          selectedTags: this.selectedTags,
          pictureName: this.fileList[0].name
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
        console.log('getTagList response: ', response.data.tagList)
        let tagListFromDB = response.data.tagList
        this.tagList.length = 0
        for (let i in tagListFromDB) {
          this.tagList.push({text: tagListFromDB[i], value: tagListFromDB[i]})
        }
      })
    },

    getPictureTags: function(pictureName) {
      let options = {
        pictureName: pictureName
      }
      axios.post('/api/getPictureTags',options).then(response => {
        console.log('getPictureTags response: ', response.data.msg)
        console.log('getPictureTags response: ', response.data.pictureTags)
        this.selectedTags = response.data.pictureTags
      })
    }
  },
  mounted () {
    this.getTagList()
    console.log('mounted')
  }
}
</script>

<style scoped>
</style>