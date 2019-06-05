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
      loginRules: {
        username: [],
        password: []
      },
      loginLoading: false,
      registerLoading: false,
      operation: 'login',
      passwordType: 'password',
      redirect: undefined
    }
  },
  watch: {
    $route: {
      handler: function (route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  methods: {
    handleLogin () {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loginLoading = true
          this.$router.replace({
            path: '/profile',
            component: resolve => require(['@/pages/profile'], resolve)
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    handleRegister () {
      this.$refs.registerForm.validate(valid => {
        if (valid) {
          this.registerLoading = true
          this.$message({
            type: 'success',
            message: 'Registered successfully!'
          })
          this.operation = 'login'
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>

<style lang="scss">
.login-area{
  padding: 150px 0px 0px 150px;
  text-align: center;
  .login-container {
    width: 500px;
    background-color: #FFFFFF;
    overflow: hidden;
  }
}
</style>
