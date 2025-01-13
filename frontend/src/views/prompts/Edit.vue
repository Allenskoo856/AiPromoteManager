<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div v-if="isLoading" class="flex justify-center items-center min-h-[400px]">
      <div class="text-gray-500">加载中...</div>
    </div>

    <div v-else-if="!isOwner" class="text-center py-12">
      <p class="text-gray-500">您没有权限编辑此提示词</p>
      <router-link :to="`/prompts/${promptId}`" class="mt-4 btn-primary inline-block">
        返回详情
      </router-link>
    </div>

    <div v-else class="bg-white shadow rounded-lg">
      <div class="px-6 py-5 border-b border-gray-200">
        <h1 class="text-2xl font-bold text-gray-900">编辑提示词</h1>
      </div>

      <form @submit.prevent="handleSubmit" class="px-6 py-5 space-y-6">
        <!-- 标题 -->
        <div>
          <label for="title" class="block text-sm font-medium text-gray-700">标题</label>
          <input
            type="text"
            id="title"
            v-model="form.title"
            required
            class="mt-1 input w-full"
            placeholder="请输入提示词标题"
          />
        </div>

        <!-- 内容 -->
        <div>
          <label for="content" class="block text-sm font-medium text-gray-700">内容</label>
          <div class="mt-1 relative">
            <textarea
              id="content"
              v-model="form.content"
              rows="8"
              required
              class="input w-full font-mono"
              placeholder="请输入提示词内容..."
            ></textarea>
            <div class="absolute bottom-2 right-2 text-sm text-gray-500">
              {{ form.content.length }} 字符
            </div>
          </div>
          <p class="mt-1 text-sm text-gray-500">
            提示：使用清晰、具体的描述，可以包含变量占位符，例如 {name}、{context} 等。
          </p>
        </div>

        <!-- 分类 -->
        <div>
          <label for="category" class="block text-sm font-medium text-gray-700">分类</label>
          <div class="mt-1 flex items-center space-x-4">
            <select
              id="category"
              v-model="form.categoryId"
              class="input flex-1"
            >
              <option value="">未分类</option>
              <option
                v-for="category in categories"
                :key="category.id"
                :value="category.id"
              >
                {{ category.name }}
              </option>
            </select>
            <button
              type="button"
              class="btn-secondary"
              @click="showNewCategoryInput = true"
              v-if="!showNewCategoryInput"
            >
              新建分类
            </button>
          </div>
          <!-- 新建分类输入框 -->
          <div v-if="showNewCategoryInput" class="mt-2">
            <div class="flex items-center space-x-2">
              <input
                type="text"
                v-model="newCategoryName"
                class="input flex-1"
                placeholder="请输入分类名称"
              />
              <button
                type="button"
                class="btn-primary"
                @click="handleCreateCategory"
                :disabled="isCreatingCategory"
              >
                {{ isCreatingCategory ? '创建中...' : '确认' }}
              </button>
              <button
                type="button"
                class="btn-secondary"
                @click="cancelCreateCategory"
              >
                取消
              </button>
            </div>
          </div>
        </div>

        <!-- 标签 -->
        <div>
          <label class="block text-sm font-medium text-gray-700">标签</label>
          <div class="mt-1">
            <!-- 已选标签 -->
            <div class="flex flex-wrap gap-2 mb-2">
              <span
                v-for="tag in selectedTags"
                :key="tag.id"
                class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-100 text-primary-800"
              >
                {{ tag.name }}
                <button
                  type="button"
                  class="ml-1 inline-flex items-center p-0.5 hover:bg-primary-200 rounded-full"
                  @click="removeTag(tag.id)"
                >
                  <span class="sr-only">删除</span>
                  <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
                  </svg>
                </button>
              </span>
            </div>
            <!-- 标签输入和选择 -->
            <div class="flex items-center space-x-2">
              <div class="relative flex-1">
                <input
                  type="text"
                  v-model="tagInput"
                  class="input w-full"
                  placeholder="输入标签名称或从下拉列表选择"
                  @input="handleTagInput"
                  @keydown.enter.prevent="handleTagSelect"
                  @keydown.down.prevent="handleTagNavigate(1)"
                  @keydown.up.prevent="handleTagNavigate(-1)"
                  @focus="showTagDropdown = true"
                />
                <!-- 标签建议列表 -->
                <div
                  v-if="(tagSuggestions.length > 0 || availableTags.length > 0) && showTagDropdown"
                  class="absolute z-10 w-full mt-1 bg-white shadow-lg rounded-md border border-gray-200 max-h-60 overflow-y-auto"
                >
                  <div v-if="tagSuggestions.length > 0" class="py-1">
                    <div class="px-3 py-1 text-xs text-gray-500 bg-gray-50">匹配结果</div>
                    <ul>
                      <li
                        v-for="(tag, index) in tagSuggestions"
                        :key="tag.id"
                        :class="[
                          'px-3 py-2 cursor-pointer hover:bg-gray-100',
                          { 'bg-gray-100': index === selectedTagIndex }
                        ]"
                        @click="selectTag(tag)"
                      >
                        {{ tag.name }}
                      </li>
                    </ul>
                  </div>
                  <div v-if="availableTags.length > 0" class="py-1 border-t border-gray-200">
                    <div class="px-3 py-1 text-xs text-gray-500 bg-gray-50">可选标签</div>
                    <ul>
                      <li
                        v-for="tag in availableTags"
                        :key="tag.id"
                        class="px-3 py-2 cursor-pointer hover:bg-gray-100"
                        @click="selectTag(tag)"
                      >
                        {{ tag.name }}
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              <button
                type="button"
                class="btn-secondary"
                @click="handleTagSelect"
              >
                添加
              </button>
            </div>
          </div>
        </div>

        <!-- 按钮 -->
        <div class="flex justify-end space-x-3 pt-4">
          <router-link
            :to="`/prompts/${promptId}`"
            class="btn-secondary"
          >
            取消
          </router-link>
          <button
            type="submit"
            class="btn-primary"
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? '保存中...' : '保存' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { usePromptStore } from '@/stores/prompt'
import { useCategoryStore } from '@/stores/category'
import { useTagStore } from '@/stores/tag'
import { useAuthStore } from '@/stores/auth'
import type { Category, Tag, Prompt } from '@/types'

