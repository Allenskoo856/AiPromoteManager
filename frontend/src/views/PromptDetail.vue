<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div v-if="isLoading" class="flex justify-center items-center min-h-[400px]">
      <div class="text-gray-500">加载中...</div>
    </div>

    <div v-else-if="prompt" class="bg-white shadow rounded-lg">
      <!-- 头部区域 -->
      <div class="px-6 py-5 border-b border-gray-200">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold text-gray-900">{{ prompt.title }}</h1>
          <div class="flex space-x-3" v-if="isOwner">
            <button 
              @click="handleEdit" 
              class="btn-secondary"
            >
              编辑
            </button>
            <button 
              @click="handleDelete" 
              class="btn-danger"
            >
              删除
            </button>
          </div>
        </div>
        <div class="mt-2 flex items-center text-sm text-gray-500">
          <span>创建于 {{ formatDate(prompt.createdAt) }}</span>
          <span class="mx-2">·</span>
          <span>更新于 {{ formatDate(prompt.updatedAt) }}</span>
        </div>
      </div>

      <!-- 内容区域 -->
      <div class="px-6 py-5">
        <div class="prose max-w-none">
          <div class="mb-6">
            <h3 class="text-lg font-medium text-gray-900 mb-2">提示词内容</h3>
            <div class="bg-gray-50 rounded-lg p-4 font-mono whitespace-pre-wrap">
              {{ prompt.content }}
            </div>
          </div>

          <!-- 标签 -->
          <div class="mb-6">
            <h3 class="text-lg font-medium text-gray-900 mb-2">标签</h3>
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

          <!-- 分类 -->
          <div class="mb-6">
            <h3 class="text-lg font-medium text-gray-900 mb-2">分类</h3>
            <div class="text-gray-700">
              {{ prompt.category?.name || '未分类' }}
            </div>
          </div>

          <!-- 使用统计 -->
          <div class="mb-6">
            <h3 class="text-lg font-medium text-gray-900 mb-2">使用统计</h3>
            <div class="grid grid-cols-3 gap-4">
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
      </div>
    </div>

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
import { useAuthStore } from '../stores/auth'
import { usePromptStore } from '../stores/prompt'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const promptStore = usePromptStore()

const isLoading = ref(true)
const prompt = ref(null)

const isOwner = computed(() => {
  return prompt.value?.userId === authStore.user?.id
})

onMounted(async () => {
  try {
    const promptId = route.params.id as string
    prompt.value = await promptStore.getPromptById(promptId)
  } catch (error) {
    console.error('Failed to fetch prompt:', error)
  } finally {
    isLoading.value = false
  }
})

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

async function handleEdit() {
  router.push(`/prompts/${prompt.value.id}/edit`)
}

async function handleDelete() {
  if (!confirm('确定要删除这个提示词吗？此操作不可撤销。')) {
    return
  }

  try {
    await promptStore.deletePrompt(prompt.value.id)
    router.push('/prompts')
  } catch (error) {
    console.error('Failed to delete prompt:', error)
    alert('删除失败，请稍后重试')
  }
}
</script> 