<template>
    <div style="padding-top: 100px;">
      <el-row>
          <el-col :span="8"></el-col>
          <el-col :span="8">
            <el-card class="card" shadow="hover">
          <div>
            <h1>Validate Email</h1>
          </div>
          <el-form ref="validateForm" :model="validateForm" :rules="validateRules" label-width="80px">
            <el-form-item label="Code" prop="code">
              <el-input v-model="validateForm.code" placeholder="Please enter your code"></el-input>
            </el-form-item>

            <el-row>
              <el-col :span="11">
                <el-button type="info" @click="goBack" style="width: 100%">Back</el-button>
              </el-col>
              <el-col :span="2"></el-col>
              <el-col :span="11">
                <el-button type="primary" @click="sendEmail" style="width: 100%">Resend</el-button>
              </el-col>
             </el-row>
             <el-row style="margin-top: 18px">
                <el-button type="primary" @click="validate" style="width: 100%">Validate</el-button>
             </el-row>
             
          </el-form>
        </el-card>
          </el-col>
          <el-col :span="8"></el-col>
      </el-row>
    
      </div>
    </template>
    
    <script>
    import { CognitoUserPool, CognitoUser  } from 'amazon-cognito-identity-js'
    
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
            Username: '',
          validateForm: {
            code: ''
          },
        }
      },
        created() {
            this.Username = this.$route.query.Username
            // this.sendEmail();
        },
      methods: {
        goBack() {
            this.$router.go(-1)     
        },

        sendEmail() {
            const cognitoUser = new CognitoUser({
                    Username: this.Username,
                    Pool: userPool
                })
                cognitoUser.resendConfirmationCode((err) => {
                    if (err) {
                        console.error(err)
                        this.$message.error(err.message || 'Failed to resend confirmation code')
                    } else {
                        console.log('Confirmation code resent successfully')
                    }
                })
        },
        validate() {
            const cognitoUser = new CognitoUser({
                Username: this.Username,
                Pool: userPool
            })
            cognitoUser.confirmRegistration(this.validateForm.code, true, (err) => {
                if (err) {
                    console.error(err)
                    this.$message.error(err.message || 'Verification code is invalid')
                } else {
                    console.log('Verification code is valid')
                    this.$message({
                            message: 'Verification code is valid.',
                            type: 'success'
                        })
                    // 跳转到登陆页面
                    this.$router.push('/login')
                }
            })
        }
    }
  }
  </script>
