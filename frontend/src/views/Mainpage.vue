<template>
  <div>
    Pippo {{firstvar}}
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MainPage',
  data () {
    return {
      firstvar: 'Pluto'
    }
  },
  mounted () {
    axios.get('/api/test').then(response => {
      console.log('response: ', response.data.msg)
    })
  }
}
</script>

<style scoped>
</style>