<template>
  <router-link
    :to="to"
    class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-md shadow-sm transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
  >
    <svg 
      class="w-5 h-5 mr-1.5" 
      fill="none" 
      stroke="currentColor" 
      viewBox="0 0 24 24"
    >
      <path 
        stroke-linecap="round" 
        stroke-linejoin="round" 
        stroke-width="2" 
        d="M10 19l-7-7m0 0l7-7m-7 7h18"
      />
    </svg>
    <slot>返回列表</slot>
  </router-link>
</template>

<script setup lang="ts">
defineProps<{
  to: string
}>()
</script> 