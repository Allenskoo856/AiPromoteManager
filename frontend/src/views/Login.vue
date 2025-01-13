<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          登录账号
        </h2>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="email" class="sr-only">邮箱地址</label>
            <input
              id="email"
              v-model="email"
              name="email"
              type="email"
              required
              class="input rounded-t-md w-full"
              placeholder="邮箱地址"
            />
          </div>
          <div>
            <label for="password" class="sr-only">密码</label>
            <input
              id="password"
              v-model="password"
              name="password"
              type="password"
              required
              class="input rounded-b-md w-full"
              placeholder="密码"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            class="btn-primary w-full"
            :disabled="isLoading"
          >
            {{ isLoading ? '登录中...' : '登录' }}
          </button>
        </div>

        <div class="text-sm text-center">
          <router-link
            to="/register"
            class="font-medium text-primary-600 hover:text-primary-500"
          >
            还没有账号？立即注册
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const isLoading = ref(false)

async function handleSubmit() {
  if (isLoading.value) return

  isLoading.value = true
  try {
    const success = await authStore.login(email.value, password.value)
    if (success) {
      router.push('/prompts')
    } else {
      alert('登录失败，请检查邮箱和密码')
    }
  } catch (error) {
    console.error('Login error:', error)
    alert('登录失败，请稍后重试')
  } finally {
    isLoading.value = false
  }
}
</script> 