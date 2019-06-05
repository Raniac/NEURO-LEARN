<template>
  <div style="background-color: #FFFFFF; margin: 14px; padding: 14px">
    <el-form :model="loginForm">
      <el-form-item label="UserName">
        <el-input v-model="loginForm.username"></el-input>
      </el-form-item>
      <el-form-item label="PassWord">
        <el-input v-model="loginForm.password"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleLogin('loginForm')">Login</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data () {
    return {
      loginForm: {
        csfmiddlewaretoken: '',
        username: '',
        password: ''
      }
    }
  },
  methods: {
    handleChange (file, fileList) {
      this.fileList = fileList.slice(-4)
    },
    uploadSuccess (response) {
      console.log(response.error_num, response.msg)
    }
  },
  mounted () {
    var vm = this
    vm.$axios({
      method: 'get',
      baseURL: '/api',
      url: '/accounts/login/'
    })
      .then(function (response) {
        // const regex = /csrfmiddlewaretoken' value='(.*)'/gm
        var arr
        var reg = new RegExp("csrfmiddlewaretoken' value='(.*)'")

        if (arr === response.data.match(reg)) {
          vm.form.csrfmiddlewaretoken = unescape(arr[1])
        } else {
          console.log('not found crsf value')
        }
      })
  }
}
</script>
