<template>
  <!-- <div>
        <input type="file" @change="funHander($event)" 
         ref="fileinput"  accept=".jpeg,.png, .gif,.bmp,.jpg">
    </div> -->
  <div>
    <input type="file" ref="fileInput" @change="selectImage" accept=".jpeg,.png, .gif,.bmp,.jpg">
    <button @click="uploadImage" :disabled="!imageSelected">Upload image</button>
    <img v-if="imageUrl" :src="imageUrl" width="200px">
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'

export default {
  name: 'UploadImage',
  setup() {
    const imageFile = ref({ name: null, value: null })

    const selectImage = (event) => {
      const reader = new FileReader()
      reader.readAsDataURL(event.target.files[0])
      reader.onload = () => {
        // console.log(reader.result.substring(reader.result.indexOf(',') + 1))
        imageFile.value.value = reader.result.substring(reader.result.indexOf(',') + 1)
      }
      // imageFile.value.value = Buffer.from(event.target.files[0]).toString('base64');
      imageFile.value.name = event.target.files[0].name
      // console.log(imageFile.value.value)
    }

    const uploadImage = () => {
      const formData = new FormData()
      // formData.append('image', imageFile.value)
      formData.append('name', imageFile.value.name)
      formData.append('value', imageFile.value.value)
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
    }

    return {
      imageFile,
      selectImage,
      uploadImage
    }
  },
  computed: {
    imageSelected() {
      return this.imageFile !== null
    }
  }
}
</script>