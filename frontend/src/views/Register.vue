<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          注册账号
        </h2>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="email" class="sr-only">邮箱地址</label>
            <input
              id="email"
              v-model="form.email"
              name="email"
              type="email"
              required
              class="input rounded-t-md w-full"
              placeholder="邮箱地址"
              :disabled="isSubmitting"
            />
          </div>
          <div>
            <label for="username" class="sr-only">用户名</label>
            <input
              id="username"
              v-model="form.username"
              name="username"
              type="text"
              required
              class="input w-full"
              placeholder="用户名"
              :disabled="isSubmitting"
            />
          </div>
          <div>
            <label for="password" class="sr-only">密码</label>
            <input
              id="password"
              v-model="form.password"
              name="password"
              type="password"
              required
              class="input w-full"
              placeholder="密码"
              :disabled="isSubmitting"
            />
          </div>
          <div>
            <label for="confirmPassword" class="sr-only">确认密码</label>
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              name="confirmPassword"
              type="password"
              required
              class="input rounded-b-md w-full"
              placeholder="确认密码"
              :disabled="isSubmitting"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            class="btn-primary w-full"
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? '注册中...' : '注册' }}
          </button>
        </div>

        <div class="text-sm text-center">
          <router-link
            to="/login"
            class="font-medium text-primary-600 hover:text-primary-500"
          >
            已有账号？立即登录
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

const isSubmitting = ref(false)
const form = ref({
  email: '',
  username: '',
  password: '',
  confirmPassword: ''
})

async function handleSubmit() {
  if (isSubmitting.value) return

  // 验证密码
  if (form.value.password !== form.value.confirmPassword) {
    alert('两次输入的密码不一致')
    return
  }

  isSubmitting.value = true
  try {
    const success = await authStore.register({
      email: form.value.email,
      username: form.value.username,
      password: form.value.password
    })
    
    if (success) {
      router.push('/prompts')
    }
  } catch (error) {
    console.error('Registration error:', error)
    alert('注册失败，请稍后重试')
  } finally {
    isSubmitting.value = false
  }
}
</script> 