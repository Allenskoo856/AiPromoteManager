<template>
  <div class="container mx-auto px-4 py-8">
    <!-- 搜索框 -->
    <div class="max-w-3xl mx-auto mb-8">
      <div class="relative">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索 Prompt"
          class="w-full h-12 pl-12 pr-4 rounded-full border border-gray-300 focus:border-primary-500 focus:ring-2 focus:ring-primary-500 focus:ring-opacity-50 transition-colors"
          @input="handleSearch"
        />
        <div class="absolute left-4 top-1/2 -translate-y-1/2">
          <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>
    </div>

    <!-- 分类标签 -->
    <div class="mb-8">
      <div class="flex flex-wrap gap-3 justify-center">
        <button
          class="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium transition-colors"
          :class="[
            selectedCategory === null 
              ? 'bg-primary-100 text-primary-800' 
              : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
          ]"
          @click="selectedCategory = null; handleFilter()"
        >
          <span class="mr-2">📑</span>
          全部
        </button>
        <button
          v-for="category in categories"
          :key="category.id"
          class="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium transition-colors"
          :class="[
            selectedCategory === category.id
              ? 'bg-primary-100 text-primary-800'
              : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
          ]"
          @click="selectedCategory = category.id; handleFilter()"
        >
          <span class="mr-2">{{ getCategoryIcon(category.name) }}</span>
          {{ category.name }}
        </button>
      </div>
    </div>

    <!-- 提示词卡片网格 -->
    <div v-if="isLoading" class="text-center py-12">
      <div class="inline-flex items-center">
        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-primary-500" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>加载中...</span>
      </div>
    </div>

    <div v-else-if="prompts.length === 0" class="text-center py-12">
      <div class="text-gray-500">暂无提示词</div>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <router-link
        v-for="prompt in prompts"
        :key="prompt.id"
        :to="`/prompts/${prompt.id}`"
        class="block group"
      >
        <div class="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow h-full border border-gray-100">
          <div class="p-5 flex flex-col h-full">
            <h3 class="text-lg font-semibold text-gray-900 group-hover:text-primary-600 transition-colors line-clamp-2 mb-4">
              {{ prompt.title }}
            </h3>
            <p class="text-sm text-gray-600 line-clamp-3 mb-4">
              {{ prompt.content }}
            </p>
            <p class="text-sm text-gray-500 line-clamp-2 mb-4">
              {{ prompt.description }}
            </p>
            <div class="mt-auto space-y-3">
              <div class="flex items-center text-sm text-gray-500">
                <span>{{ formatDate(prompt.created_at) }}</span>
                <span class="mx-2">·</span>
                <span>{{ prompt.category?.name || '未分类' }}</span>
              </div>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="tag in (prompt.tags || []).slice(0, 3)"
                  :key="tag.id"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-50 text-primary-700"
                >
                  {{ tag.name }}
                </span>
                <span
                  v-if="(prompt.tags || []).length > 3"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-50 text-gray-600"
                >
                  +{{ (prompt.tags || []).length - 3 }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </router-link>
    </div>

    <!-- 分页 -->
    <div v-if="totalPages > 1" class="mt-8 flex justify-center">
      <nav class="inline-flex rounded-md shadow">
        <button
          class="px-3 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="currentPage === 1"
          @click="handlePageChange(currentPage - 1)"
        >
          上一页
        </button>
        <button
          v-for="page in displayedPages"
          :key="page"
          class="px-3 py-2 border-t border-b border-gray-300 bg-white text-sm font-medium transition-colors"
          :class="[
            currentPage === page
              ? 'text-primary-600 border-primary-500'
              : 'text-gray-700 hover:bg-gray-50'
          ]"
          @click="handlePageChange(page)"
        >
          {{ page }}
        </button>
        <button
          class="px-3 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="currentPage === totalPages"
          @click="handlePageChange(currentPage + 1)"
        >
          下一页
        </button>
      </nav>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { usePromptStore } from '@/stores/prompt'
import { useCategoryStore } from '@/stores/category'
import { useTagStore } from '@/stores/tag'

const pageSize = 10

const promptStore = usePromptStore()
const categoryStore = useCategoryStore()
const tagStore = useTagStore()

const isLoading = ref(false)
const searchQuery = ref('')
const selectedCategory = ref<number | null>(null)
const currentPage = ref(1)

const categories = computed(() => categoryStore.categories)
const prompts = computed(() => promptStore.prompts)
const totalCount = computed(() => promptStore.total)

const totalPages = computed(() => Math.ceil(totalCount.value / pageSize))

onMounted(async () => {
  try {
    await Promise.all([
      categoryStore.fetchCategories(),
      tagStore.fetchTags(),
      loadPrompts()
    ])
  } catch (error) {
    console.error('Failed to load initial data:', error)
  }
})

async function loadPrompts() {
  isLoading.value = true
  try {
    await promptStore.fetchPrompts(currentPage.value, pageSize, {
      category_id: selectedCategory.value,
      search: searchQuery.value
    })
  } catch (error) {
    console.error('Failed to load prompts:', error)
  } finally {
    isLoading.value = false
  }
}

function debounce<T extends (...args: any[]) => any>(fn: T, delay: number) {
  let timeout: NodeJS.Timeout
  return function (this: any, ...args: Parameters<T>) {
    clearTimeout(timeout)
    timeout = setTimeout(() => fn.apply(this, args), delay)
  }
}

const handleSearch = debounce(async () => {
  currentPage.value = 1
  await loadPrompts()
}, 300)

async function handleFilter() {
  currentPage.value = 1
  await loadPrompts()
}

async function handlePageChange(page: number | string) {
  if (typeof page === 'number') {
    currentPage.value = page
    await loadPrompts()
  }
}

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 计算要显示的页码
const displayedPages = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  const delta = 2
  const range: (number | string)[] = []
  
  for (let i = Math.max(2, current - delta); i <= Math.min(total - 1, current + delta); i++) {
    range.push(i)
  }
  
  if (current - delta > 2) {
    range.unshift('...')
  }
  if (current + delta < total - 1) {
    range.push('...')
  }
  
  range.unshift(1)
  if (total !== 1) {
    range.push(total)
  }
  
  return range
})

// 获取分类图标
function getCategoryIcon(categoryName: string): string {
  const icons = {
    '文本': '📝',
    '图像设计': '🎨',
    '商业': '💼',
    '个人生活': '🏠',
    '市场营销': '📈',
    '代码': '💻',
    '教育学习': '📚',
    '知识探索': '🔍',
    '内容创作': '✍️',
    '游戏娱乐': '🎮',
    '人格化': '🤖',
    '策略建议': '💡'
  }
  return (icons as any)[categoryName] || '📑'
}
</script>

<style>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>