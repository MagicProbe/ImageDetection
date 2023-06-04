<template>
  <div style="padding-top: 100px;">
    <el-row>
        <el-col :span="8"></el-col>
        <el-col :span="8">
          <el-card class="card" shadow="hover">
        <div>
          <h1>Login</h1>
        </div>
        <el-form v-if="!isLoggedIn" ref="loginForm" :model="loginForm" :rules="loginRules" label-width="80px">
          <el-form-item label="Email" prop="email">
            <el-input v-model="loginForm.email" placeholder="Please enter your email"></el-input>
          </el-form-item>
          <el-form-item label="Password" prop="password">
            <el-input type="password" v-model="loginForm.password" placeholder="Please enter your password"></el-input>
          </el-form-item>
          <el-form-item>
            <router-link to="/forgotpassword">Forgot your password?</router-link>
          </el-form-item>

          <el-row>
            <el-col :span="11">
              <el-button type="info" @click="toRegister" style="width: 100%">Register</el-button>
            </el-col>
            <el-col :span="2"></el-col>
            <el-col :span="11">
              <el-button type="primary" @click="login" style="width: 100%">Login</el-button>
            </el-col>
           </el-row>
        </el-form>
        <div class="success-message" v-if="isLoggedIn">
          <h2>Welcome, {{ user.attributes.email }}!</h2>
          <el-button @click="logout">Logout</el-button>
        </div>
      </el-card>
        </el-col>
        <el-col :span="8"></el-col>
    </el-row>
  
    </div>
  </template>
  
  <script>
  import { CognitoUserPool, AuthenticationDetails, CognitoUser } from 'amazon-cognito-identity-js'
  
  // 配置 AWS Cognito 身份池
  const poolData = {
    UserPoolId: 'us-east-1_gDIoH9hFt',
    ClientId: '5qe26bvhvj2i5vrl83er54q6ks'
  }
  const userPool = new CognitoUserPool(poolData)
  
  export default {
    name: 'LoginPage',
    data() {
      return {
        isRegistered: false,
        isLoggedIn: false,
        user: null,
        loginForm: {
          email: '',
          password: ''
        },
        loginRules: {
          email: [
            { required: true, message: 'Please enter your email', trigger: 'blur' },
            { type: 'email', message: 'Please enter a valid email address', trigger: ['blur', 'change'] }
          ],
          password: [
            { required: true, message: 'Please enter your password', trigger: 'blur' }
          ]
        }
      }
    },
    methods: {
      toRegister() {
        this.$router.push('/register')
      },
    login() {
        this.$refs.loginForm.validate(valid => {
            if (valid) {
            // 构造身份验证详情对象
            const authenticationData = {
                Username: this.loginForm.email,
                Password: this.loginForm.password
            }
            const authenticationDetails = new AuthenticationDetails(authenticationData)

            // 构造用户对象
            const userData = {
                Username: this.loginForm.email,
                Pool: userPool
            }
            const cognitoUser = new CognitoUser(userData)

            // 进行登录验证
            cognitoUser.authenticateUser(authenticationDetails, {
                onSuccess: result => {
                  this.$message({
                            message: 'Login successful.',
                            type: 'success'
                        })
                  const idToken = result.getIdToken().getJwtToken()
                  localStorage.setItem('idToken', idToken)
                  this.$router.push({
                      path: '/'
                    })
                },
                onFailure: err => {
                  if (err.code === 'UserNotConfirmedException') {
                    // 重定向到验证页面
                    this.$router.push({
                      path: '/validateemail',
                      query: { 
                        Username: this.loginForm.email
                      }
                    })
                  } else {
                    this.$message.error(err.message || 'Login failed')
                  }
                }
            })
            } else {
            console.log('Validation failed.')
            return false
            }
        })
    },
    logout() {
    const cognitoUser = userPool.getCurrentUser()
        if (cognitoUser != null) {
            cognitoUser.signOut()
        }
            this.isLoggedIn = false
            this.user = null
        }
    }
}
</script>