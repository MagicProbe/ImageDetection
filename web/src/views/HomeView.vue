<template>

  <div>
    <input type="file" ref="fileInput" @change="selectImage" accept=".jpeg,.png, .gif,.bmp,.jpg">
    <button @click="uploadImage" :disabled="!imageSelected">Upload image</button>
    <img v-if="imageUrl" :src="imageUrl" width="200px">
  </div>

  <div>
    <el-form :model="form" label-width="120px">
      <el-form-item label="S3 URL">
        <el-input v-model="form.url"></el-input>
      </el-form-item>
      <el-form-item label="Type">
        <el-radio-group v-model="form.type">
          <el-radio :label="1">Add</el-radio>
          <el-radio :label="0">Remove</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item v-for="(tag, index) in form.tags" :key="index" :label="'Tag ' + (index + 1)">
        <el-row>
          <el-col :span="12">
            <el-input v-model="tag.name" placeholder="Tag name"></el-input>
          </el-col>
          <el-col :span="12">
            <el-input-number v-model.number="tag.count" min="1" placeholder="Count"></el-input-number>
          </el-col>
          <el-col :span="2">
            <el-button type="danger" size="small" @click="removeTag(index)">Remove</el-button>
          </el-col>
        </el-row>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="addTag">Add tag</el-button>
        <el-button type="primary" @click="submitData">Submit</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'

export default {
  name: 'UploadImage',
  data() {
    return {
      imageFile: ref({ name: null, value: null }),
      form: {
        url: '',
        type: 1,
        tags: [{ name: '', count: 1 }]
      }
    }
  },

  methods: {
    selectImage(event) {
      const reader = new FileReader()
      reader.readAsDataURL(event.target.files[0])
      reader.onload = () => {
        // console.log(reader.result.substring(reader.result.indexOf(',') + 1))
        this.imageFile.value.value = reader.result.substring(reader.result.indexOf(',') + 1)
      }
      // imageFile.value.value = Buffer.from(event.target.files[0]).toString('base64');
      this.imageFile.value.name = event.target.files[0].name
      // console.log(imageFile.value.value)
    },

    uploadImage() {
      const formData = new FormData()
      // formData.append('image', imageFile.value)
      formData.append('name', this.imageFile.value.name)
      formData.append('value', this.imageFile.value.value)
      console.log(formData)
      axios.post('https://y728lwojnb.execute-api.us-east-1.amazonaws.com/prod/image/upload', formData, {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(response => {
        console.log(response)
        // imageUrl.value = response.data.url
      }).catch(error => {
        console.error(error)
      })
    },

    addTag() {
      this.form.tags.push({ name: '', count: 1 })
    },

    removeTag(index) {
      this.form.tags.splice(index, 1)
    },

    submitData() {
      const data = {
        url: this.form.url,
        type: this.form.type,
        tags: this.form.tags.filter(tag => tag.name !== '' && tag.count > 0)
                            .map(tag => ({ tag: tag.name, count: tag.count }))
      }
      this.$http.post('/api/endpoint', data)
        .then(response => {
          console.log('Data submitted successfully', response.data)
        })
        .catch(error => {
          console.error('Error submitting data', error)
        })
    }
  },

  computed: {
    imageSelected() {
      return this.imageFile !== null
    }
  }
}
</script>