<template>
  <b-container fluid>
    <b-container fluid>
      <b-row>
        <b-col cols="8">
          <b-row v-if="pictureList.length>0">
            <b-col>
              <b-row v-for="rowNum in (parseInt((pictureList.length-1)/4)+1)" :key="'row'+rowNum">
                <b-col v-if="[(rowNum-1)*4+0]<pictureList.length">
                  <div class="withMargin">
                    <b-img :src="temp_url[(rowNum-1)*4+0]" alt="Image Missing?"></b-img> 
                  </div>
                </b-col>
                <b-col v-if="[(rowNum-1)*4+1]<pictureList.length">
                  <div class="withMargin">
                    <b-img :src="temp_url[(rowNum-1)*4+1]" alt="Image Missing?"></b-img> 
                  </div>
                </b-col>
                <b-col v-if="[(rowNum-1)*4+2]<pictureList.length">
                  <div class="withMargin">
                    <b-img :src="temp_url[(rowNum-1)*4+2]" alt="Image Missing?"></b-img> 
                  </div>
                </b-col>
                <b-col v-if="[(rowNum-1)*4+3]<pictureList.length">
                  <div class="withMargin">
                    <b-img :src="temp_url[(rowNum-1)*4+3]" alt="Image Missing?"></b-img> 
                  </div>
                </b-col>
              </b-row>
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
      searchTags: [],
      tagList: [],
      tagListForModal: [],
      tagGroups: [],
      pictureList: [],
      selectedGroup: "",
      temp_url: [],
      temp_single_url: ""
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

    getTagList: function() {
      axios.get('/api/getTagList').then(response => {
        console.log('getTagList response: ', response.data.msg)
        let tagListFromDB = response.data.tagList
        this.tagGroups = response.data.tagGroups
        this.tagList.length = 0
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

    getPictureList: function() {
      this.pictureList.length = 0
      this.selectedFolder = ""
      let options = {
        searchTagList: this.searchTags
      }
      axios.post('/api/getPictureList', options).then(response => {
        this.pictureList = response.data.pictureList
        console.log('getPictureList response: ', response.data.msg)
        this.temp_url.length=0
        for (let index in this.pictureList) {
          this.getImageUrl(index)
        }
      })
    },

    getImageUrl: function(pictureNumber) {
      let options = {
        selectedPictureId: this.pictureList[pictureNumber]
      }
      axios.post('/api/getPicture', options).then(response => {
        console.log('getPicture response: ', response.data.msg)
        if (Object.keys(response.data).includes('picture')) {
          // You can use following line if you do base64.b64encode on server side
          this.temp_url.push('data:;base64,' + response.data.picture)
        }
      })
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