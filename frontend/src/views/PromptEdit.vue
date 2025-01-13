<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="bg-white shadow rounded-lg">
      <div class="px-6 py-5 border-b border-gray-200">
        <h1 class="text-2xl font-bold text-gray-900">
          {{ isEdit ? '编辑提示词' : '创建提示词' }}
        </h1>
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
          <textarea
            id="content"
            v-model="form.content"
            rows="6"
            required
            class="mt-1 input w-full"
            placeholder="请输入提示词内容"
          ></textarea>
        </div>

        <!-- 分类 -->
        <div>
          <label for="category" class="block text-sm font-medium text-gray-700">分类</label>
          <select
            id="category"
            v-model="form.categoryId"
            class="mt-1 input w-full"
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
        </div>

        <!-- 标签 -->
        <div>
          <label class="block text-sm font-medium text-gray-700">标签</label>
          <div class="mt-1 flex flex-wrap gap-2">
            <div
              v-for="tag in tags"
              :key="tag.id"
              class="inline-flex items-center"
            >
              <label class="inline-flex items-center space-x-2">
                <input
                  type="checkbox"
                  :value="tag.id"
                  v-model="form.tagIds"
                  class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                <span>{{ tag.name }}</span>
              </label>
            </div>
          </div>
        </div>

        <!-- 按钮 -->
        <div class="flex justify-end space-x-3">
          <router-link
            :to="isEdit ? `/prompts/${promptId}` : '/prompts'"
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
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePromptStore } from '../stores/prompt'
import { useCategoryStore } from '../stores/category'
import { useTagStore } from '../stores/tag'

const route = useRoute()
const router = useRouter()
const promptStore = usePromptStore()
const categoryStore = useCategoryStore()
const tagStore = useTagStore()

const promptId = computed(() => route.params.id as string)
const isEdit = computed(() => !!promptId.value)

const categories = ref([])
const tags = ref([])
const isSubmitting = ref(false)

const form = ref({
  title: '',
  content: '',
  categoryId: '',
  tagIds: [] as string[]
})

onMounted(async () => {
  try {
    // 加载分类和标签
    const [categoriesData, tagsData] = await Promise.all([
      categoryStore.getCategories(),
      tagStore.getTags()
    ])
    categories.value = categoriesData
    tags.value = tagsData

    // 如果是编辑模式，加载提示词数据
    if (isEdit.value) {
      const prompt = await promptStore.getPromptById(promptId.value)
      form.value = {
        title: prompt.title,
        content: prompt.content,
        categoryId: prompt.categoryId || '',
        tagIds: prompt.tags.map(tag => tag.id)
      }
    }
  } catch (error) {
    console.error('Failed to load data:', error)
    alert('加载数据失败，请刷新页面重试')
  }
})

async function handleSubmit() {
  if (isSubmitting.value) return

  isSubmitting.value = true
  try {
    if (isEdit.value) {
      await promptStore.updatePrompt({
        id: promptId.value,
        ...form.value
      })
      router.push(`/prompts/${promptId.value}`)
    } else {
      const newPrompt = await promptStore.createPrompt(form.value)
      router.push(`/prompts/${newPrompt.id}`)
    }
  } catch (error) {
    console.error('Failed to save prompt:', error)
    alert('保存失败，请稍后重试')
  } finally {
    isSubmitting.value = false
  }
}
</script> 