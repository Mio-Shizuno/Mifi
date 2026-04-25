<template>
  <div class="profile-container" v-if="user">
    <div class="profile-header">
      <img :src="user.avatar || 'https://via.placeholder.com/100'" :alt="user.username" class="avatar">
      <div class="user-info">
        <h1>{{ user.username }}</h1>
        <p class="bio">{{ user.bio || '这个用户很懒，什么都没留下...' }}</p>
        <div class="stats">
          <span><strong>{{ posts.length }}</strong> 作品</span>
          <span><strong>{{ user.followersCount || 0 }}</strong> 粉丝</span>
          <span><strong>{{ user.followingCount || 0 }}</strong> 关注</span>
        </div>
        <div class="actions" v-if="isOtherUser">
          <el-button type="primary" @click="handleFollow">
            {{ isFollowing ? '✓ 已关注' : '+ 关注' }}
          </el-button>
          <router-link :to="`/messages/${user._id}`">
            <el-button>💬 私信</el-button>
          </router-link>
        </div>
        <div class="actions" v-else>
          <router-link to="/create-post">
            <el-button type="primary">📝 发布新作品</el-button>
          </router-link>
          <el-button @click="handleEditProfile">⚙️ 编辑资料</el-button>
        </div>
      </div>
    </div>

    <div class="user-posts">
      <h2>📚 我的作品</h2>
      <el-empty v-if="posts.length === 0" description="暂无作品"></el-empty>
      <div v-else class="posts-grid">
        <div v-for="post in posts" :key="post._id" class="post-item">
          <router-link :to="`/post/${post._id}`">
            <div class="post-thumbnail">
              <img v-if="post.images && post.images.length" :src="post.images[0]" :alt="post.title" class="thumbnail-img">
              <div v-else class="placeholder">📝</div>
            </div>
          </router-link>
          <div class="post-info">
            <h3>{{ post.title }}</h3>
            <p class="post-preview">{{ post.content.substring(0, 50) }}{{ post.content.length > 50 ? '...' : '' }}</p>
            <div class="post-meta">
              <span class="post-date">{{ formatDate(post.createdAt) }}</span>
              <span class="post-stats">❤️ {{ post.likeCount || 0 }} | 💬 {{ post.commentCount || 0 }}</span>
            </div>
            <div v-if="isCurrentUser" class="post-actions">
              <el-button link type="danger" @click="handleDeletePost(post._id)">🗑️ 删除</el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <el-empty v-else description="用户不存在"></el-empty>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const user = ref(null)
const posts = ref([])
const isFollowing = ref(false)

const currentUser = computed(() => {
  const user = localStorage.getItem('user')
  return user ? JSON.parse(user) : null
})

const isCurrentUser = computed(() => {
  return currentUser.value && currentUser.value._id === user.value?._id
})

const isOtherUser = computed(() => {
  return currentUser.value && currentUser.value._id !== user.value?._id
})

const formatDate = (dateString) => {
  if (!dateString) return '未知'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

const handleFollow = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    ElMessage.warning('请先登录')
    return
  }

  try {
    const url = `http://localhost:5000/api/users/${user.value._id}/${isFollowing.value ? 'unfollow' : 'follow'}`
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.ok) {
      isFollowing.value = !isFollowing.value
      user.value.followersCount = (user.value.followersCount || 0) + (isFollowing.value ? 1 : -1)
      ElMessage.success(isFollowing.value ? '已关注' : '已取消关注')
    }
  } catch (err) {
    ElMessage.error('操作失败')
  }
}

const handleEditProfile = () => {
  ElMessage.info('编辑资料功能开发中...')
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

onMounted(async () => {
  try {
    const userId = route.params.userId
    
    // 获取用户信息
    const userResponse = await fetch(`http://localhost:5000/api/users/${userId}`)
    if (userResponse.ok) {
      const userData = await userResponse.json()
      user.value = userData.user
    } else {
      ElMessage.error('用户不存在')
      return
    }

    // 获取用户作品
    const postsResponse = await fetch(`http://localhost:5000/api/users/${userId}/posts`)
    if (postsResponse.ok) {
      const postsData = await postsResponse.json()
      posts.value = postsData.posts || []
    }

    // 检查是否已关注
    const token = localStorage.getItem('token')
    if (token && isOtherUser.value) {
      const followResponse = await fetch(`http://localhost:5000/api/users/${userId}/is-following`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      if (followResponse.ok) {
        const followData = await followResponse.json()
        isFollowing.value = followData.isFollowing
      }
    }
  } catch (err) {
    ElMessage.error('加载失败')
    console.error(err)
  }
})
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  min-height: 100vh;
}

.profile-header {
  display: flex;
  gap: 24px;
  margin-bottom: 40px;
  padding-bottom: 24px;
  border-bottom: 2px solid #f0f0f0;
}

.avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
}

.user-info h1 {
  margin: 0 0 8px 0;
  font-size: 24px;
  color: #333;
}

.bio {
  margin: 0 0 16px 0;
  color: #666;
  font-size: 14px;
}

.stats {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
  color: #666;
}

.stats span {
  font-size: 14px;
}

.stats strong {
  color: #333;
  font-size: 16px;
}

.actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.actions a {
  text-decoration: none;
}

.user-posts {
  margin-top: 32px;
}

.user-posts h2 {
  margin: 0 0 20px 0;
  font-size: 20px;
  color: #333;
  padding-bottom: 12px;
  border-bottom: 2px solid #667eea;
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.post-item {
  border-radius: 8px;
  overflow: hidden;
  background: #f9f9f9;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.post-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.post-thumbnail {
  width: 100%;
  height: 150px;
  overflow: hidden;
  background: #f0f0f0;
}

.post-thumbnail a {
  display: block;
  width: 100%;
  height: 100%;
  text-decoration: none;
}

.thumbnail-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
}

.post-info {
  padding: 12px;
}

.post-info h3 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.post-preview {
  margin: 0 0 8px 0;
  font-size: 12px;
  color: #999;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
  margin-top: 8px;
}

.post-actions {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #e0e0e0;
}

.post-actions :deep(.el-button) {
  padding: 0;
  font-size: 12px;
}
</style>