const route = useRoute()
const router = useRouter()
const promptStore = usePromptStore()
const categoryStore = useCategoryStore()
const tagStore = useTagStore()
const authStore = useAuthStore()

const promptId = ref(Number(route.params.id))
const prompt = ref<Prompt | null>(null)
const isLoading = ref(false)
const isSubmitting = ref(false)
const categories = ref<Category[]>([])
const showNewCategoryInput = ref(false)
const newCategoryName = ref('')
const isCreatingCategory = ref(false)

// 标签相关
const tagInput = ref('')
const selectedTagIndex = ref(-1)
const selectedTags = ref<Tag[]>([])
const allTags = ref<Tag[]>([])
const showTagDropdown = ref(false)

const form = ref<{
  title: string
  content: string
  description: string
  categoryId: number | undefined
  tagIds: number[]
  is_public: boolean
}>({
  title: '',
  content: '',
  description: '',
  categoryId: undefined,
  tagIds: [],
  is_public: true
})

// 计算可选的标签（排除已选的标签）
const availableTags = computed(() => {
  return allTags.value.filter(tag => !form.value.tagIds.includes(tag.id))
})

// 计算搜索建议
const tagSuggestions = computed(() => {
  if (!tagInput.value) return []
  return availableTags.value.filter(tag => 
    tag.name.toLowerCase().includes(tagInput.value.toLowerCase())
  )
})

// 处理标签输入
function handleTagInput() {
  selectedTagIndex.value = -1
  showTagDropdown.value = true
}

