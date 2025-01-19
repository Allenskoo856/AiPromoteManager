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
                <div class="relative inline-block text-left">
                  <button
                    type="button"
                    class="inline-flex items-center text-gray-700 hover:text-gray-900 focus:outline-none transition-colors duration-200"
                    @click="showDropdown = !showDropdown"
                  >
                    <span class="font-medium">{{ authStore.user?.username || '个人中心' }}</span>
                    <svg 
                      class="ml-1 h-4 w-4 transition-transform duration-200"
                      :class="{ 'rotate-180': showDropdown }"
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>
                  
                  <!-- 下拉菜单 -->
                  <div
                    v-if="showDropdown"
                    class="origin-top-right absolute right-0 mt-2 min-w-[200px] max-w-sm w-max rounded-lg shadow-xl bg-white ring-1 ring-black ring-opacity-5 divide-y divide-gray-100 transform transition-all duration-200 ease-out z-50"
                  >
                    <!-- 添加小箭头 -->
                    <div class="absolute right-5 -top-2 w-4 h-4 rotate-45 bg-gray-50 border-t border-l border-gray-200"></div>
                    
                    <div class="px-5 py-4 bg-gray-50 rounded-t-lg relative">
                      <p class="text-sm text-gray-900 font-medium break-all">
                        {{ authStore.user?.email }}
                      </p>
                      <p class="text-xs text-gray-500 mt-1.5">
                        {{ authStore.user?.username }}
                      </p>
                    </div>
                    <div class="py-1">
                      <router-link
                        to="/profile"
                        class="group flex items-center px-5 py-3 text-sm text-gray-700 hover:bg-gray-50 transition-colors duration-200"
                        @click="showDropdown = false"
                      >
                        <svg class="mr-3 h-5 w-5 text-gray-400 group-hover:text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                        个人中心
                      </router-link>
                    </div>
                    <div class="py-1">
                      <button
                        class="group flex w-full items-center px-5 py-3 text-sm text-red-600 hover:bg-red-50 transition-colors duration-200"
                        @click="handleLogout"
                      >
                        <svg class="mr-3 h-5 w-5 text-red-400 group-hover:text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                        </svg>
                        退出登录
                      </button>
                    </div>
                  </div>
                </div>
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const showDropdown = ref(false)

const isLoggedIn = computed(() => authStore.isLoggedIn)

// 处理退出登录
const handleLogout = () => {
  authStore.logout()
  router.push('/')
  showDropdown.value = false
}

// 点击外部关闭下拉菜单
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (!target.closest('.relative')) {
    showDropdown.value = false
  }
}

// 添加和移除全局点击事件监听
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
