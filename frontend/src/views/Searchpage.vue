<template>
  <b-container>
    <b-container>
      <b-row>
        <b-col cols="8">
          <b-row v-if="pictureList.length>0">
            <b-col>
              <b-row v-for="rowNum in (parseInt(pictureList.length/4)+1)" :key="'row'+rowNum">
                <b-col v-for="colNum in 4" :key="'col'+colNum">
                  <div class="withMargin">
                    <b-img-lazy :src="getImageUrl((rowNum-1)*4+colNum-1)" alt="Image Missing?"></b-img-lazy>
                  </div>
                </b-col>
              </b-row>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
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
        </b-container>
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
      pictureUrl: "",
      selectedTags: [],
      searchTags: [],
      tagList: [],
      tagListForModal: [],
      tagGroups: [],
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
      this.tagListForModal.length = 0
    },

    noPicturesDisable: function() {
      if (this.pictureList.length === 0) {
        return true
      }
      return false
    },

    getTagList: function() {
      axios.get('/api/getTagList').then(response => {
        console.log('getTagList response: ', response.data.msg)
        let tagListFromDB = response.data.tagList
        this.tagGroups = response.data.tagGroups
        this.tagList.length = 0
        this.selectedTags.length = 0
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

    getPictureList: function() {
      this.pictureNumber = 0
      this.pictureList.length = 0
      this.selectedPictureId = ""
      this.pictureUrl = ""
      this.selectedTags.length = 0
      this.selectedFolder = ""
      let options = {
        searchTagList: this.searchTags
      }
      axios.post('/api/getPictureList', options).then(response => {
        this.pictureList = response.data.pictureList
        console.log('getPictureList response: ', response.data.msg)
      })
    },

    getImageUrl: function(pictureNumber) {
      if (pictureNumber >= this.pictureList.length) {
        return ""
      } else {
        let options = {
          selectedPictureId: this.pictureList[pictureNumber]
        }
        axios.post('/api/getPicture', options).then(response => {
          console.log('getPicture response: ', response.data.msg)
          if (Object.keys(response.data).includes('picture')) {
            // You can use following line if you do base64.b64encode on server side
            return 'data:;base64,' + response.data.picture
          } else {
            return ""
          }
        })
      }
    },
    // getPicture: function() {
    //   this.selectedPictureId = this.pictureList[this.pictureNumber]
    //   let options = {
    //     selectedPictureId: this.selectedPictureId
    //   }
    //   axios.post('/api/getPicture', options).then(response => {
    //     console.log('getPicture response: ', response.data.msg)
    //     if (Object.keys(response.data).includes('picture')) {
    //       // You can use following line if you do base64.b64encode on server side
    //       this.pictureUrl = 'data:;base64,' + response.data.picture
    //       this.getPictureTags()
    //     } else {
    //       console.log('No picture found')
    //     }
    //   })
    // }


  },
  mounted () {
    this.getTagList()
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