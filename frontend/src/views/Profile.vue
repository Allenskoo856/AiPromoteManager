<template>
  <div class="container mx-auto px-4 py-8">
    <div class="bg-white rounded-lg shadow p-6">
      <h1 class="text-2xl font-bold mb-6">个人中心</h1>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div class="bg-gray-50 rounded-lg p-4">
          <h2 class="text-lg font-semibold mb-4">基本信息</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">邮箱</label>
              <div class="mt-1 text-gray-900">{{ email }}</div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">用户名</label>
              <input
                type="text"
                v-model="username"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        <div class="bg-gray-50 rounded-lg p-4">
          <h2 class="text-lg font-semibold mb-4">修改密码</h2>
          <form @submit.prevent="handlePasswordChange" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">当前密码</label>
              <input
                type="password"
                v-model="passwordForm.current_password"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">新密码</label>
              <input
                type="password"
                v-model="passwordForm.new_password"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">确认新密码</label>
              <input
                type="password"
                v-model="passwordForm.confirm_password"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>
            <button
              type="submit"
              class="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              :disabled="isSubmitting"
            >
              {{ isSubmitting ? '保存中...' : '保存' }}
            </button>
          </form>
        </div>
      </div>

      <div class="bg-gray-50 rounded-lg p-4">
        <h2 class="text-lg font-semibold mb-4">使用统计</h2>
        <div v-if="statsStore.loading" class="text-center py-4">
          加载中...
        </div>
        <div v-else class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="bg-white p-4 rounded-lg shadow">
            <div class="text-sm text-gray-500">提示词数量</div>
            <div class="text-2xl font-bold">{{ statsStore.stats.prompt_count }}</div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow">
            <div class="text-sm text-gray-500">分类数量</div>
            <div class="text-2xl font-bold">{{ statsStore.stats.category_count }}</div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow">
            <div class="text-sm text-gray-500">标签数量</div>
            <div class="text-2xl font-bold">{{ statsStore.stats.tag_count }}</div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow">
            <div class="text-sm text-gray-500">分享数量</div>
            <div class="text-2xl font-bold">{{ statsStore.stats.share_count }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStatsStore } from '../stores/userStats'

const statsStore = useUserStatsStore()
const isSubmitting = ref(false)
const email = ref('user@example.com')
const username = ref('用户名')

const passwordForm = ref({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

onMounted(async () => {
  await statsStore.fetchStats()
})

async function handlePasswordChange() {
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    alert('两次输入的密码不一致')
    return
  }

  isSubmitting.value = true
  try {
    // TODO: 调用修改密码的 API
    alert('密码修改成功')
    passwordForm.value = {
      current_password: '',
      new_password: '',
      confirm_password: ''
    }
  } catch (error) {
    console.error('Failed to change password:', error)
    alert('密码修改失败，请重试')
  } finally {
    isSubmitting.value = false
  }
}
</script> 