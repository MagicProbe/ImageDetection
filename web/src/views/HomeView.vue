<template>

<el-header class="page-header centered" height="60px">
    <el-container>
      <el-aside width="auto" class="centered">
        <el-button type="success" @click="uploadImageSync = true">Upload Image</el-button>
      </el-aside>
      <el-aside width="auto" class="centered" style="margin-left: 14px;">
        <el-button type="primary" @click="queryImages">Query All</el-button>
      </el-aside>
      <el-aside width="auto" class="centered" style="margin-left: 14px;">
        <el-button type="primary" @click="queryImagesByTagsSync = true">Query By Tags</el-button>
      </el-aside>
      <el-aside width="auto" class="centered" style="margin-left: 14px;">
        <el-button type="primary" @click="queryImagesByImageSync = true">Query By Image</el-button>
      </el-aside>
      <el-main></el-main>
      <el-aside width="auto" class="centered">
        <el-button type="danger" @click="logout">Logout</el-button>
      </el-aside>
    </el-container>
  </el-header>

  <el-main>
    <el-table v-loading="loading" :data="imageForm">
      <el-table-column label="S3URL" align="center" prop="S3URL" />
      <el-table-column label="name" align="center" prop="name" />
      <el-table-column label="tags" align="center">
        <template #default="{ row }">
          <span v-for="(count, tag) in row.tags" :key="tag">{{ tag }}: {{ count }}&nbsp;&nbsp;</span>
        </template>
      </el-table-column>
      <el-table-column label="operation" align="center" class-name="small-padding fixed-width" fixed="right">
        <template #default="{row}">
          <el-button type="primary" @click="adjustTags(row)">Adjust tags</el-button>
          <el-button type="danger" @click="deleteImage(row)">Delete</el-button>
        </template>
    </el-table-column>
    </el-table>
  </el-main>

  <!-- queryImagesByTags -->
  <el-dialog :title="title" v-model="queryImagesByTagsSync" width="50%" :append-to-body="true" >
    <el-form :model="queryForm" label-width="120px">
      <el-form-item v-for="(tag, index) in queryForm.tags" :key="index" :label="'Tag ' + (index + 1)">
        <el-row>
          <el-col :span="12">
            <el-input v-model="tag.name" placeholder="Tag name"></el-input>
          </el-col>
          <el-col :span="12">
            <el-input-number v-model.number="tag.count" min="1" placeholder="Count"></el-input-number>
          </el-col>
          <el-col :span="2">
            <el-button type="danger" size="small" @click="removeQueryTag(index)">Remove</el-button>
          </el-col>
        </el-row>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="addQueryTag">Add tag</el-button>
      </el-form-item>
    </el-form>
    <el-row style="margin-top: 20px;">
      <el-col :span="11">
        <el-button type="info" @click="queryImagesByTagsSync = false" style="width: 100%">Cancel</el-button>
      </el-col>
      <el-col :span="2"></el-col>
      <el-col :span="11">
        <el-button type="success" @click="queryImagesByTags" style="width: 100%">Query</el-button>
      </el-col>
    </el-row>
  </el-dialog>

  <!-- queryImagesByImage -->
  <el-dialog :title="title" v-model="queryImagesByImageSync" width="50%" :append-to-body="true" >
    <div>
      <input type="file" ref="fileInput" @change="selectImage" accept=".jpeg,.png, .gif,.bmp,.jpg">
      <img v-if="imageUrl" :src="imageUrl" width="200px">
    </div>
    <el-row style="margin-top: 20px;">
      <el-col :span="11">
        <el-button type="info" @click="queryImagesByImageSync = false" style="width: 100%">Cancel</el-button>
      </el-col>
      <el-col :span="2"></el-col>
      <el-col :span="11">
        <el-button type="success" @click="queryImagesByImage" style="width: 100%">Query</el-button>
      </el-col>
    </el-row>
  </el-dialog>

  
  <!-- adjustTags -->
  <el-dialog :title="title" v-model="adjustTagsSync" width="50%" :append-to-body="true" >
    <el-form :model="form" label-width="120px">
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
      </el-form-item>
    </el-form>
    <el-row style="margin-top: 20px;">
      <el-col :span="11">
        <el-button type="info" @click="adjustTagsSync = false"  style="width: 100%">Cancel</el-button>
      </el-col>
      <el-col :span="2"></el-col>
      <el-col :span="11">
        <el-button type="primary" @click="submitData"  style="width: 100%">Submit</el-button>
      </el-col>
    </el-row>
  </el-dialog>

  <!-- uploadImage -->
  <el-dialog :title="title" v-model="uploadImageSync" width="50%" :append-to-body="true" >
    <div>
      <input type="file" ref="fileInput" @change="selectImage" accept=".jpeg,.png, .gif,.bmp,.jpg">
      <img v-if="imageUrl" :src="imageUrl" width="200px">
    </div>
    <el-row style="margin-top: 20px;">
      <el-col :span="11">
        <el-button type="info" @click="uploadImageSync = false" style="width: 100%">Cancel</el-button>
      </el-col>
      <el-col :span="2"></el-col>
      <el-col :span="11">
        <el-button type="success" @click="uploadImage" :disabled="!imageSelected" style="width: 100%">Upload image</el-button>
      </el-col>
    </el-row>
  </el-dialog>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const imageFile = ref({ name: null, value: null })
const queryForm = ref({
  tags: [{ name: '', count: 1 }]
})
const form = ref({
  // allTags: [],
  url: '',
  type: 1,
  tags: [{ name: '', count: 1 }]
})
const imageForm = ref([])
const title = ref('')
const queryImagesByTagsSync = ref(false)
const queryImagesByImageSync = ref(false)
const uploadImageSync = ref(false)
const adjustTagsSync = ref(false)

