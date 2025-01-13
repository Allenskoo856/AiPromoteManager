<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- 头部区域 -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">标签管理</h1>
      <button
        @click="showCreateModal = true"
        class="btn-primary"
      >
        创建标签
      </button>
    </div>

    <!-- 列表区域 -->
    <div class="bg-white shadow rounded-lg">
      <div v-if="isLoading" class="flex justify-center items-center py-12">
        <div class="text-gray-500">加载中...</div>
      </div>

      <div v-else-if="tags.length === 0" class="text-center py-12">
        <p class="text-gray-500">暂无标签</p>
      </div>

      <div v-else>
        <ul class="divide-y divide-gray-200">
          <li v-for="tag in tags" :key="tag.id" class="hover:bg-gray-50">
            <div class="px-6 py-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-100 text-primary-800">
                    {{ tag.name }}
                  </span>
                  <span class="ml-4 text-sm text-gray-500">
                    {{ tag.promptCount || 0 }} 个提示词
                  </span>
                </div>
                <div class="flex items-center space-x-3">
                  <button
                    @click="handleEdit(tag)"
                    class="btn-secondary"
                  >
                    编辑
                  </button>
                  <button
                    @click="handleDelete(tag)"
                    class="btn-danger"
                    :disabled="isDeleting === tag.id"
                  >
                    {{ isDeleting === tag.id ? '删除中...' : '删除' }}
                  </button>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- 创建/编辑模态框 -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 z-10">
      <!-- 背景遮罩 -->
      <div class="absolute inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>

      <!-- 模态框 -->
      <div class="fixed inset-0 z-10 overflow-y-auto">
        <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
          <div class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6">
            <div>
              <h3 class="text-lg font-medium leading-6 text-gray-900">
                {{ showEditModal ? '编辑标签' : '创建标签' }}
              </h3>
              <div class="mt-2">
                <input
                  type="text"
                  v-model="form.name"
                  class="input"
                  placeholder="请输入标签名称"
                  :disabled="isSubmitting"
                />
              </div>
            </div>
            <div class="mt-5 sm:mt-6 sm:grid sm:grid-flow-row-dense sm:grid-cols-2 sm:gap-3">
              <button
                type="button"
                class="btn-primary"
                @click="handleSubmit"
                :disabled="isSubmitting"
              >
                {{ isSubmitting ? '保存中...' : '保存' }}
              </button>
              <button
                type="button"
                class="btn-secondary mt-3 sm:mt-0"
                @click="closeModal"
                :disabled="isSubmitting"
              >
                取消
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useTagStore } from '../../stores/tag'
import type { Tag } from '../../types'

const tagStore = useTagStore()

const isLoading = ref(false)
const isSubmitting = ref(false)
const isDeleting = ref<number | null>(null)
const tags = ref<Tag[]>([])
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
  await loadTags()
})

async function loadTags() {
  isLoading.value = true
  try {
    tags.value = await tagStore.fetchTags()
  } catch (error) {
    console.error('Failed to load tags:', error)
  } finally {
    isLoading.value = false
  }
}

function handleEdit(tag: Tag) {
  form.value = {
    id: tag.id,
    name: tag.name
  }
  showEditModal.value = true
}

async function handleDelete(tag: Tag) {
  if (!confirm(`确定要删除标签"${tag.name}"吗？此操作不可撤销。`)) {
    return
  }

  isDeleting.value = tag.id
  try {
    await tagStore.deleteTag(tag.id)
    await loadTags()
  } catch (error) {
    console.error('Failed to delete tag:', error)
    alert('删除失败，请重试')
  } finally {
    isDeleting.value = null
  }
}

async function handleSubmit() {
  if (!form.value.name.trim()) {
    alert('请输入标签名称')
    return
  }

  isSubmitting.value = true
  try {
    if (showEditModal.value) {
      await tagStore.updateTag(form.value.id, {
        name: form.value.name.trim()
      })
    } else {
      await tagStore.createTag({
        name: form.value.name.trim()
      })
    }
    await loadTags()
    closeModal()
  } catch (error) {
    console.error('Failed to save tag:', error)
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