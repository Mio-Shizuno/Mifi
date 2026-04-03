<template>
  <div class="auth-container">
    <div class="auth-box">
      <h1>🎨 Mifi 同人创作平台</h1>
      <h2>创建账号</h2>
      <el-form :model="form" @submit.prevent="handleRegister">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="输入用户名" minlength="3"></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" placeholder="输入邮箱" type="email"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" placeholder="输入密码" type="password" show-password></el-input>
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input v-model="form.confirmPassword" placeholder="再次输入密码" type="password" show-password></el-input>
        </el-form-item>
        <el-button type="primary" :loading="loading" @click="handleRegister" style="width: 100%">
          注册
        </el-button>
      </el-form>
      <p class="auth-link">
        已有账号？<router-link to="/login">点击登录</router-link>
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
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const handleRegister = async () => {
  if (!form.value.username || !form.value.email || !form.value.password) {
    ElMessage.error('请填写所有字段')
    return
  }

  if (form.value.password !== form.value.confirmPassword) {
    ElMessage.error('两次输入密码不一致')
    return
  }

  if (form.value.password.length < 6) {
    ElMessage.error('密码至少6个字符')
    return
  }

  loading.value = true
  try {
    const { data } = await authAPI.register(
      form.value.username,
      form.value.email,
      form.value.password
    )
    authStore.setAuth(data.user, data.token)
    ElMessage.success('注册成功')
    router.push('/')
  } catch (err) {
    ElMessage.error(err.response?.data?.message || '注册失败')
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