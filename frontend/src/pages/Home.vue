<template>
  <div class="home-container">
    <h1>✨ 同人创作广场</h1>
    <el-empty v-if="!loading && posts.length === 0" description="暂无帖子"></el-empty>
    <div v-else>
      <el-skeleton v-if="loading" :rows="5" animated></el-skeleton>
      <div v-for="post in posts" :key="post.id" class="post-card">
        <div class="post-header">
          <div class="author-info">
            <img :src="post.author.avatar" :alt="post.author.username" class="avatar">
            <span class="username">{{ post.author.username }}</span>
          </div>
          <span class="post-time">{{ formatDate(post.createdAt) }}</span>
        </div>
        <h3>{{ post.title }}</h3>
        <p class="post-content">{{ post.content }}</p>
        
        <div v-if="post.images.length" class="post-images">
          <img v-for="(img, i) in post.images" :key="i" :src="img" :alt="post.title">
        </div>
        
        <div v-if="post.characters.length" class="post-tags">
          <span v-for="char in post.characters" :key="char" class="tag">{{ char }}</span>
        </div>
        
        <div class="post-actions">
          <el-button link @click="handleLike(post)">
            <span :style="{ color: post.liked ? 'red' : 'inherit' }">❤️ {{ post.likeCount }}</span>
          </el-button>
          <el-button link>💬 {{ post.commentCount }}</el-button>
          <el-button link>💬 私信</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { postsAPI } from '../api'
import { ElMessage } from 'element-plus'

const posts = ref([])
const loading = ref(true)

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

const handleLike = async (post) => {
  try {
    await postsAPI.updatePost(post.id, { liked: !post.liked })
    post.liked = !post.liked
    post.likeCount += post.liked ? 1 : -1
  } catch (err) {
    ElMessage.error('操作失败')
  }
}

onMounted(async () => {
  try {
    const { data } = await postsAPI.getFeed()
    posts.value = data.posts.map(p => ({ ...p, liked: false }))
  } catch (err) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.home-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.post-card {
  background: white;
  padding: 16px;
  margin-bottom: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}

.username {
  font-weight: bold;
}

.post-time {
  font-size: 12px;
  color: #999;
}

.post-content {
  margin: 12px 0;
}

.post-images {
  display: flex;
  gap: 8px;
  margin: 12px 0;
}

.post-images img {
  max-width: 100%;
  max-height: 300px;
  border-radius: 4px;
}

.post-tags {
  display: flex;
  gap: 8px;
  margin: 12px 0;
}

.tag {
  background: #f0f0f0;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
}

.post-actions {
  display: flex;
  gap: 16px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}
</style>