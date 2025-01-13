import type { Tag } from '../types'
import type { Ref } from 'vue'

export interface TagStore {
  tags: Ref<Tag[]>
  loading: Ref<boolean>
  fetchTags: () => Promise<Tag[]>
  createTag: (data: { name: string }) => Promise<Tag>
  updateTag: (id: number, data: { name: string }) => Promise<Tag>
  deleteTag: (id: number) => Promise<void>
}

export type UseTagStore = () => TagStore 