<template>
  <div>
    <!-- Loading Screen while determining auth status -->
    <div v-if="!authStore.isInitialized" class="min-h-screen bg-gradient-to-br from-orange-50 via-orange-25 to-amber-50 flex items-center justify-center">
      <div class="text-center">
        <div class="w-16 h-16 bg-gradient-to-br from-orange-500 to-amber-500 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl animate-pulse">
          <UIcon name="i-heroicons-cpu-chip" class="w-8 h-8 text-white" />
        </div>
        <h2 class="text-2xl font-bold bg-gradient-to-r from-orange-500 to-amber-500 bg-clip-text text-transparent mb-2">
          DAISY
        </h2>
        <p class="text-gray-600 font-light">Loading your workspace...</p>
        <div class="mt-4 flex justify-center">
          <div class="w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
      </div>
    </div>

    <!-- Main Content when authenticated -->
    <div v-else>
      <slot />
      
      <!-- Global Footer -->
      <GlobalFooter />
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()
</script>