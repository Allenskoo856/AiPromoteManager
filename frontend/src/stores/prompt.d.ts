import type { Prompt } from '../types'
import type { Ref } from 'vue'

export interface PromptStore {
  prompts: Ref<Prompt[]>
  loading: Ref<boolean>
  total: Ref<number>
  fetchPrompts: (page?: number, pageSize?: number) => Promise<void>
  fetchPrompt: (id: number) => Promise<Prompt>
  createPrompt: (data: {
    title: string
    content: string
    description?: string
    is_public?: boolean
    category_id?: number
    tag_ids?: number[]
  }) => Promise<Prompt>
  updatePrompt: (id: number, data: {
    title?: string
    content?: string
    description?: string
    is_public?: boolean
    category_id?: number
    tag_ids?: number[]
  }) => Promise<Prompt>
  deletePrompt: (id: number) => Promise<void>
} 