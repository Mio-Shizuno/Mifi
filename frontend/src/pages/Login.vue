<template>
  <div class="auth-container">
    <div class="auth-box">
      <h1>🎨 Mifi 同人创作平台</h1>
      <h2>登录账号</h2>
      <el-form :model="form" @submit.prevent="handleLogin">
        <el-form-item label="邮箱">
          <el-input v-model="form.email" placeholder="输入邮箱" type="email"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" placeholder="输入密码" type="password" show-password></el-input>
        </el-form-item>
        <el-button type="primary" :loading="loading" @click="handleLogin" style="width: 100%">
          登录
        </el-button>
      </el-form>
      <p class="auth-link">
        还没有账号？<router-link to="/register">点击注册</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { authAPI } from '../api'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(false)
const form = ref({
  email: '',
  password: ''
})

const handleLogin = async () => {
  if (!form.value.email || !form.value.password) {
    ElMessage.error('请输入邮箱和密码')
    return
  }

  loading.value = true
  try {
    const { data } = await authAPI.login(form.value.email, form.value.password)
    authStore.setAuth(data.user, data.token)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (err) {
    ElMessage.error(err.response?.data?.message || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.auth-box {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.auth-box h1 {
  text-align: center;
  margin-bottom: 10px;
  font-size: 28px;
}

.auth-box h2 {
  text-align: center;
  margin-bottom: 24px;
  font-size: 18px;
  color: #666;
}

.auth-link {
  text-align: center;
  margin-top: 16px;
  color: #666;
}

.auth-link a {
  color: #667eea;
  text-decoration: none;
}
</style>