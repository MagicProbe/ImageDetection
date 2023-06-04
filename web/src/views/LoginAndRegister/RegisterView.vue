<template>
    <div style="padding-top: 100px;">
    <el-row>
        <el-col :span="8"></el-col>
        <el-col :span="8">
            <el-card class="card" shadow="hover">
                <div>
                    <h1>Registration</h1>
                </div>
                    <el-form ref="registerForm" :model="registerForm" :rules="registerRules" label-width="160px">
                        <el-form-item label="Email" prop="email">
                            <el-input v-model="registerForm.email" placeholder="Please enter your email"></el-input>
                        </el-form-item>
                        <el-form-item label="Password" prop="password">
                            <el-input type="password" v-model="registerForm.password" placeholder="Please enter your password"></el-input>
                        </el-form-item>
                        <el-form-item label="Confirm Password" prop="confirmPassword">
                            <el-input type="password" v-model="registerForm.confirmPassword" placeholder="Please confirm your password"></el-input>
                        </el-form-item>
                        <el-form-item label="First Name" prop="firstName">
                            <el-input v-model="registerForm.firstName" placeholder="Please enter your first name"></el-input>
                        </el-form-item>
                        <el-form-item label="Last Name" prop="lastName">
                            <el-input v-model="registerForm.lastName" placeholder="Please enter your last name"></el-input>
                        </el-form-item>
                        <el-row>
                            <el-col :span="11">
                                <el-button type="info" @click="toLogin" style="width: 100%">Login</el-button>
                            </el-col>
                            <el-col :span="2"></el-col>
                            <el-col :span="11">
                                <el-button type="primary" @click="register" style="width: 100%">Register</el-button>
                            </el-col>
                        </el-row>
                    </el-form>
            </el-card>
        </el-col>
        <el-col :span="8"></el-col>
    </el-row>
    </div>
  </template>
  
  <script>
  import { CognitoUserPool, CognitoUserAttribute } from 'amazon-cognito-identity-js'
  
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
        user: null,
        registerForm: {
          email: '',
          password: '',
          confirmPassword: '',
          firstName: '',
          lastName: ''
        },
        registerRules: {
          email: [
            { required: true, message: 'Please enter your email', trigger: 'blur' },
            { type: 'email', message: 'Please enter a valid email address', trigger: ['blur', 'change'] }
          ],
          password: [
            { required: true, message: 'Please enter your password', trigger: 'blur' },
            { min: 6, max: 30, message: 'Password length should between 6 and 30 characters', trigger: 'blur'}
          ],
          confirmPassword: [
            { required: true, message: 'Please confirm your password', trigger: 'blur' },
            { validator: this.validateConfirmPassword, trigger: 'blur' }
          ],
          firstName: [
            { required: true, message: 'Please enter your first name', trigger: 'blur' },
          ],
          lastName: [
            { required: true, message: 'Please enter your last name', trigger: 'blur' },
          ]
        }
      }
    },
    methods: {
      validateConfirmPassword(rule, value, callback) {
        if (value !== this.registerForm.password) {
          callback(new Error('Passwords do not match'))
        } else {
          callback()
        }
      },
      toLogin() {
        this.$router.push('/login')
      },
      register(){
        this.$refs.registerForm.validate(valid => {
            if (valid) {
            // 创建 Cognito 用户
                const email = this.registerForm.email
                const password = this.registerForm.password
                const attributeList = [
                    new CognitoUserAttribute({ Name: 'given_name', Value: this.registerForm.firstName }),
                    new CognitoUserAttribute({ Name: 'family_name', Value: this.registerForm.lastName })
                ]
                userPool.signUp(email, password, attributeList, null, (err, result) => {
                    if (err) {
                        console.error(err)
                        this.$message.error(err.message || 'Registration failed')
                    } else {
                        this.$message({
                            message: 'Register successful. A validation email has been send to your email.',
                            type: 'success'
                        })
                        this.$router.push({
                            path: '/validateemail',
                            query: { 
                                Username: this.registerForm.email
                            }
                        })
                        console.log(result)
                    }
                })
            } else {
                console.log('Validation failed.')
                return false
            }
        })
        }
    }
}
</script>