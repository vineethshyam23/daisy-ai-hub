<template>
  <div class="bg-amber-50 border border-amber-200 rounded-xl p-4 flex items-start space-x-3 shadow-sm">
    <UIcon name="i-heroicons-information-circle" class="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5" />
    <div class="flex-1">
      <h4 class="text-amber-800 font-medium text-sm mb-1">Disclaimer</h4>
      <p class="text-amber-700 text-sm leading-relaxed">
        {{ disclaimerText }}
      </p>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  disclaimerText: {
    type: String,
    required: true
  }
})
</script>