<template>
  <div class="min-h-screen">
    <!-- 导航栏 -->
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <!-- Logo -->
            <div class="flex-shrink-0 flex items-center">
              <router-link to="/" class="text-xl font-bold text-primary-600">
                AI Prompt Manager
              </router-link>
            </div>
            <!-- 导航链接 -->
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8" v-if="isLoggedIn">
              <router-link
                to="/prompts"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="[
                  $route.path.startsWith('/prompts')
                    ? 'border-primary-500 text-gray-900'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                ]"
              >
                提示词
              </router-link>
              <router-link
                to="/categories"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="[
                  $route.path.startsWith('/categories')
                    ? 'border-primary-500 text-gray-900'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                ]"
              >
                分类
              </router-link>
              <router-link
                to="/tags"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="[
                  $route.path.startsWith('/tags')
                    ? 'border-primary-500 text-gray-900'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                ]"
              >
                标签
              </router-link>
            </div>
          </div>
          <!-- 用户菜单 -->
          <div class="flex items-center">
            <template v-if="isLoggedIn">
              <router-link
                to="/prompts/create"
                class="btn-primary mr-4"
              >
                创建提示词
              </router-link>
              <div class="ml-3 relative">
                <router-link
                  to="/profile"
                  class="text-gray-500 hover:text-gray-700"
                >
                  {{ authStore.user?.username || '个人中心' }}
                </router-link>
              </div>
            </template>
            <template v-else>
              <router-link
                to="/login"
                class="btn-secondary mr-2"
              >
                登录
              </router-link>
              <router-link
                to="/register"
                class="btn-primary"
              >
                注册
              </router-link>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主要内容 -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const isLoggedIn = computed(() => authStore.isLoggedIn)
</script>
