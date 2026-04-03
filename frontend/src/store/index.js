import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const api = axios.create({
  baseURL: 'http://localhost:5000/api'
})

api.interceptors.request.use(config => {
  const authStore = useAuthStore()
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  return config
})

export const authAPI = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (username, email, password) => api.post('/auth/register', { username, email, password })
}

export const postsAPI = {
  getFeed: (page = 1) => api.get(`/posts/feed?page=${page}`),
  getPost: (id) => api.get(`/posts/${id}`),
  createPost: (data) => api.post('/posts', data),
  updatePost: (id, data) => api.put(`/posts/${id}`, data),
  deletePost: (id) => api.delete(`/posts/${id}`)
}

export const usersAPI = {
  getUser: (id) => api.get(`/users/${id}`),
  getUserPosts: (id, page = 1) => api.get(`/users/${id}/posts?page=${page}`),
  updateProfile: (data) => api.put('/users', data),
  follow: (id) => api.post(`/users/${id}/follow`),
  unfollow: (id) => api.post(`/users/${id}/unfollow`)
}

export const commentsAPI = {
  createComment: (postId, content) => api.post('/comments', { postId, content }),
  deleteComment: (id) => api.delete(`/comments/${id}`)
}

export const messagesAPI = {
  sendMessage: (recipientId, content) => api.post('/messages', { recipientId, content }),
  getConversations: () => api.get('/messages/conversations'),
  getMessages: (userId) => api.get(`/messages/${userId}`)
}

export default api