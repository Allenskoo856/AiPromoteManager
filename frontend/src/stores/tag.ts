import { defineStore } from 'pinia';
import { ref } from 'vue';
import request from '../utils/request';
import type { Tag } from '../types';

export const useTagStore = defineStore('tag', () => {
  const tags = ref<Tag[]>([]);
  const loading = ref(false);

  // 获取所有标签
  const fetchTags = async () => {
    loading.value = true;
    try {
      const response = await request.get('/api/v1/tags');
      tags.value = response.data;
      return response.data;
    } catch (error) {
      console.error('Failed to fetch tags:', error);
      return [];
    } finally {
      loading.value = false;
    }
  };

  // 创建标签
  const createTag = async (data: { name: string }) => {
    try {
      const response = await request.post('/api/v1/tags', data);
      await fetchTags();
      return response.data;
    } catch (error) {
      console.error('Failed to create tag:', error);
      throw error;
    }
  };

  // 更新标签
  const updateTag = async (id: number, data: { name: string }) => {
    try {
      const response = await request.put(`/api/v1/tags/${id}`, data);
      await fetchTags();
      return response.data;
    } catch (error) {
      console.error('Failed to update tag:', error);
      throw error;
    }
  };

  // 删除标签
  const deleteTag = async (id: number) => {
    try {
      await request.delete(`/api/v1/tags/${id}`);
      await fetchTags();
    } catch (error) {
      console.error('Failed to delete tag:', error);
      throw error;
    }
  };

  return {
    tags,
    loading,
    fetchTags,
    createTag,
    updateTag,
    deleteTag,
  }
}) 