// 选择标签
function selectTag(tag: Tag) {
  if (!form.value.tagIds.includes(tag.id)) {
    form.value.tagIds.push(tag.id)
    selectedTags.value.push(tag)
  }
  tagInput.value = ''
  showTagDropdown.value = false
}

// 移除标签
function removeTag(tagId: number) {
  form.value.tagIds = form.value.tagIds.filter(id => id !== tagId)
  selectedTags.value = selectedTags.value.filter(tag => tag.id !== tagId)
}

// 处理标签选择
function handleTagSelect() {
  if (selectedTagIndex.value >= 0 && tagSuggestions.value[selectedTagIndex.value]) {
    selectTag(tagSuggestions.value[selectedTagIndex.value])
  } else if (tagInput.value.trim()) {
    // 如果有匹配的现有标签，选择第一个
    const matchingTag = availableTags.value.find(tag => 
      tag.name.toLowerCase() === tagInput.value.trim().toLowerCase()
    )
    if (matchingTag) {
      selectTag(matchingTag)
    }
  }
}

// 处理标签导航
function handleTagNavigate(direction: number) {
  if (tagSuggestions.value.length === 0) return
  
  const newIndex = selectedTagIndex.value + direction
  if (newIndex >= -1 && newIndex < tagSuggestions.value.length) {
    selectedTagIndex.value = newIndex
  }
}

// 点击页面其他地方时关闭下拉框
onMounted(() => {
  document.addEventListener('click', (e) => {
    const target = e.target as HTMLElement
    if (!target.closest('.relative')) {
      showTagDropdown.value = false
    }
  })
})

const isOwner = computed(() => {
  if (!prompt.value || !authStore.user) return false
  return String(prompt.value.owner_id) === String(authStore.user.id)
})

const loadPrompt = async () => {
  isLoading.value = true
  try {
    const id = Array.isArray(promptId.value) ? promptId.value[0] : promptId.value
    const data = await promptStore.fetchPrompt(Number(id))
    prompt.value = data
    if (data) {
      form.value = {
        title: data.title,
        content: data.content,
        description: data.description || '',
        categoryId: data.category_id,
        tagIds: data.tags.map(tag => tag.id),
        is_public: data.is_public
      }
      selectedTags.value = data.tags
    }
  } catch (error) {
    console.error('Failed to fetch prompt:', error)
  } finally {
    isLoading.value = false
  }
}

const handleSubmit = async () => {
  if (!prompt.value) return
  
  try {
    isSubmitting.value = true
    const id = Number(promptId.value)
    await promptStore.updatePrompt(id, {
      title: form.value.title,
      content: form.value.content,
      description: form.value.description,
      category_id: form.value.categoryId || undefined,
      tag_ids: form.value.tagIds,
      is_public: form.value.is_public
    })
    router.push(`/prompts/${id}`)
  } catch (error) {
    console.error('Failed to update prompt:', error)
  } finally {
    isSubmitting.value = false
  }
}

// 创建新分类
async function handleCreateCategory() {
  if (!newCategoryName.value.trim()) return
  
  isCreatingCategory.value = true
  try {
    const category = await categoryStore.createCategory({
      name: newCategoryName.value.trim()
    })
    categories.value.push(category)
    form.value.categoryId = category.id
    showNewCategoryInput.value = false
    newCategoryName.value = ''
  } catch (error) {
    console.error('Failed to create category:', error)
    alert('创建分类失败，请重试')
  } finally {
    isCreatingCategory.value = false
  }
}

function cancelCreateCategory() {
  showNewCategoryInput.value = false
  newCategoryName.value = ''
}

// 加载数据
const loadData = async () => {
  try {
    await Promise.all([
      loadPrompt(),
      categoryStore.fetchCategories(),
      tagStore.fetchTags()
    ])
    
    categories.value = categoryStore.categories
    allTags.value = tagStore.tags
  } catch (error) {
    console.error('Failed to load data:', error)
  }
}

onMounted(() => {
  loadData()
})
</script> 