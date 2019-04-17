<template lang="html">
<div>
  <el-menu default-active="1" id="nav-menu">
    <div class="logo">
      <router-link to="/" class="nav-title">
        NEURO-LEARN
      </router-link>
    </div>
    <el-menu-item index="1"><router-link to="/overview" class="nav-link"><i class="el-icon-menu"></i>Overview</router-link></el-menu-item>
    <el-submenu index="2">
      <template slot="title"><i class="el-icon-edit-outline"></i><span style="font-size: 16px; color: #dbdbdb">New Task</span></template>
      <el-menu-item index="2-1"><router-link to="/newsa" class="nav-link"><i class="el-icon-edit"></i>Statistical Analysis</router-link></el-menu-item>
      <el-menu-item index="2-2"><router-link to="/newml" class="nav-link"><i class="el-icon-edit"></i>Machine Learning</router-link></el-menu-item>
      <el-menu-item index="2-3"><router-link to="/newdl" class="nav-link"><i class="el-icon-edit"></i>Deep Learning</router-link></el-menu-item>
    </el-submenu>
    <el-menu-item index="3"><router-link to="/submissions" class="nav-link"><i class="el-icon-tickets"></i>Submissions</router-link></el-menu-item>
    <el-menu-item index="4"><router-link to="/viewer" class="nav-link"><i class="el-icon-view"></i>Viewer</router-link></el-menu-item>
    <el-menu-item index="5"><router-link to="/help" class="nav-link"><i class="el-icon-question"></i>Help</router-link></el-menu-item>
    <el-menu-item index="6"><router-link to="/test" class="nav-link"><i class="el-icon-loading"></i>Test</router-link></el-menu-item>
  </el-menu>
  </div>
</template>

<style lang='scss'>
#nav-menu {
  width: 250px;
  min-width: 250px;
  height: 100%;
  background-color: #282828;
  border-right-color: #282828;
  box-shadow: 5px 0 20px rgba(0,0,0,.3);
  .logo {
    width: 250px;
    height: 65px;
    text-align: center;
    background-color: #282828;
  }
  .nav-title {
    display: block;
    padding-top: 20px;
    font-size: 25px;
    font-weight: 600;
    color: #E8E8E8;
  }
  .nav-link {
    display: block;
    font-size: 16px;
  }
  .el-menu {
    background-color: #282828;
  }
  .el-menu-item,
  .el-submenu .el-submenu__title {
    height: 44px;
    line-height: 44px;
    color: #E8E8E8;
    &:hover {
      background-color: #505050;
    }
  }
  .router-link-active {
    color: #00CCFF;
  }
}
</style>

<script>
export default {
}
</script>