onBeforeMount(() => {
  queryImages()
})

const queryImages = () => {
  axios.post('https://y728lwojnb.execute-api.us-east-1.amazonaws.com/prod/image/query/all', null, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': localStorage.getItem('idToken')
    }
  }).then(response => {
    console.log(response.data.body)
    // for (const key in response.data.body) {
    //   console.log(`Key: ${key}, Value: ${response.data.body[key]}`)
    // }
    imageForm.value = response.data.body
    console.log(imageForm.value)
    ElMessage({
        message: 'Query successful.',
        type: 'success',
      })
    // response.data.body
  }).catch(error => {
    console.error(error)
    ElMessage({
        message: 'Query failed.',
        type: 'warning',
      })
  })
}

const queryImagesByTags = () => {
  const formData = new FormData()
  formData.append('tags', JSON.stringify(queryForm.value.tags))
  axios.post('https://y728lwojnb.execute-api.us-east-1.amazonaws.com/prod/image/query/bytags', formData, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': localStorage.getItem('idToken')
    }
  }).then(response => {
    console.log(response)
    imageForm.value = response.data.body
    console.log(imageForm.value)
    ElMessage({
        message: 'Query successful.',
        type: 'success',
      })
  }).catch(error => {
    console.error(error)
    ElMessage({
        message: 'Query failed.',
        type: 'warning',
      })
  })
  queryImagesByTagsSync.value = false
}

const queryImagesByImage = () => {
  const formData = new FormData()
  formData.append('name', imageFile.value.name)
  formData.append('value', imageFile.value.value)
  axios.post('https://y728lwojnb.execute-api.us-east-1.amazonaws.com/prod/image/query/byimage', formData, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': localStorage.getItem('idToken')
    }
  }).then(response => {
    console.log(response)
    imageForm.value = response.data.body
      ElMessage({
        message: 'Query successful.',
        type: 'success',
      })
      
  }).catch(error => {
    console.error(error)
    ElMessage.error(error)
    ElMessage({
        message: 'Query failed.',
        type: 'warning',
      })
  })
  queryImagesByImageSync.value = false
}

const deleteImage = (row) => {
  const formData = new FormData()
  formData.append('url', row.S3URL)
  axios.post('https://y728lwojnb.execute-api.us-east-1.amazonaws.com/prod/image/delete', formData, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': localStorage.getItem('idToken')
    }
  }).then(response => {
    console.log(response)
    ElMessage({
        message: 'Delete successful.',
        type: 'success',
      })
      queryImages()
  }).catch(error => {
    console.error(error)
    ElMessage({
        message: 'Delete failed.',
        type: 'warning',
      })
  })
}

const adjustTags = (row) => {
  form.value.url = row.S3URL
  // form.value.allTags = row.tags
  form.value.type = 1,
  form.value.tags = [{ name: '', count: 1 }]
  adjustTagsSync.value = true
}

const selectImage = (event) => {
  const reader = new FileReader()
  reader.readAsDataURL(event.target.files[0])
  reader.onload = () => {
    imageFile.value.value = reader.result.substring(reader.result.indexOf(',') + 1)
  }
  imageFile.value.name = event.target.files[0].name
}

const uploadImage = () => {
  const formData = new FormData()
  formData.append('name', imageFile.value.name)
  formData.append('value', imageFile.value.value)
  axios.post('https://y728lwojnb.execute-api.us-east-1.amazonaws.com/prod/image/upload', formData, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': localStorage.getItem('idToken')
    }
  }).then(response => {
    console.log(response)
    if(response.data.StatusCode !== 400) {
      ElMessage({
        message: 'Upload successful.',
        type: 'success',
      })
      queryImages()
    } else {
      ElMessage.error(response.data.body)
    }
  }).catch(error => {
    console.error(error)
    ElMessage.error(error)
  })
  uploadImageSync.value = false
}

const removeQueryTag = (index) => {
  queryForm.value.tags.splice(index, 1)
}

const addQueryTag = () => {
  queryForm.value.tags.push({ name: '', count: 1 })
}
    const addTag = () => {
      form.value.tags.push({ name: '', count: 1 })
    }

    const removeTag = (index) => {
      form.value.tags.splice(index, 1)
    }

    const submitData = () => {
      // if(form.value.type === 0) {
      //   // console.log(form.value.tags)
      //   for(const tag in form.value.tags) {
      //     const name = form.value.tags[tag]['name']
      //     const count = form.value.tags[tag]['count']
      //     if(!(name in form.value.allTags) || count > form.value.allTags[name]) {
      //       ElMessage.error('Invalide remove parameters')
      //       return
      //     }
      //   }
      // }
      const formData = new FormData()
      formData.append('url', form.value.url)
      formData.append('type', parseInt(form.value.type))
      formData.append('tags', JSON.stringify(form.value.tags))
      axios.post('https://y728lwojnb.execute-api.us-east-1.amazonaws.com/prod/image/updatetags', formData, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': localStorage.getItem('idToken')
        }
      }).then(response => {
        console.log(response)
        if(response.data.StatusCode !== 400) {
          ElMessage({
            message: 'Update successful.',
            type: 'success',
          })
          queryImages()
        } else {
          ElMessage.error(response.data.body)
        }
      }).catch(error => {
        console.error(error)
        ElMessage.error(error)
      })
      adjustTagsSync.value = false

    }

    const logout = () => {
      localStorage.removeItem('idToken')
      ElMessage({
        message: 'Logout successful.',
        type: 'success',
      })
      router.push({path: '/login'})
    }

    const imageSelected = ref(false)
    if (imageFile.value !== null) {
      imageSelected.value = true
    } else {
      imageSelected.value = false
    }

</script>

<style scoped>
.page-header {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 9999;
}
.centered {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>

