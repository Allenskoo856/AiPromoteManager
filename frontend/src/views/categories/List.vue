<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">分类管理</h1>
      <button
        class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
        @click="showCreateModal = true"
      >
        新建分类
      </button>
    </div>

    <div v-if="loading" class="text-center py-8">
      加载中...
    </div>
    <div v-else-if="!categories.length" class="text-center py-8 text-gray-500">
      暂无分类数据
    </div>
    <div v-else class="bg-white rounded shadow overflow-hidden">
      <table class="min-w-full">
        <thead>
          <tr class="bg-gray-50">
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">名称</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">提示词数量</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">创建时间</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="category in categories" :key="category.id">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ category.id }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ category.name }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ category.promptCount || 0 }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ category.created_at }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              <button
                class="text-blue-600 hover:text-blue-800 mr-3"
                @click="handleEdit(category)"
              >
                编辑
              </button>
              <button
                class="text-red-600 hover:text-red-800"
                :disabled="isDeleting === category.id"
                @click="handleDelete(category)"
              >
                {{ isDeleting === category.id ? '删除中...' : '删除' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">
          {{ showEditModal ? '编辑分类' : '新建分类' }}
        </h2>
        <form @submit.prevent="handleSubmit">
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="name">
              分类名称
            </label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              required
            >
          </div>
          <div class="flex justify-end space-x-4">
            <button
              type="button"
              class="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded"
              @click="closeModal"
              :disabled="isSubmitting"
            >
              取消
            </button>
            <button
              type="submit"
              class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
              :disabled="isSubmitting"
            >
              {{ isSubmitting ? '保存中...' : '保存' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useCategoryStore } from '../../stores/category'
import type { Category } from '../../types'

const categoryStore = useCategoryStore()
const { categories, loading } = storeToRefs(categoryStore)

const isSubmitting = ref(false)
const isDeleting = ref<number | null>(null)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const form = ref<{
  id: number
  name: string
}>({
  id: 0,
  name: ''
})

onMounted(async () => {
  await loadCategories()
})

async function loadCategories() {
  try {
    await categoryStore.fetchCategories()
  } catch (error) {
    console.error('Failed to load categories:', error)
  }
}

function handleEdit(category: Category) {
  form.value = {
    id: category.id,
    name: category.name
  }
  showEditModal.value = true
}

async function handleDelete(category: Category) {
  if (!confirm(`确定要删除分类"${category.name}"吗？此操作不可撤销。`)) {
    return
  }

  isDeleting.value = category.id
  try {
    await categoryStore.deleteCategory(category.id)
    await loadCategories()
  } catch (error) {
    console.error('Failed to delete category:', error)
    alert('删除失败，请重试')
  } finally {
    isDeleting.value = null
  }
}

async function handleSubmit() {
  if (!form.value.name.trim()) {
    alert('请输入分类名称')
    return
  }

  isSubmitting.value = true
  try {
    if (showEditModal.value) {
      await categoryStore.updateCategory(form.value.id, {
        name: form.value.name.trim()
      })
    } else {
      await categoryStore.createCategory({
        name: form.value.name.trim()
      })
    }
    await loadCategories()
    closeModal()
  } catch (error) {
    console.error('Failed to save category:', error)
    alert('保存失败，请重试')
  } finally {
    isSubmitting.value = false
  }
}

function closeModal() {
  showCreateModal.value = false
  showEditModal.value = false
  form.value = {
    id: 0,
    name: ''
  }
}
</script> 