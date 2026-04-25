<template>
  <div class="auth-container">
    <div class="auth-box">
      <div class="auth-header">
        <h1>🎨 Mifi</h1>
        <p class="subtitle">同人创作分享平台</p>
      </div>
      
      <h2>创建账号</h2>
      
      <el-form :model="form" @submit.prevent="handleRegister">
        <el-form-item label="用户名">
          <el-input 
            v-model="form.username" 
            placeholder="输入用户名（3-20个字符）" 
            minlength="3"
            maxlength="20"
            clearable
          ></el-input>
        </el-form-item>
        
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
            placeholder="输入密码（至少6个字符）" 
            type="password" 
            show-password
            minlength="6"
            clearable
          ></el-input>
        </el-form-item>
        
        <el-form-item label="确认密码">
          <el-input 
            v-model="form.confirmPassword" 
            placeholder="再次输入密码" 
            type="password" 
            show-password
            clearable
          ></el-input>
        </el-form-item>
        
        <el-button type="primary" :loading="loading" @click="handleRegister" style="width: 100%; margin-bottom: 16px;">
          {{ loading ? '注册中...' : '注册' }}
        </el-button>
      </el-form>
      
      <div class="auth-footer">
        <span>已有账号？</span>
        <router-link to="/login" class="auth-link">点击登录</router-link>
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
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const handleRegister = async () => {
  // 验证表单
  if (!form.value.username || !form.value.email || !form.value.password) {
    ElMessage.error('请填写所有字段')
    return
  }

  if (form.value.username.length < 3 || form.value.username.length > 20) {
    ElMessage.error('用户名长度应为3-20个字符')
    return
  }

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
    ElMessage.error('邮箱格式不正确')
    return
  }

  if (form.value.password.length < 6) {
    ElMessage.error('密码至少6个字符')
    return
  }

  if (form.value.password !== form.value.confirmPassword) {
    ElMessage.error('两次输入密码不一致')
    return
  }

  loading.value = true
  try {
    const response = await fetch('http://localhost:5000/api/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: form.value.username,
        email: form.value.email,
        password: form.value.password
      })
    })

    const data = await response.json()

    if (response.ok) {
      // 保存用户信息和token
      localStorage.setItem('token', data.token)
      localStorage.setItem('user', JSON.stringify(data.user))
      
      ElMessage.success('注册成功')
      router.push('/')
    } else {
      ElMessage.error(data.message || '注册失败')
    }
  } catch (err) {
    console.error('注册错误:', err)
    ElMessage.error('注册失败，请检查网络连接')
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