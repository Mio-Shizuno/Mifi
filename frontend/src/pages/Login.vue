<template>
  <div class="auth-container">
    <div class="auth-box">
      <div class="auth-header">
        <h1>🎨 Mifi</h1>
        <p class="subtitle">同人创作分享平台</p>
      </div>
      
      <h2>登录账号</h2>
      
      <el-form :model="form" @submit.prevent="handleLogin">
        <el-form-item label="邮箱">
          <el-input 
            v-model="form.email" 
            placeholder="输入邮箱" 
            type="email"
            clearable
          ></el-input>
        </el-form-item>
        
        <el-form-item label="密码">
          <el-input 
            v-model="form.password" 
            placeholder="输入密码" 
            type="password" 
            show-password
            clearable
          ></el-input>
        </el-form-item>
        
        <el-button type="primary" :loading="loading" @click="handleLogin" style="width: 100%; margin-bottom: 16px;">
          {{ loading ? '登录中...' : '登录' }}
        </el-button>
      </el-form>
      
      <div class="auth-footer">
        <span>还没有账号？</span>
        <router-link to="/register" class="auth-link">点击注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
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

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
    ElMessage.error('邮箱格式不正确')
    return
  }

  loading.value = true
  try {
    const response = await fetch('http://localhost:5000/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: form.value.email,
        password: form.value.password
      })
    })

    const data = await response.json()

    if (response.ok) {
      // 保存用户信息和token
      localStorage.setItem('token', data.token)
      localStorage.setItem('user', JSON.stringify(data.user))
      
      ElMessage.success('登录成功')
      router.push('/')
    } else {
      ElMessage.error(data.message || '登录失败')
    }
  } catch (err) {
    console.error('登录错误:', err)
    ElMessage.error('登录失败，请检查网络连接')
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
  padding: 20px;
}

.auth-box {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.auth-header h1 {
  margin: 0;
  font-size: 36px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  margin: 8px 0 0 0;
  color: #666;
  font-size: 14px;
}

.auth-box h2 {
  text-align: center;
  margin: 0 0 24px 0;
  font-size: 18px;
  color: #333;
}

.auth-footer {
  text-align: center;
  margin-top: 20px;
  color: #666;
  font-size: 14px;
}

.auth-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  cursor: pointer;
  transition: color 0.2s ease;
}

.auth-link:hover {
  color: #764ba2;
}

:deep(.el-input) {
  margin-bottom: 8px;
}

:deep(.el-form-item__label) {
  color: #333;
  font-weight: 500;
}
</style>