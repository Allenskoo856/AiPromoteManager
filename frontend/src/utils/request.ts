import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import router from '../router'

// 创建 axios 实例
const request = axios.create({
  baseURL: import.meta.env.DEV ? 'http://localhost:8000' : '/',
  timeout: 15000,
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response
      
      // 处理 401 未授权错误
      if (status === 401) {
        const authStore = useAuthStore()
        authStore.logout()
        router.push('/login')
      }
      
      // 显示错误信息
      const message = data.detail || '请求失败'
      console.error(message)
      throw new Error(message)
    }
    return Promise.reject(error)
  }
)

export default request