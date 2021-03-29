<template>
  <div>
    Pippo {{firstvar}}
    <div>
      <b-img :src="imageUrl" fluid alt="Responsive image"></b-img>
    </div>
    <div>
      <b-form-file v-model="fileList" class="mt-3" multiple plain></b-form-file>
      {{imageUrl}}
    </div>
  </div>
</template>

<script>
//import axios from 'axios'

export default {
  name: 'MainPage',
  data () {
    return {
      firstvar: 'Pluto',
      imageUrl: "",
      fileList: []
    }
  },
  watch: {
    fileList: function (val) {
      if (val.length > 0) {
        console.log(val[0])
        this.imageUrl = URL.createObjectURL(val[0])
      }
    }
  },
  mounted () {
    // axios.get('/api/test').then(response => {
    //   console.log('response: ', response.data.msg)
    // })
    console.log('mounted')
  }
}
</script>

<style scoped>
</style>