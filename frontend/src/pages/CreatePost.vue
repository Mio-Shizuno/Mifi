<template>
  <div class="create-post-container">
    <h1>🎨 创建新作品</h1>
    <el-form :model="form">
      <el-form-item label="标题">
        <el-input v-model="form.title" placeholder="给你的作品起个名字" maxlength="100"></el-input>
      </el-form-item>

      <el-form-item label="内容">
        <el-input v-model="form.content" type="textarea" placeholder="分享你的创意..." :rows="6"></el-input>
      </el-form-item>

      <el-form-item label="作品类型">
        <el-select v-model="form.type">
          <el-option label="文字" value="text"></el-option>
          <el-option label="图片" value="image"></el-option>
          <el-option label="混合" value="mixed"></el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="人物标签">
        <el-select v-model="form.characters" multiple placeholder="选择出现的人物">
          <el-option label="主角A" value="主角A"></el-option>
          <el-option label="主角B" value="主角B"></el-option>
          <el-option label="配角C" value="配角C"></el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="上传图片">
        <el-upload
          v-model:file-list="fileList"
          list-type="picture-card"
          :auto-upload="false"
          @change="handleImageChange"
        >
          <template #default>
            <el-icon><Plus /></el-icon>
          </template>
        </el-upload>
      </el-form-item>

      <el-button type="primary" :loading="loading" @click="handleSubmit" style="width: 100%">
        发布作品
      </el-button>
    </el-form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { postsAPI } from '../api'

const router = useRouter()
const loading = ref(false)
const fileList = ref([])
const form = ref({
  title: '',
  content: '',
  type: 'text',
  characters: [],
  images: []
})

const handleImageChange = () => {
  form.value.images = fileList.value.map(f => f.raw)
}

const handleSubmit = async () => {
  if (!form.value.title || !form.value.content) {
    ElMessage.error('请填写标题和内容')
    return
  }

  loading.value = true
  try {
    const formData = new FormData()
    formData.append('title', form.value.title)
    formData.append('content', form.value.content)
    formData.append('type', form.value.type)
    formData.append('characters', JSON.stringify(form.value.characters))

    await postsAPI.createPost(formData)
    ElMessage.success('发布成功')
    router.push('/')
  } catch (err) {
    ElMessage.error(err.response?.data?.message || '发布失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.create-post-container {
  max-width: 600px;
  margin: 0 auto;
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.create-post-container h1 {
  margin-bottom: 24px;
}
</style>