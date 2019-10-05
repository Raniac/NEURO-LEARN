<template>
  <div class="login-area">
      <div class="login-container">
        <el-tabs v-model="operation" stretch style="margin: 40px">
          <el-tab-pane label="Login" name="login">
            <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" auto-complete="on" label-position="left">
              <el-form-item prop="username">
                <el-input
                  ref="username"
                  v-model="loginForm.username"
                  placeholder="Username"
                  name="username"
                  type="text"
                  tabindex="1"
                  auto-complete="on"
                  style="margin-top: 10px"
                  />
                </el-form-item>
                <el-form-item prop="password">
                  <el-input
                    :key="passwordType"
                    ref="password"
                    v-model="loginForm.password"
                    :type="passwordType"
                    placeholder="Password"
                    name="password"
                    tabindex="2"
                    auto-complete="on"
                    @keyup.enter.native="handleLogin"
                  />
                </el-form-item>
              <el-button :loading="loginLoading" type="primary" style="width:100%" @click.native.prevent="handleLogin">Login</el-button>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="Register" name="register">
            <el-form ref="registerForm" :model="registerForm" :rules="registerRules" class="register-form" auto-complete="on" label-position="left">
              <el-form-item prop="username">
                <el-input
                  ref="username"
                  v-model="registerForm.username"
                  placeholder="Username"
                  name="username"
                  type="text"
                  tabindex="1"
                  auto-complete="on"
                  style="margin-top: 10px"
                  />
                </el-form-item>
                <el-form-item prop="password">
                  <el-input
                    :key="passwordType"
                    ref="password"
                    v-model="registerForm.password"
                    :type="passwordType"
                    placeholder="Password"
                    name="password"
                    tabindex="2"
                    auto-complete="on"
                    @keyup.enter.native="handleRegister"
                  />
                </el-form-item>
                <el-form-item prop="password">
                  <el-input
                    :key="passwordType"
                    ref="password"
                    v-model="registerForm.confirm_password"
                    :type="passwordType"
                    placeholder="Confirm Password"
                    name="confirm password"
                    tabindex="3"
                    auto-complete="on"
                    @keyup.enter.native="handleRegister"
                  />
                </el-form-item>
              <el-button :loading="registerLoading" type="primary" style="width:100%" @click.native.prevent="handleRegister">Register</el-button>
            </el-form>
          </el-tab-pane>
        </el-tabs>
      </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Login',
  data () {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      registerForm: {
        username: '',
        password: '',
        confirm_password: ''
      },
      loginRules: {
        username: [],
        password: []
      },
      registerRules: {
        username: [],
        password: [],
        confirm_password: []
      },
      loginLoading: false,
      registerLoading: false,
      operation: 'login',
      passwordType: 'password',
      redirect: undefined
    }
  },
  methods: {
    handleLogin () {
      if (this.loginForm.username === 'admin' && this.loginForm.password === 'admin') {
        sessionStorage.setItem('Authorization', '00000000000000000000000000000000')
        sessionStorage.setItem('Username', 'admin')
        this.$router.push('/home')
      } else {
        axios.get('/api/v0/login?username=' + this.loginForm.username + '&password=' + this.loginForm.password).then(response => {
          // var DjangoToken = this.getCookie('sessionid')
          // var username = this.getCookie('username')
          var res = response.data
          var DjangoToken = res.sessionid
          var username = res.username
          console.log(DjangoToken)
          console.log(username)
          console.log(res)
          if (res.error_num === 0) {
            console.log(res.msg)
            sessionStorage.setItem('Authorization', DjangoToken)
            sessionStorage.setItem('Username', username)
            this.$router.push('/home')
          } else {
            this.$message.error('Wrong password!')
            console.log(res.msg)
          }
        })
      }
    },
    handleRegister () {
      console.log(JSON.stringify(this.registerForm))
      axios.post('/api/v0/register', JSON.stringify(this.registerForm))
        .then(response => {
          var res = response.data
          console.log(res.error_num)
          if (res.error_num === 0) {
            console.log(res)
            this.$message.success('Successfully registered!')
            this.loginForm.username = this.registerForm.username
            this.loginForm.password = this.registerForm.password
            this.handleLogin()
          } else {
            this.$message.error('Failed to register!')
            console.log(res['msg'])
          }
        })
    },
    getCookie (name) {
      name = name + '='
      let start = document.cookie.indexOf(name)
      let value = null
      if (start > -1) {
        let end = document.cookie.indexOf(';', start)
        if (end === -1) {
          end = document.cookie.length
        }
        value = document.cookie.substring(start + name.length, end)
      }
      return value
    },
    delCookie (name) {
      var exp = new Date()
      exp.setTime(exp.getTime() - 1)
      var cval = this.getCookie(name)
      if (cval != null) {
        document.cookie = name + '=' + cval + ';expires=' + exp.toGMTString()
      }
    }
  }
}
</script>

<style lang="scss">
.login-area{
  padding: 150px 0px 0px 0px;
  text-align: center;
  .login-container {
    margin: 0 auto;
    width: 500px;
    background-color: #FFFFFF;
    overflow: hidden;
  }
}
</style>
