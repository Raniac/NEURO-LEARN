<template>
  <div id="container">
    <TopBar></TopBar>
    <transition name="slide-fade">
      <router-view class="content"></router-view>
    </transition>
  </div>
</template>

<script>
import TopBar from '@/components/common/TopBar.vue'

export default {
  components: {
    TopBar
  }
}
</script>

<style lang='scss'>
#container {
  min-height: 100vh;
  flex: 1 auto;
}
.pull-left {
  float: left;
}
.pull-right {
  float: right;
}
[v-cloak] {
  display: none;
}
a {
  text-decoration: none;
  color: #E8E8E8;
}
.router-link-active {
  color: #00CCFF;
}
.slide-fade-enter-active {
  transition: all .3s ease;
}
.slide-fade-leave-active {
  transition: all 0s cubic-bezier(1.0, 0.5, 0.8, 1.0);
}
.slide-fade-enter, .slide-fade-leave-active {
  transform: translateX(10px);
  opacity: 0;
}
</style>
