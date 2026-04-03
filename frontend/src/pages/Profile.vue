<template>
  <div class="profile-container" v-if="user">
    <div class="profile-header">
      <img :src="user.avatar" :alt="user.username" class="avatar">
      <div class="user-info">
        <h1>{{ user.username }}</h1>
        <p>{{ user.bio }}</p>
        <div class="stats">
          <span>粉丝: {{ user.followersCount }}</span>
          <span>关注: {{ user.followingCount }}</span>
        </div>
        <el-button v-if="isOtherUser" @click="handleFollow">
          {{ isFollowing ? '取消关注' : '关注' }}
        </el-button>
      </div>
    </div>

    <div class="user-posts">
      <h2>作品</h2>
      <el-empty v-if="posts.length === 0" description="暂无作品"></el-empty>
      <div v-for="post in posts" :key="post.id" class="post-card">
        <h3>{{ post.title }}</h3>
        <p>{{ post.content }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { usersAPI } from '../api'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const authStore = useAuthStore()
const user = ref(null)
const posts = ref([])
const isFollowing = ref(false)

const isOtherUser = computed(() => authStore.user?.id !== route.params.id)

onMounted(async () => {
  try {
    const { data: userData } = await usersAPI.getUser(route.params.id)
    user.value = userData.user
    
    const { data: postsData } = await usersAPI.getUserPosts(route.params.id)
    posts.value = postsData.posts
  } catch (err) {
    console.error('加载失败', err)
  }
})

const handleFollow = async () => {
  try {
    if (isFollowing.value) {
      await usersAPI.unfollow(route.params.id)
    } else {
      await usersAPI.follow(route.params.id)
    }
    isFollowing.value = !isFollowing.value
  } catch (err) {
    console.error('操作失败', err)
  }
}
</script>

<style scoped>
.profile-container {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.profile-header {
  display: flex;
  gap: 20px;
  padding: 24px;
  border-bottom: 1px solid #f0f0f0;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}

.user-info {
  flex: 1;
}

.stats {
  display: flex;
  gap: 20px;
  margin: 10px 0;
  color: #666;
}

.user-posts {
  padding: 24px;
}

.post-card {
  padding: 16px;
  margin-bottom: 16px;
  background: #f5f5f5;
  border-radius: 4px;
}

.post-card h3 {
  margin-bottom: 8px;
}

.post-card p {
  color: #666;
}
</style>