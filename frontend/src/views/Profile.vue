<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <div class="bg-white rounded-lg shadow-lg p-8">
      <h1 class="text-3xl font-bold mb-8 text-gray-800 border-b pb-4">个人中心</h1>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- 基本信息卡片 -->
        <div class="bg-gray-50 rounded-xl p-6 shadow-sm">
          <h2 class="text-xl font-semibold mb-6 text-gray-700 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            基本信息
          </h2>
          <div class="space-y-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">邮箱</label>
              <div class="text-gray-900 bg-white px-4 py-2 rounded-md border border-gray-200">
                {{ email }}
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">用户名</label>
              <input
                type="text"
                v-model="username"
                class="text-gray-900 bg-white px-4 py-2 rounded-md border border-gray-200 w-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                @click="updateUsername"
                class="mt-4 w-full bg-blue-500 text-white py-2.5 px-4 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-150"
              >
                保存修改
              </button>
            </div>
          </div>
        </div>

        <!-- 修改密码卡片 -->
        <div class="bg-gray-50 rounded-xl p-6 shadow-sm">
          <h2 class="text-xl font-semibold mb-6 text-gray-700 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            修改密码
          </h2>
          <form @submit.prevent="handlePasswordChange" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">当前密码</label>
              <input
                type="password"
                v-model="passwordForm.current_password"
                class="text-gray-900 bg-white px-4 py-2 rounded-md border border-gray-200 w-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">新密码</label>
              <input
                type="password"
                v-model="passwordForm.new_password"
                class="text-gray-900 bg-white px-4 py-2 rounded-md border border-gray-200 w-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">确认新密码</label>
              <input
                type="password"
                v-model="passwordForm.confirm_password"
                class="text-gray-900 bg-white px-4 py-2 rounded-md border border-gray-200 w-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
            <button
              type="submit"
              class="w-full mt-4 bg-blue-500 text-white py-2.5 px-4 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-150 disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center"
              :disabled="isSubmitting"
            >
              <svg v-if="isSubmitting" class="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ isSubmitting ? '保存中...' : '保存修改' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useUserStatsStore } from '../stores/userStats'
import { toast } from '../utils/toast'

const authStore = useAuthStore()
const statsStore = useUserStatsStore()

const isSubmitting = ref(false)
const email = ref('')
const username = ref('')

const passwordForm = ref({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

// 获取用户信息
async function fetchUserProfile() {
  try {
    await authStore.fetchUser()
    if (authStore.user) {
      email.value = authStore.user.email
      username.value = authStore.user.username
    }
  } catch (error) {
    console.error('Failed to fetch user profile:', error)
  }
}

// 更新用户信息
async function updateUsername() {
  try {
    await authStore.updateProfile({
      username: username.value
    })
    toast.success('用户名修改成功')
  } catch (error) {
    console.error('Failed to update username:', error)
    toast.error('更新用户名失败')
  }
}

async function handlePasswordChange() {
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    toast.error('两次输入的密码不一致')
    return
  }

  isSubmitting.value = true
  try {
    await authStore.updateProfile({
      currentPassword: passwordForm.value.current_password,
      newPassword: passwordForm.value.new_password
    })
    toast.success('密码修改成功')
    passwordForm.value = {
      current_password: '',
      new_password: '',
      confirm_password: ''
    }
  } catch (error) {
    console.error('Failed to change password:', error)
    toast.error('密码修改失败，请重试')
  } finally {
    isSubmitting.value = false
  }
}

// 页面加载时获取用户信息
onMounted(() => {
  fetchUserProfile()
})
</script> 