<template>
  <div v-if="show" class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click="handleBackdropClick">
    <div class="relative max-w-2xl w-full" @click.stop>
      <!-- Modal Content -->
      <div class="bg-white rounded-2xl shadow-2xl overflow-hidden">
        <!-- Header -->
        <div :class="[headerClasses, 'px-6 py-4']">
          <div class="flex items-center justify-between">
            <h2 class="text-xl font-bold text-white">
              {{ isEditMode ? 'Edit Template' : 'Create New Template' }}
            </h2>
            <button
              @click="handleClose"
              class="w-8 h-8 bg-white/20 hover:bg-white/30 rounded-full flex items-center justify-center text-white transition-colors cursor-pointer"
            >
              <UIcon name="i-heroicons-x-mark" class="w-5 h-5" />
            </button>
          </div>
        </div>

        <!-- Form Content -->
        <div class="p-6">
          <form @submit.prevent="handleSubmit" class="space-y-6">
            <!-- Title Input -->
            <div>
              <label for="template-title" class="block text-sm font-medium text-gray-700 mb-2">
                Template Title *
              </label>
              <input
                id="template-title"
                v-model="formData.title"
                type="text"
                placeholder="e.g., 'Extract Contact Information', 'Convert to Table Format'"
                :class="['w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 transition-colors', focusClasses]"
                required
                maxlength="100"
                :disabled="isLoading"
              />
              <p class="text-xs text-gray-500 mt-1">{{ formData.title.length }}/100 characters</p>
            </div>

            <!-- Description Input (Optional) -->
            <div>
              <label for="template-description" class="block text-sm font-medium text-gray-700 mb-2">
                Description (Optional)
              </label>
              <input
                id="template-description"
                v-model="formData.description"
                type="text"
                placeholder="Brief description of what this template does..."
                :class="['w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 transition-colors', focusClasses]"
                maxlength="200"
                :disabled="isLoading"
              />
              <p class="text-xs text-gray-500 mt-1">{{ formData.description.length }}/200 characters</p>
            </div>

            <!-- Content Textarea -->
            <div>
              <label for="template-content" class="block text-sm font-medium text-gray-700 mb-2">
                Processing Instructions *
              </label>
              <textarea
                id="template-content"
                v-model="formData.content"
                rows="8"
                placeholder="Enter the processing instructions that will be used when this template is selected..."
                :class="['w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 transition-colors resize-none', focusClasses]"
                required
                maxlength="2000"
                :disabled="isLoading"
              ></textarea>
              <p class="text-xs text-gray-500 mt-1">{{ formData.content.length }}/2000 characters</p>
            </div>

            <!-- Form Actions -->
            <div class="flex items-center justify-end space-x-4 pt-4 border-t border-gray-200">
              <button
                type="button"
                @click="handleClose"
                :disabled="isLoading"
                class="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="isLoading || !formData.title.trim() || !formData.content.trim()"
                :class="['px-6 py-3 text-white rounded-lg font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2 cursor-pointer', buttonClasses]"
              >
                <UIcon 
                  :name="isLoading ? 'i-heroicons-arrow-path' : (isEditMode ? 'i-heroicons-pencil-square' : 'i-heroicons-plus')" 
                  :class="['w-4 h-4', isLoading ? 'animate-spin' : '']" 
                />
                <span>{{ isLoading ? 'Saving...' : (isEditMode ? 'Update Template' : 'Create Template') }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useTemplateStore } from '../stores/templates'
import type { ProcessingTemplate } from '../stores/templates'

// Props
interface Props {
  show: boolean
  assistantType: string
  colorScheme?: 'orange' | 'teal'
  template?: ProcessingTemplate | null
}

const props = withDefaults(defineProps<Props>(), {
  template: null,
  colorScheme: 'teal'
})

// Emits
const emit = defineEmits<{
  close: []
  created: [template: ProcessingTemplate]
  updated: [template: ProcessingTemplate]
}>()

// Store
const templateStore = useTemplateStore()

// State
const isLoading = ref(false)
const formData = ref({
  title: '',
  description: '',
  content: ''
})

// Computed
const isEditMode = computed(() => !!props.template)

// Dynamic color classes based on colorScheme prop
const headerClasses = computed(() => {
  return props.colorScheme === 'orange' 
    ? 'bg-gradient-to-r from-orange-500 to-amber-500'
    : 'bg-gradient-to-r from-teal-500 to-emerald-500'
})

const focusClasses = computed(() => {
  return props.colorScheme === 'orange'
    ? 'focus:ring-orange-500 focus:border-orange-500'
    : 'focus:ring-teal-500 focus:border-teal-500'
})

const buttonClasses = computed(() => {
  return props.colorScheme === 'orange'
    ? 'bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600'
    : 'bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600'
})

// Methods
const resetForm = () => {
  formData.value = {
    title: '',
    description: '',
    content: ''
  }
}

const loadTemplate = () => {
  if (props.template) {
    formData.value = {
      title: props.template.title,
      description: props.template.description || '',
      content: props.template.content
    }
  }
}

const handleClose = () => {
  if (!isLoading.value) {
    emit('close')
  }
}

const handleBackdropClick = (event: MouseEvent) => {
  if (event.target === event.currentTarget) {
    handleClose()
  }
}

const handleSubmit = async () => {
  if (isLoading.value) return
  
  isLoading.value = true
  
  try {
    if (isEditMode.value && props.template) {
      // Update existing template
      await templateStore.updateTemplate(props.template.id, {
        title: formData.value.title.trim(),
        description: formData.value.description.trim(),
        content: formData.value.content.trim()
      })
      
      // Get updated template from store
      const updatedTemplate = templateStore.getTemplate(props.template.id)
      if (updatedTemplate) {
        emit('updated', updatedTemplate)
      }
      
    } else {
      // Create new template
      const newTemplate = await templateStore.createTemplate({
        assistantType: props.assistantType,
        title: formData.value.title.trim(),
        description: formData.value.description.trim(),
        content: formData.value.content.trim()
      })
      
      emit('created', newTemplate)
    }
    
    // Close modal and reset form
    resetForm()
    emit('close')
    
  } catch (error) {
    console.error('Error saving template:', error)
    // TODO: Show error toast or notification
  } finally {
    isLoading.value = false
  }
}

// Handle ESC key
const handleEscKey = (event: KeyboardEvent) => {
  if (event.key === 'Escape' && props.show) {
    handleClose()
  }
}

// Watchers
watch(() => props.show, (newShow) => {
  if (newShow) {
    if (props.template) {
      loadTemplate()
    } else {
      resetForm()
    }
  }
})

watch(() => props.template, () => {
  if (props.show && props.template) {
    loadTemplate()
  }
})

// Lifecycle
onMounted(() => {
  document.addEventListener('keydown', handleEscKey)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscKey)
})
</script> 