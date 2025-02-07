<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- 复制成功提示 -->
    <div
      v-if="showCopySuccess"
      class="fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded shadow-lg transition-opacity duration-300"
      :class="{ 'opacity-0': fadeOut }"
    >
      复制成功！
    </div>
    
    <!-- 返回按钮 -->
    <div class="mb-6">
      <BackButton to="/prompts" />
    </div>

    <div v-if="isLoading" class="flex justify-center items-center min-h-[400px]">
      <div class="text-gray-500">加载中...</div>
    </div>

    <template v-else-if="prompt">
      <!-- 头部区域 -->
      <div class="bg-white shadow rounded-lg mb-6">
        <div class="px-6 py-5">
          <div class="flex justify-between items-start">
            <div>
              <h1 class="text-2xl font-bold text-gray-900">{{ prompt.title }}</h1>
              <div class="mt-2 flex items-center text-sm text-gray-500">
                <span>创建于 {{ formatDate(prompt.created_at) }}</span>
                <span class="mx-2">·</span>
                <span>更新于 {{ formatDate(prompt.updated_at) }}</span>
              </div>
            </div>
            <div class="flex space-x-3" v-if="isOwner">
              <router-link
                :to="`/prompts/${promptId}/edit`"
                class="btn-secondary"
              >
                编辑
              </router-link>
              <button
                @click="handleDelete"
                class="btn-danger"
                :disabled="isDeleting"
              >
                {{ isDeleting ? '删除中...' : '删除' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 内容区域 -->
      <div class="bg-white shadow rounded-lg mb-6">
        <div class="px-6 py-5">
          <div class="prose max-w-none">
            <!-- 提示词内容 -->
            <div class="mb-6">
              <h2 class="text-lg font-medium text-gray-900 mb-3">提示词内容</h2>
              <div class="relative">
                <div class="bg-gray-50 rounded-lg p-4">
                  <MdPreview :modelValue="prompt.content || ''" class="prose-sm max-w-none" />
                </div>
                <button
                  class="absolute top-2 right-2 p-2 text-gray-500 hover:text-gray-700 bg-white rounded-md shadow-sm"
                  @click="copyContent"
                  :disabled="isCopying"
                >
                  <span class="sr-only">复制内容</span>
                  <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path v-if="isCopying" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- 分类和标签 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- 分类 -->
              <div>
                <h2 class="text-lg font-medium text-gray-900 mb-2">分类</h2>
                <div class="text-gray-700">
                  {{ prompt.category?.name || '未分类' }}
                </div>
              </div>

              <!-- 标签 -->
              <div>
                <h2 class="text-lg font-medium text-gray-900 mb-2">标签</h2>
                <div class="flex flex-wrap gap-2">
                  <span
                    v-for="tag in prompt.tags"
                    :key="tag.id"
                    class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-100 text-primary-800"
                  >
                    {{ tag.name }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 使用统计 -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-6 py-5">
          <h2 class="text-lg font-medium text-gray-900 mb-4">使用统计</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="bg-gray-50 rounded-lg p-4 text-center">
              <div class="text-2xl font-bold text-gray-900">{{ prompt.usageCount }}</div>
              <div class="text-sm text-gray-500">使用次数</div>
            </div>
            <div class="bg-gray-50 rounded-lg p-4 text-center">
              <div class="text-2xl font-bold text-gray-900">{{ prompt.likeCount }}</div>
              <div class="text-sm text-gray-500">收藏数</div>
            </div>
            <div class="bg-gray-50 rounded-lg p-4 text-center">
              <div class="text-2xl font-bold text-gray-900">{{ prompt.shareCount }}</div>
              <div class="text-sm text-gray-500">分享数</div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <div v-else class="text-center py-12">
      <p class="text-gray-500">提示词不存在或已被删除</p>
      <router-link to="/prompts" class="mt-4 btn-primary inline-block">
        返回列表
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePromptStore } from '../../stores/prompt'
import { useAuthStore } from '../../stores/auth'
import BackButton from '@/components/BackButton.vue'
import type { Prompt } from '../../types'
import { MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/preview.css'

const route = useRoute()
const router = useRouter()
const promptStore = usePromptStore()
const authStore = useAuthStore()

const promptId = ref(route.params.id)
const prompt = ref<Prompt | null>(null)
const isLoading = ref(false)
const isDeleting = ref(false)
const isCopying = ref(false)
const showCopySuccess = ref(false)
const fadeOut = ref(false)

const isOwner = computed(() => {
  if (!prompt.value || !authStore.user) return false
  return Number(prompt.value.owner_id) === Number(authStore.user.id)
})

const loadPrompt = async () => {
  isLoading.value = true
  try {
    const id = Array.isArray(promptId.value) ? promptId.value[0] : promptId.value
    prompt.value = await promptStore.fetchPrompt(Number(id))
  } catch (error) {
    console.error('Failed to fetch prompt:', error)
  } finally {
    isLoading.value = false
  }
}

const handleDelete = async () => {
  if (!prompt.value) return
  if (!confirm('确定要删除这个提示词吗？此操作不可撤销。')) return
  
  isDeleting.value = true
  try {
    await promptStore.deletePrompt(prompt.value.id)
    router.push('/prompts')
  } catch (error) {
    console.error('Failed to delete prompt:', error)
  } finally {
    isDeleting.value = false
  }
}

const formatDate = (date: string | undefined) => {
  if (!date) return ''
  return new Date(date).toLocaleString()
}

onMounted(async () => {
  await loadPrompt()
})

const copyContent = async () => {
  if (!prompt.value?.content) return
  
  isCopying.value = true
  try {
    const textArea = document.createElement('textarea')
    textArea.value = prompt.value.content
    document.body.appendChild(textArea)
    textArea.select()
    const success = document.execCommand('copy')
    document.body.removeChild(textArea)

    if (success) {
      showCopySuccess.value = true
      fadeOut.value = false
      
      // 1.8秒后开始淡出动画
      setTimeout(() => {
        fadeOut.value = true
      }, 1800)
      
      // 2秒后完全隐藏提示
      setTimeout(() => {
        showCopySuccess.value = false
      }, 2000)
    } else {
      console.error('复制失败')
    }
  } catch (error) {
    console.error('复制失败:', error)
  } finally {
    isCopying.value = false
  }
}
</script>