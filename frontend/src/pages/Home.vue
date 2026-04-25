<template>
  <div class="home-container">
    <div class="home-header">
      <h1>✨ 同人创作广场</h1>
      <router-link to="/create-post">
        <el-button type="primary">📝 发布新作品</el-button>
      </router-link>
    </div>
    
    <el-empty v-if="!loading && posts.length === 0" description="暂无帖子"></el-empty>
    <div v-else>
      <el-skeleton v-if="loading" :rows="5" animated></el-skeleton>
      <div v-for="post in posts" :key="post._id" class="post-card">
        <div class="post-header">
          <div class="author-info">
            <img :src="post.author?.avatar || 'https://via.placeholder.com/32'" :alt="post.author?.username" class="avatar">
            <div class="author-details">
              <router-link :to="`/profile/${post.author?._id}`" class="username-link">
                <span class="username">{{ post.author?.username }}</span>
              </router-link>
              <span class="post-time">{{ formatDate(post.createdAt) }}</span>
            </div>
          </div>
          <el-button v-if="isOwnPost(post)" link @click="handleDeletePost(post._id)">
            🗑️
          </el-button>
        </div>
        
        <h3>{{ post.title }}</h3>
        <p class="post-content">{{ post.content }}</p>
        
        <div v-if="post.images && post.images.length" class="post-images">
          <img v-for="(img, i) in post.images" :key="i" :src="img" :alt="post.title" @click="openImageViewer(img)">
        </div>
        
        <div v-if="post.characters && post.characters.length" class="post-tags">
          <span v-for="char in post.characters" :key="char" class="tag">🏷️ {{ char }}</span>
        </div>
        
        <div class="post-actions">
          <el-button link @click="handleLike(post)" :class="{ 'liked': isPostLiked(post._id) }">
            <span :style="{ color: isPostLiked(post._id) ? 'red' : 'inherit' }">❤️ {{ post.likeCount || 0 }}</span>
          </el-button>
          <router-link :to="`/post/${post._id}`">
            <el-button link>💬 {{ post.commentCount || 0 }}</el-button>
          </router-link>
          <router-link :to="`/messages/${post.author?._id}`">
            <el-button link>✉️ 私信</el-button>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()
const posts = ref([])
const loading = ref(true)
const likedPosts = ref(new Set())

const formatDate = (dateString) => {
  if (!dateString) return '未知'
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  return date.toLocaleDateString('zh-CN')
}

const isOwnPost = (post) => {
  const user = JSON.parse(localStorage.getItem('user') || 'null')
  return user && user._id === post.author?._id
}

const isPostLiked = (postId) => {
  return likedPosts.value.has(postId)
}

const handleLike = async (post) => {
  const token = localStorage.getItem('token')
  if (!token) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }

  try {
    const isLiked = isPostLiked(post._id)
    const response = await fetch(`http://localhost:5000/api/posts/${post._id}/like`, {
      method: isLiked ? 'DELETE' : 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    if (response.ok) {
      if (isLiked) {
        likedPosts.value.delete(post._id)
        post.likeCount = (post.likeCount || 1) - 1
      } else {
        likedPosts.value.add(post._id)
        post.likeCount = (post.likeCount || 0) + 1
      }
      ElMessage.success(isLiked ? '已取消点赞' : '点赞成功')
    }
  } catch (err) {
    ElMessage.error('操作失败，请重试')
  }
}

const handleDeletePost = async (postId) => {
  try {
    await ElMessageBox.confirm('确定删除此作品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    const token = localStorage.getItem('token')
    const response = await fetch(`http://localhost:5000/api/posts/${postId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.ok) {
      posts.value = posts.value.filter(p => p._id !== postId)
      ElMessage.success('删除成功')
    }
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const openImageViewer = (imageUrl) => {
  const link = document.createElement('a')
  link.href = imageUrl
  link.target = '_blank'
  link.click()
}

onMounted(async () => {
  try {
    loading.value = true
    const response = await fetch('http://localhost:5000/api/posts/feed', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
      }
    })

    if (response.ok) {
      const data = await response.json()
      posts.value = data.posts || []
      
      // 恢复点赞状态
      const user = JSON.parse(localStorage.getItem('user') || 'null')
      if (user) {
        posts.value.forEach(post => {
          if (post.likedBy && post.likedBy.includes(user._id)) {
            likedPosts.value.add(post._id)
          }
        })
      }
    } else {
      ElMessage.error('加载失败')
    }
  } catch (err) {
    ElMessage.error('加载失败，请检查网络')
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.home-container {
  max-width: 700px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
}

.home-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0f0f0;
}

.home-header h1 {
  margin: 0;
  font-size: 28px;
}

.post-card {
  background: white;
  padding: 20px;
  margin-bottom: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: box-shadow 0.3s ease;
}

.post-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.author-info {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  flex: 1;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.author-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.username-link {
  text-decoration: none;
  color: inherit;
}

.username {
  font-weight: 600;
  color: #333;
}

.username:hover {
  color: #667eea;
}

.post-time {
  font-size: 12px;
  color: #999;
}

.post-card h3 {
  margin: 12px 0 8px 0;
  font-size: 18px;
  color: #333;
}

.post-content {
  margin: 12px 0;
  color: #555;
  line-height: 1.6;
  word-break: break-word;
}

.post-images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 8px;
  margin: 16px 0;
}

.post-images img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 6px;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.post-images img:hover {
  transform: scale(1.02);
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 16px 0;
}

.tag {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.post-actions {
  display: flex;
  gap: 16px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.post-actions :deep(.el-button) {
  padding: 0;
  color: #666;
  transition: color 0.2s ease;
}

.post-actions :deep(.el-button:hover) {
  color: #667eea;
}

.post-actions :deep(.el-button.liked) {
  color: red;
}

.post-actions a {
  text-decoration: none;
}
</style>