<template>
  <div>
    <!-- Widget Container -->
    <div ref="widgetContainer"></div>
    
    <!-- Search Trigger -->
    <UInput
      id="searchWidgetTrigger"
      placeholder="Search here"
      icon="i-heroicons-magnifying-glass"
      class="max-w-sm"
    />
  </div>
</template>

<script setup>
const widgetContainer = ref<HTMLElement | null>(null)

onMounted(() => {
  // Widget Element erstellen
  const widget = document.createElement('gen-search-widget')
  widget.setAttribute('configId', '8cbcd9d8-95bc-46db-a971-3371d90810c7')
  widget.setAttribute('location', 'eu')
  widget.setAttribute('triggerId', 'searchWidgetTrigger')
  
  // Widget zum Container hinzufügen
  if (widgetContainer.value) {
    widgetContainer.value.appendChild(widget)
  }
})
</script>