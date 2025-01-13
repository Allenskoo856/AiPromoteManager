import type { Category } from '../types'
import type { Ref } from 'vue'

export interface CategoryStore {
  categories: Ref<Category[]>
  categoryTree: Ref<Category[]>
  loading: Ref<boolean>
  fetchCategories: () => Promise<Category[]>
  fetchCategoryTree: () => Promise<Category[]>
  createCategory: (data: { name: string; parent_id?: number }) => Promise<Category>
  updateCategory: (id: number, data: { name: string; parent_id?: number }) => Promise<Category>
  deleteCategory: (id: number) => Promise<void>
}

export type UseCategoryStore = () => CategoryStore 