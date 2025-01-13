import { defineStore } from 'pinia';
import { ref } from 'vue';
import request from '../utils/request';
import type { Category } from '../types';

export const useCategoryStore = defineStore('category', () => {
  const categories = ref<Category[]>([]);
  const categoryTree = ref<Category[]>([]);
  const loading = ref(false);

  // 获取所有分类
  const fetchCategories = async () => {
    loading.value = true;
    try {
      const response = await request.get('/api/v1/categories');
      categories.value = response.data;
      return response.data;
    } catch (error) {
      console.error('Failed to fetch categories:', error);
      return [];
    } finally {
      loading.value = false;
    }
  };

  // 获取分类树
  const fetchCategoryTree = async () => {
    loading.value = true;
    try {
      const response = await request.get('/api/v1/categories/tree');
      categoryTree.value = response.data;
      return response.data;
    } catch (error) {
      console.error('Failed to fetch category tree:', error);
      return [];
    } finally {
      loading.value = false;
    }
  };

  // 创建分类
  const createCategory = async (data: { name: string; parent_id?: number }) => {
    try {
      const response = await request.post('/api/v1/categories', data);
      await fetchCategories();
      return response.data;
    } catch (error) {
      console.error('Failed to create category:', error);
      throw error;
    }
  };

  // 更新分类
  const updateCategory = async (id: number, data: { name: string; parent_id?: number }) => {
    try {
      const response = await request.put(`/api/v1/categories/${id}`, data);
      await fetchCategories();
      return response.data;
    } catch (error) {
      console.error('Failed to update category:', error);
      throw error;
    }
  };

  // 删除分类
  const deleteCategory = async (id: number) => {
    try {
      await request.delete(`/api/v1/categories/${id}`);
      await fetchCategories();
    } catch (error) {
      console.error('Failed to delete category:', error);
      throw error;
    }
  };

  return {
    categories,
    categoryTree,
    loading,
    fetchCategories,
    fetchCategoryTree,
    createCategory,
    updateCategory,
    deleteCategory,
  }
}) 