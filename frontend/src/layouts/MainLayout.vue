<template>
  <div class="main-layout">
    <el-container>
      <el-aside width="200px" class="sidebar">
        <div class="logo">🎨 Mifi</div>
        <el-menu :default-active="activeMenu" router>
          <el-menu-item index="/" @click="router.push('/')">
            <span>🏠 首页</span>
          </el-menu-item>
          <el-menu-item index="/create" @click="router.push('/create')">
            <span>✏️ 创建</span>
          </el-menu-item>
          <el-menu-item index="/messages" @click="router.push('/messages')">
            <span>💬 私信</span>
          </el-menu-item>
          <el-menu-item :index="`/profile/${authStore.user?.id}`" @click="router.push(`/profile/${authStore.user?.id}`)">
            <span>👤 个人中心</span>
          </el-menu-item>
        </el-menu>
        <el-button type="danger" @click="handleLogout" style="width: 90%; margin-top: 20px">
          退出登录
        </el-button>
      </el-aside>

      <el-container>
        <el-header class="header">
          <span>欢迎, {{ authStore.user?.username }}</span>
        </el-header>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const activeMenu = computed(() => route.path)

const handleLogout = () => {
  authStore.clearAuth()
  router.push('/login')
}
</script>

<style scoped>
.main-layout {
  height: 100vh;
}

.sidebar {
  background-color: #f5f5f5;
  border-right: 1px solid #e0e0e0;
}

.logo {
  padding: 16px;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  border-bottom: 1px solid #e0e0e0;
}

.header {
  background-color: white;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
}
</style>