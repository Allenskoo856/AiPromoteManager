import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '../types'
import { request } from '../utils/request'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref<User | null>(null)

  async function fetchCurrentUser() {
    try {
      const data = await request.get<User>('/users/me')
      currentUser.value = data
      return data
    } catch (error) {
      console.error('Failed to fetch user:', error)
      throw error
    }
  }

  function clearUser() {
    currentUser.value = null
  }

  return {
    currentUser,
    fetchCurrentUser,
    clearUser
  }
}) 