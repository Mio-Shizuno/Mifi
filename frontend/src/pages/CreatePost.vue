<template>
  <div class="create-post-container">
    <div class="create-post-header">
      <h1>🎨 创建新作品</h1>
      <p class="subtitle">分享你的同人创意</p>
    </div>

    <el-form :model="form" class="post-form" @submit.prevent="handleSubmit">
      <el-form-item label="作品标题 *">
        <el-input 
          v-model="form.title" 
          placeholder="给你的作品起个名字" 
          maxlength="100"
          show-word-limit
          clearable
        ></el-input>
      </el-form-item>

      <el-form-item label="作品内容 *">
        <el-input 
          v-model="form.content" 
          type="textarea" 
          placeholder="分享你的创意..." 
          :rows="6"
          maxlength="5000"
          show-word-limit
        ></el-input>
      </el-form-item>

      <el-form-item label="作品类型">
        <el-select v-model="form.type" placeholder="选择作品类型">
          <el-option label="📝 纯文字" value="text"></el-option>
          <el-option label="🖼️ 图片作品" value="image"></el-option>
          <el-option label="🎨 文字+图片" value="mixed"></el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="人物标签">
        <el-select 
          v-model="form.characters" 
          multiple 
          placeholder="选择出现的人物或角色"
          collapse-tags
        >
          <el-option label="主角A" value="主角A"></el-option>
          <el-option label="主角B" value="主角B"></el-option>
          <el-option label="配角C" value="配角C"></el-option>
          <el-option label="反派D" value="反派D"></el-option>
          <el-option label="女主" value="女主"></el-option>
          <el-option label="男主" value="男主"></el-option>
          <el-option label="其他" value="其他"></el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="添加标签">
        <el-input 
          v-model="tagInput" 
          placeholder="输入标签，按Enter添加"
          @keyup.enter="addTag"
          clearable
        >
          <template #append>
            <el-button @click="addTag">添加</el-button>
          </template>
        </el-input>
        <div class="tags-display" v-if="form.tags && form.tags.length">
          <el-tag 
            v-for="tag in form.tags" 
            :key="tag" 
            closable 
            @close="removeTag(tag)"
            style="margin-right: 8px; margin-top: 8px;"
          >
            {{ tag }}
          </el-tag>
        </div>
      </el-form-item>

      <el-form-item label="上传图片">
        <el-upload
          v-model:file-list="fileList"
          list-type="picture-card"
          :auto-upload="false"
          @change="handleImageChange"
          multiple
          accept="image/*"
        >
          <template #default>
            <el-icon style="font-size: 28px; color: #8c939d;"><Plus /></el-icon>
          </template>
          <template #file="{ file }">
            <div style="position: relative;">
              <img :src="file.url" alt="preview" style="width: 100%; height: 100%; object-fit: cover;" />
              <span class="el-upload-list__item-actions" style="position: absolute; right: 0; top: 0;">
                <span class="el-upload-list__item-delete" @click.stop="removeFile(file)">
                  <el-icon><Delete /></el-icon>
                </span>
              </span>
            </div>
          </template>
        </el-upload>
      </el-form-item>

      <div class="form-actions">
        <el-button type="primary" :loading="loading" @click="handleSubmit" size="large">
          {{ loading ? '发布中...' : '🚀 发布作品' }}
        </el-button>
        <router-link to="/">
          <el-button @click="resetForm" size="large">取消</el-button>
        </router-link>
      </div>
    </el-form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus, Delete } from '@element-plus/icons-vue'

const router = useRouter()
const loading = ref(false)
const fileList = ref([])
const tagInput = ref('')
const form = ref({
  title: '',
  content: '',
  type: 'mixed',
  characters: [],
  tags: [],
  images: []
})

const handleImageChange = () => {
  form.value.images = fileList.value.map(f => f.raw || f)
}

const removeFile = (file) => {
  const index = fileList.value.findIndex(f => f === file)
  if (index > -1) {
    fileList.value.splice(index, 1)
    handleImageChange()
  }
}

const addTag = () => {
  if (tagInput.value.trim()) {
    if (!form.value.tags) {
      form.value.tags = []
    }
    if (!form.value.tags.includes(tagInput.value.trim())) {
      form.value.tags.push(tagInput.value.trim())
    }
    tagInput.value = ''
  }
}

const removeTag = (tag) => {
  form.value.tags = form.value.tags.filter(t => t !== tag)
}

const resetForm = () => {
  form.value = {
    title: '',
    content: '',
    type: 'mixed',
    characters: [],
    tags: [],
    images: []
  }
  fileList.value = []
}

const handleSubmit = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    ElMessage.error('请先登录')
    router.push('/login')
    return
  }

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
    formData.append('tags', JSON.stringify(form.value.tags || []))

    // 添加图片
    form.value.images.forEach((image, index) => {
      if (image instanceof File) {
        formData.append('images', image)
      }
    })

    const response = await fetch('http://localhost:5000/api/posts', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    })

    const data = await response.json()

    if (response.ok) {
      ElMessage.success('发布成功')
      resetForm()
      router.push('/')
    } else {
      ElMessage.error(data.message || '发布失败')
    }
  } catch (err) {
    console.error('发布错误:', err)
    ElMessage.error('发布失败，请检查网络连接')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.create-post-container {
  max-width: 700px;
  margin: 0 auto;
  background: white;
  padding: 32px;
  border-radius: 8px;
  min-height: 100vh;
}

.create-post-header {
  text-align: center;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 2px solid #f0f0f0;
}

.create-post-header h1 {
  margin: 0 0 8px 0;
  font-size: 28px;
  color: #333;
}

.subtitle {
  margin: 0;
  color: #999;
  font-size: 14px;
}

.post-form {
  margin-top: 24px;
}

.tags-display {
  margin-top: 8px;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
}

.form-actions a {
  text-decoration: none;
}

.form-actions a .el-button {
  flex: 1;
}

.form-actions .el-button {
  flex: 1;
}

:deep(.el-input) {
  margin-bottom: 4px;
}

:deep(.el-form-item__label) {
  color: #333;
  font-weight: 500;
}

:deep(.el-upload-list__item) {
  border-radius: 4px;
}
</style>