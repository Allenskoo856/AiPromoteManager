import { defineStore } from 'pinia'
import { ref } from 'vue'
import request from '../utils/request'

interface User {
  id: string
  email: string
  username: string
  createdAt: string
  updatedAt: string
}

interface LoginResponse {
  access_token: string
}

interface UserStats {
  prompt_count: number
  category_count: number
  tag_count: number
  share_count: number
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref<User | null>(null)
  const isLoggedIn = ref(!!token.value)

  // 初始化
  async function initialize() {
    if (token.value) {
      try {
        await fetchUser()
      } catch (error) {
        console.error('Failed to initialize auth:', error)
        logout()
      }
    }
  }

  // 登录
  async function login(email: string, password: string) {
    try {
      const formData = new FormData()
      formData.append('username', email)  // OAuth2 使用 username 字段
      formData.append('password', password)
      
      const { data } = await request.post<LoginResponse>('/api/v1/auth/login', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      token.value = data.access_token
      localStorage.setItem('token', token.value)
      isLoggedIn.value = true
      await fetchUser()
      return true
    } catch (error) {
      console.error('Login failed:', error)
      return false
    }
  }

  // 注册
  async function register(data: { email: string; username: string; password: string }) {
    try {
      const { data: responseData } = await request.post<LoginResponse>('/api/v1/auth/register', data)
      token.value = responseData.access_token
      localStorage.setItem('token', token.value)
      isLoggedIn.value = true
      await fetchUser()
      return true
    } catch (error) {
      console.error('Registration failed:', error)
      return false
    }
  }

  // 获取用户信息
  async function fetchUser() {
    try {
      const { data } = await request.get<User>('/api/v1/users/me')
      user.value = data
    } catch (error) {
      console.error('Failed to fetch user:', error)
      logout()
    }
  }

  // 更新用户信息
  async function updateProfile(data: {
    username?: string
    currentPassword?: string
    newPassword?: string
  }) {
    try {
      const { data: responseData } = await request.put<User>('/api/v1/users/me', data)
      user.value = responseData
      return true
    } catch (error) {
      console.error('Failed to update profile:', error)
      throw error
    }
  }

  // 获取用户统计信息
  async function getUserStats() {
    try {
      const { data } = await request.get<UserStats>('/api/v1/users/me/stats')
      return data
    } catch (error) {
      console.error('Failed to get user stats:', error)
      throw error
    }
  }

  // 登出
  function logout() {
    token.value = ''
    user.value = null
    isLoggedIn.value = false
    localStorage.removeItem('token')
  }

  // 初始化
  initialize()

  return {
    token,
    user,
    isLoggedIn,
    login,
    register,
    fetchUser,
    updateProfile,
    getUserStats,
    logout,
  }
}) 