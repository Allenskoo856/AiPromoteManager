import { defineStore } from 'pinia'
import { ref } from 'vue'
import request from '../utils/request'
import type { Prompt } from '../types'

export const usePromptStore = defineStore('prompt', () => {
  const prompts = ref<Prompt[]>([])
  const loading = ref(false)
  const total = ref(0)

  // 获取提示词列表
  const fetchPrompts = async (page: number = 1, pageSize: number = 10, filters?: { 
    category_id?: number | null,
    search?: string
  }) => {
    loading.value = true
    try {
      const response = await request.get('/api/v1/prompts', {
        params: {
          skip: (page - 1) * pageSize,
          limit: pageSize,
          category_id: filters?.category_id || undefined,
          search: filters?.search
        },
      })
      prompts.value = response.data
      total.value = parseInt(response.headers['x-total-count'] || '0')
    } catch (error) {
      console.error('Failed to fetch prompts:', error)
    } finally {
      loading.value = false
    }
  }

  // 获取单个提示词
  const fetchPrompt = async (id: number) => {
    try {
      const response = await request.get(`/api/v1/prompts/${id}`)
      return response.data
    } catch (error) {
      console.error('Failed to fetch prompt:', error)
      throw error
    }
  }

  // 创建提示词
  const createPrompt = async (data: {
    title: string
    content: string
    description?: string
    is_public?: boolean
    category_id?: number
    tag_ids?: number[]
  }) => {
    try {
      const response = await request.post('/api/v1/prompts', data)
      await fetchPrompts()
      return response.data
    } catch (error) {
      console.error('Failed to create prompt:', error)
      throw error
    }
  }

  // 更新提示词
  const updatePrompt = async (id: number, data: {
    title?: string
    content?: string
    description?: string
    is_public?: boolean
    category_id?: number
    tag_ids?: number[]
  }) => {
    try {
      const response = await request.put(`/api/v1/prompts/${id}`, data)
      await fetchPrompts()
      return response.data
    } catch (error) {
      console.error('Failed to update prompt:', error)
      throw error
    }
  }

  // 删除提示词
  const deletePrompt = async (id: number) => {
    try {
      await request.delete(`/api/v1/prompts/${id}`)
      await fetchPrompts()
    } catch (error) {
      console.error('Failed to delete prompt:', error)
      throw error
    }
  }

  return {
    prompts,
    loading,
    total,
    fetchPrompts,
    fetchPrompt,
    createPrompt,
    updatePrompt,
    deletePrompt,
  }
}) 