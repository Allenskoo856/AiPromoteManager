import { defineStore } from 'pinia';
import { ref } from 'vue';
import request from '../utils/request';

interface UserStats {
  prompt_count: number;
  category_count: number;
  tag_count: number;
  share_count: number;
}

export const useUserStatsStore = defineStore('userStats', () => {
  const stats = ref<UserStats>({
    prompt_count: 0,
    category_count: 0,
    tag_count: 0,
    share_count: 0
  });
  const loading = ref(false);

  const fetchStats = async () => {
    loading.value = true;
    try {
      const response = await request.get('/api/v1/users/me/stats');
      stats.value = response.data;
    } catch (error) {
      console.error('Failed to fetch user stats:', error);
    } finally {
      loading.value = false;
    }
  };

  return {
    stats,
    loading,
    fetchStats
  };
}); 