<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 头部区域 -->
    <div class="relative">
      <!-- 主要内容 -->
      <div class="pt-20 pb-16 sm:pt-24 sm:pb-20">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center">
            <h1 class="text-5xl tracking-tight font-extrabold text-gray-900 sm:text-6xl md:text-7xl">
              <span class="block text-primary-600">
                AI Prompt Manager
              </span>
              <span class="block mt-3 text-4xl sm:text-5xl md:text-6xl">
                管理你的 AI 提示词
              </span>
            </h1>
            <p class="mt-6 max-w-2xl mx-auto text-lg text-gray-600 sm:text-xl md:text-2xl">
              一个强大的 AI 提示词管理平台，帮助你组织、分享和优化你的 AI 提示词。
            </p>
            <div class="mt-8 max-w-md mx-auto sm:flex sm:justify-center md:mt-12">
              <div class="rounded-md shadow">
                <router-link
                  to="/prompts"
                  class="w-full flex items-center justify-center px-8 py-3 text-base font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 hover:text-gray-900 border border-gray-200 transition-all duration-200 md:py-4 md:text-lg md:px-10"
                >
                  浏览提示词
                </router-link>
              </div>
              <div class="mt-3 rounded-md shadow sm:mt-0 sm:ml-3">
                <router-link
                  :to="authStore.isLoggedIn ? '/prompts' : '/register'"
                  class="w-full flex items-center justify-center px-8 py-3 text-base font-medium rounded-lg text-white bg-primary-600 hover:bg-primary-700 transition-all duration-200 md:py-4 md:text-lg md:px-10"
                >
                  {{ authStore.isLoggedIn ? '立即体验' : '立即注册' }}
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 特性区域 -->
    <div class="py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h2 class="text-base text-primary-600 font-semibold tracking-wide uppercase">功能特性</h2>
          <p class="mt-2 text-3xl font-extrabold text-gray-900 tracking-tight sm:text-4xl">
            更好的提示词管理方式
          </p>
        </div>

        <div class="mt-16">
          <div class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-12">
            <!-- 特性卡片 -->
            <div v-for="(feature, index) in features" :key="index" 
              class="relative bg-gray-50 p-6 group"
            >
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <component 
                    :is="feature.icon" 
                    class="h-12 w-12 text-primary-600 group-hover:text-primary-700 transition-colors duration-300"
                  />
                </div>
                <div class="ml-4">
                  <h3 class="text-lg font-medium text-gray-900">{{ feature.title }}</h3>
                  <p class="mt-2 text-base text-gray-500">{{ feature.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import {
  DocumentTextIcon,
  TagIcon,
  UserGroupIcon,
  ClockIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()

const features = [
  {
    title: '分类管理',
    description: '支持多级分类，轻松组织你的提示词库。',
    icon: DocumentTextIcon
  },
  {
    title: '标签系统',
    description: '使用标签灵活标记和检索提示词。',
    icon: TagIcon
  },
  {
    title: '分享协作',
    description: '便捷地分享提示词，支持公开和私密分享。',
    icon: UserGroupIcon
  },
  {
    title: '版本控制',
    description: '追踪提示词的修改历史，随时回溯。',
    icon: ClockIcon
  }
]
</script>

<style scoped>
/* 移除之前的渐变动画相关样式 */
</style> 