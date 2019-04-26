<template>
  <div id="app">
    <NavMenu></NavMenu>
    <Container></Container>
  </div>
</template>

<script>
import NavMenu from '@/components/common/NavMenu.vue'
import Container from '@/components/common/Container.vue'

export default {
  name: 'app',
  components: {
    NavMenu,
    Container
  }
}
</script>

<style lang='scss'>
body {
  margin:0;
  padding:0;
  font-family: Arial, Helvetica, sans-serif;
  // font-size: 40px;
}
#app {
  display: flex;
  min-width: 800px;
  background-color: #E8E8E8;
  color: #282828;
}
</style>
