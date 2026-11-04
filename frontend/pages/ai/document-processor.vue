<template>
  <!-- Loading State while auth is being determined -->
  <div v-if="!authStore.isInitialized" class="min-h-screen bg-gradient-to-br from-orange-50 via-orange-25 to-amber-50 flex items-center justify-center">
    <div class="text-center">
      <div class="w-16 h-16 bg-gradient-to-br from-orange-500 to-amber-500 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl animate-pulse">
        <UIcon name="i-heroicons-cpu-chip" class="w-8 h-8 text-white" />
      </div>
      <h2 class="text-2xl font-bold bg-gradient-to-r from-orange-500 to-amber-500 bg-clip-text text-transparent mb-2">
        DAISY
      </h2>
      <p class="text-gray-600 font-light">Loading Document Processor...</p>
      <div class="mt-4 flex justify-center">
        <div class="w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    </div>
  </div>

  <!-- Main Content - Only show if authenticated -->
  <div v-else-if="authStore.isAuthenticated" class="min-h-screen bg-gradient-to-br from-orange-50 via-orange-25 to-amber-50">
    <!-- Unified Header -->
    <AIHeader />

    <!-- Hero Banner -->
    <div class="relative bg-gradient-to-r from-orange-800 via-orange-600 to-orange-500 border-b border-orange-700 overflow-hidden">
          <!-- Document Pattern -->
          <div class="absolute right-0 top-0 w-1/2 h-full opacity-8">
            <svg class="w-full h-full" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <pattern id="document-pattern" x="0" y="0" width="28" height="28" patternUnits="userSpaceOnUse">
                  <rect x="8" y="6" width="12" height="16" fill="none" stroke="white" stroke-width="0.5"/>
                  <line x1="10" y1="9" x2="18" y2="9" stroke="white" stroke-width="0.3"/>
                  <line x1="10" y1="12" x2="18" y2="12" stroke="white" stroke-width="0.3"/>
                  <line x1="10" y1="15" x2="16" y2="15" stroke="white" stroke-width="0.3"/>
                  <circle cx="10" cy="18" r="0.5" fill="white" opacity="0.6"/>
                </pattern>
              </defs>
              <rect width="100" height="100" fill="url(#document-pattern)"/>
            </svg>
          </div>
          
          <!-- OCR Network Background -->
          <div class="absolute right-0 top-0 w-2/3 h-full opacity-4">
            <div class="w-full h-full" style="background-image: radial-gradient(circle at 85% 25%, white 2px, transparent 2px), radial-gradient(circle at 75% 75%, white 1.5px, transparent 1.5px), radial-gradient(circle at 90% 55%, white 1px, transparent 1px); background-size: 48px 48px, 36px 36px, 64px 64px;"></div>
          </div>
          
      <UContainer class="relative z-10 py-16">
        <div class="max-w-4xl">
          <div class="flex items-center mb-6">
            <div class="w-16 h-16 bg-orange-500 rounded-2xl flex items-center justify-center mr-6 border border-orange-700">
              <UIcon name="i-heroicons-document-magnifying-glass" class="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 class="text-4xl font-bold text-white mb-2">Document Processor</h1>
              <p class="text-xl text-orange-100">Advanced Document Processing with OCR and AI</p>
            </div>
          </div>
        </div>
      </UContainer>
    </div>
    
    <UContainer class="py-8">

      <!-- Upload Form -->
      <div class="bg-white/90 backdrop-blur-sm rounded-3xl shadow-xl p-8 mb-8 border border-orange-100">
        <div class="flex items-center space-x-3 mb-6">
          <div class="w-12 h-12 bg-gradient-to-br from-orange-500 to-amber-500 rounded-2xl flex items-center justify-center">
            <UIcon name="i-heroicons-document-arrow-up" class="w-6 h-6 text-white" />
          </div>
          <h2 class="text-2xl font-bold text-gray-900">Upload Document</h2>
        </div>

        <!-- File Upload Area -->
        <div class="bg-gradient-to-br from-orange-50/50 to-amber-50/30 rounded-2xl p-8 border-2 border-dashed border-orange-300 hover:border-orange-400 transition-colors mb-6">
          <div 
            @click="triggerFileInput"
            @drop.prevent="handleFileDrop"
            @dragover.prevent
            @dragenter.prevent
            class="text-center cursor-pointer"
          >
            <div class="w-16 h-16 bg-gradient-to-br from-orange-500 to-amber-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <UIcon name="i-heroicons-cloud-arrow-up" class="w-8 h-8 text-white" />
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">
              Drop your document here
            </h3>
            <p class="text-gray-600 mb-4">
              Or click to browse and select a file
            </p>
            <div class="flex items-center justify-center space-x-4 text-sm text-gray-500">
              <div class="flex items-center space-x-1">
                <UIcon name="i-heroicons-document" class="w-4 h-4" />
                <span>.pdf</span>
              </div>
              <div class="flex items-center space-x-1">
                <UIcon name="i-heroicons-photo" class="w-4 h-4" />
                <span>.png</span>
              </div>
              <div class="flex items-center space-x-1">
                <UIcon name="i-heroicons-photo" class="w-4 h-4" />
                <span>.jpg</span>
              </div>
              <span>•</span>
              <span>Max 25MB</span>
            </div>
          </div>
        </div>

        <!-- Selected File Display -->
        <div v-if="selectedFile" class="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-4 border border-green-200 mb-6">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <!-- File Icon or Image Preview -->
              <div v-if="!isImageFile(selectedFile)" class="w-10 h-10 bg-gradient-to-br from-green-500 to-emerald-500 rounded-lg flex items-center justify-center">
                <UIcon name="i-heroicons-document-check" class="w-5 h-5 text-white" />
              </div>
              <div 
                v-else 
                class="relative w-16 h-16 rounded-lg overflow-hidden border-2 border-green-300 shadow-sm cursor-pointer group"
                @click="showImageModal = true"
              >
                <img 
                  :src="imagePreviewUrl" 
                  :alt="selectedFile.name"
                  class="w-full h-full object-cover transition-transform duration-200 group-hover:scale-110"
                />
                <!-- Hover overlay -->
                <div class="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all duration-200 flex items-center justify-center">
                  <UIcon name="i-heroicons-magnifying-glass-plus" class="w-6 h-6 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-200" />
                </div>
              </div>
              
              <div>
                <p class="font-semibold text-green-800">{{ selectedFile.name }}</p>
                <p class="text-sm text-green-600">{{ formatFileSize(selectedFile.size) }} • Ready to process</p>
                <p v-if="isImageFile(selectedFile)" class="text-xs text-green-500 italic">Click preview to view full size</p>
              </div>
            </div>
            <button
              @click="removeFile"
              class="p-2 text-green-600 hover:text-green-800 hover:bg-green-100 rounded-lg transition-colors cursor-pointer"
            >
              <UIcon name="i-heroicons-x-mark" class="w-5 h-5" />
            </button>
          </div>
        </div>

        <!-- Extraction Instructions (Optional) -->
        <div v-if="selectedFile" class="bg-gradient-to-br from-orange-50/50 to-amber-50/30 rounded-2xl p-6 border border-orange-200 mb-6">
          <div class="flex items-center space-x-3 mb-4">
            <div class="w-10 h-10 bg-gradient-to-br from-orange-500 to-amber-500 rounded-xl flex items-center justify-center">
              <UIcon name="i-heroicons-adjustments-horizontal" class="w-5 h-5 text-white" />
            </div>
            <h3 class="text-lg font-semibold text-gray-900">Instructions (Optional)</h3>
          </div>
          
          <p class="text-sm text-gray-600 mb-4">Provide specific instructions for what information to extract or the target structure required:</p>
          
          <textarea
            v-model="extractionInstructions"
            rows="8"
            class="w-full px-4 py-3 text-gray-900 bg-white border border-orange-200 rounded-xl focus:border-orange-400 focus:ring-2 focus:ring-orange-100 focus:outline-none transition-all resize-none"
            :placeholder="instructionsPlaceholder"
          ></textarea>
          
          <!-- Processing Templates -->
          <div class="mt-4">
            <div class="flex items-center justify-between mb-2">
              <p class="text-sm text-gray-600">Templates:</p>
              <button
                @click="showTemplateModal = true"
                class="inline-flex items-center space-x-1 px-2 py-1 bg-gradient-to-r from-orange-500 to-amber-500 text-white text-xs rounded-md hover:from-orange-600 hover:to-amber-600 transition-all shadow-sm hover:shadow-md cursor-pointer"
              >
                <UIcon name="i-heroicons-plus" class="w-3 h-3" />
                <span>Create</span>
              </button>
            </div>
            
            <div v-if="templateStore.getTemplatesForAssistant('document-processor').length > 0" class="grid grid-cols-2 md:grid-cols-3 gap-2">
              <div
                v-for="template in templateStore.getTemplatesForAssistant('document-processor')"
                :key="template.id"
                @click="selectTemplate(template)"
                :class="[
                  'relative text-left p-3 rounded-lg transition-all cursor-pointer group border',
                  selectedTemplateId === template.id 
                    ? 'bg-orange-100 border-orange-400 shadow-md'
                    : 'bg-white border-orange-200 hover:border-orange-300 hover:bg-orange-50'
                ]"
              >
                <!-- Edit/Delete buttons -->
                <div class="absolute top-2 right-2 flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity z-10">
                  <button
                    @click.stop="editTemplate(template)"
                    class="p-1 text-gray-400 hover:text-orange-500 rounded-md hover:bg-orange-100 transition-colors"
                  >
                    <UIcon name="i-heroicons-pencil-square" class="w-3 h-3" />
                  </button>
                  <button
                    @click.stop="deleteTemplate(template.id)"
                    class="p-1 text-gray-400 hover:text-red-500 rounded-md hover:bg-red-100 transition-colors"
                  >
                    <UIcon name="i-heroicons-trash" class="w-3 h-3" />
                  </button>
                </div>
                
                <!-- Template content -->
                <div class="pr-8">
                  <h4 class="text-xs font-semibold text-gray-900 mb-0.5">{{ template.title }}</h4>
                  <p v-if="template.description" class="text-xs text-gray-600 line-clamp-1">{{ template.description }}</p>
                </div>
              </div>
            </div>
            
                         <!-- Empty State -->
             <div v-else class="text-center py-4 px-4 bg-gray-50 border border-gray-200 rounded-lg">
               <p class="text-xs text-gray-600">No templates yet</p>
             </div>
          </div>
        </div>



        <!-- Process Button -->
        <div class="flex flex-col items-center space-y-4">
          <button
            @click="processDocument"
            :disabled="!selectedFile || loading || !hasEnoughTokens"
            :class="[
              'flex items-center justify-center px-8 py-4 rounded-xl font-semibold shadow-lg transition-all duration-300',
              selectedFile && !loading && hasEnoughTokens
                ? 'bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white hover:shadow-xl transform hover:scale-105 cursor-pointer'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            ]"
          >
            <span v-if="loading">Processing Document...</span>
            <span v-else-if="!selectedFile">Select a file first</span>
            <span v-else-if="!hasEnoughTokens">Insufficient tokens ({{ tokenStore.tokens }}/{{ requiredTokens }})</span>
            <span v-else>Process Document ({{ requiredTokens }} token{{ requiredTokens !== 1 ? 's' : '' }})</span>
          </button>
        </div>

        <!-- Hidden File Input -->
        <input
          ref="fileInput"
          type="file"
          accept=".pdf,.png,.jpg,.jpeg"
          @change="handleFileSelect"
          class="hidden"
        />
      </div>

      <!-- Loading Animation -->
      <div v-if="loading" class="bg-white/90 backdrop-blur-sm rounded-3xl shadow-xl p-8 mb-8 border border-orange-100">
        <div class="text-center py-12">
          <div class="flex justify-center mb-6">
            <div class="relative">
              <div class="animate-spin rounded-full h-20 w-20 border-4 border-orange-200 border-t-orange-600"></div>
              <div class="absolute inset-0 flex items-center justify-center">
                <UIcon name="i-heroicons-document-magnifying-glass" class="text-2xl text-orange-600" />
              </div>
            </div>
          </div>
          
          <div class="flex items-center justify-center space-x-2 mb-2">
            <UIcon name="i-heroicons-sparkles" class="text-xl text-orange-600" />
            <h3 class="text-2xl font-bold bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent">Processing Document</h3>
          </div>
          <p class="text-gray-600 font-light mb-8">Extracting text content using OCR and AI...</p>
          
          <!-- Progress Animation -->
          <div class="max-w-md mx-auto">
            <div class="bg-orange-100 rounded-full h-3 shadow-inner">
              <div 
                class="bg-gradient-to-r from-orange-500 to-amber-500 h-3 rounded-full transition-all duration-500 shadow-lg" 
                :style="{ width: progress + '%' }"
              ></div>
            </div>
            <div class="flex items-center justify-center space-x-2 mt-4">
              <UIcon name="i-heroicons-cpu-chip" class="text-sm text-orange-500" />
              <p class="text-sm text-gray-600 font-medium">{{ progressText }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Document Digitalizer Results -->
      <div v-if="extractedText" class="bg-white/90 backdrop-blur-sm rounded-3xl shadow-xl p-8 mb-8 border border-orange-100">
        <div class="flex items-center justify-between mb-8">
          <div class="flex items-center space-x-3">
            <div class="w-12 h-12 bg-gradient-to-br from-orange-500 to-amber-500 rounded-2xl flex items-center justify-center">
              <UIcon name="i-heroicons-check-circle" class="w-6 h-6 text-white" />
            </div>
            <div>
              <h3 class="text-2xl font-bold bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent">Text Extracted Successfully</h3>
              <p v-if="processingInfo" class="text-sm text-gray-600 mt-1 flex items-center space-x-1">
                <UIcon name="i-heroicons-information-circle" class="w-4 h-4 text-orange-500" />
                <span>{{ processingInfo }}</span>
              </p>
            </div>
          </div>
          <div class="flex items-center space-x-3">
            <button
              @click="downloadPDF"
              :disabled="generatingPDF"
              class="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 disabled:from-gray-400 disabled:to-gray-500 text-white font-medium rounded-lg shadow-lg transition-all cursor-pointer disabled:cursor-not-allowed"
            >
              <UIcon :name="generatingPDF ? 'i-heroicons-arrow-path' : 'i-heroicons-document-arrow-down'" class="w-4 h-4" :class="{ 'animate-spin': generatingPDF }" />
              <span v-if="generatingPDF">Generating PDF...</span>
              <span v-else>Download PDF</span>
            </button>
            <div class="relative">
              <button
                @click="copyToClipboard"
                class="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white font-medium rounded-lg shadow-lg transition-all cursor-pointer"
              >
                <UIcon name="i-heroicons-clipboard-document" class="w-4 h-4" />
                <span>Copy</span>
              </button>
              <!-- Copy Confirmation Text -->
              <div v-if="copyConfirmation" class="absolute top-full mt-2 left-0 z-50 text-sm text-green-600 font-medium flex items-center space-x-1 whitespace-nowrap bg-white px-3 py-2 rounded-lg shadow-lg border border-green-200">
                <UIcon name="i-heroicons-check-circle" class="w-4 h-4" />
                <span>Text copied to clipboard!</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Extracted Text Content -->
        <div class="bg-gradient-to-br from-orange-50/50 to-amber-50/30 rounded-2xl p-6 border border-orange-200">
          <div class="prose max-w-none" v-html="extractedText"></div>
        </div>
      </div>

      <!-- Error State -->
      <div v-if="error" class="bg-gradient-to-br from-red-50/90 to-rose-50/80 backdrop-blur-sm border border-red-200 rounded-2xl shadow-xl p-6 mb-8">
        <div class="flex items-start justify-between">
          <div class="flex items-start space-x-3">
            <UIcon name="i-heroicons-exclamation-triangle" class="text-2xl text-red-600 mt-1" />
            <div>
              <h3 class="text-lg font-bold text-red-800 mb-2">Processing Failed</h3>
              <p class="text-red-600 text-sm leading-relaxed">{{ error }}</p>
            </div>
          </div>
          <button
            @click="error = ''"
            class="p-2 text-red-400 hover:text-red-600 hover:bg-red-100 rounded-lg transition-colors cursor-pointer"
          >
            <UIcon name="i-heroicons-x-mark" class="w-5 h-5" />
          </button>
        </div>
      </div>

      <!-- Image Modal -->
      <div v-if="showImageModal && imagePreviewUrl" class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click="showImageModal = false">
        <div class="relative max-w-6xl max-h-[90vh] w-full h-full flex items-center justify-center" @click.stop>
          <!-- Close Button -->
          <button
            @click="showImageModal = false"
            class="absolute -top-4 -right-4 z-20 w-12 h-12 bg-white rounded-full flex items-center justify-center text-gray-600 hover:text-gray-800 hover:bg-gray-50 transition-all shadow-lg hover:shadow-xl cursor-pointer"
          >
            <UIcon name="i-heroicons-x-mark" class="w-6 h-6" />
          </button>
          
          <!-- Image -->
          <img 
            :src="imagePreviewUrl" 
            :alt="selectedFile?.name || 'Preview'"
            class="max-w-full max-h-full object-contain rounded-lg shadow-2xl"
          />
          
          <!-- Image Info -->
          <div class="absolute bottom-4 left-4 bg-black/60 backdrop-blur-sm text-white px-4 py-2 rounded-lg">
            <p class="font-semibold">{{ selectedFile?.name }}</p>
            <p class="text-sm opacity-90">{{ formatFileSize(selectedFile?.size || 0) }}</p>
          </div>
        </div>
      </div>

      <!-- Tips Section -->
      <div class="mt-8 border border-orange-200 rounded-2xl shadow-sm p-8" style="background-color: rgba(251, 146, 60, 0.25);">
        <div class="flex items-center space-x-2 mb-4">
          <UIcon name="i-heroicons-light-bulb" class="text-2xl text-orange-800" />
          <h3 class="text-xl font-bold text-orange-900">Tips for Better Results</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-3">
            <h4 class="font-semibold text-orange-800">Document Quality</h4>
            <ul class="text-sm text-orange-700 space-y-1">
              <li>• Use high-quality, clear images or PDFs</li>
              <li>• Ensure text is readable and not rotated</li>
              <li>• Avoid documents with complex layouts</li>
            </ul>
          </div>
          <div class="space-y-3">
            <h4 class="font-semibold text-orange-800">Extraction Instructions</h4>
            <ul class="text-sm text-orange-700 space-y-1">
              <li>• Specify exactly what information you need</li>
              <li>• Mention the desired output format</li>
              <li>• Include structure requirements if needed</li>
            </ul>
          </div>
        </div>
      </div>
    </UContainer>
    
    <!-- Global Footer -->
    <GlobalFooter />
    
    <!-- Template Modal -->
    <TemplateModal
      :show="showTemplateModal"
      :assistant-type="'document-processor'"
      :color-scheme="'orange'"
      :template="editingTemplate"
      @close="closeTemplateModal"
      @created="onTemplateCreated"
      @updated="onTemplateUpdated"
    />
  </div>
</template>

<script setup>
import { nextTick } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useTokenStore } from '~/stores/tokens'
import { useTemplateStore } from '~/stores/templates'
import { useAdobeTracking } from '~/composables/useAdobeTracking'
import TemplateModal from '~/components/TemplateModal.vue'

// Stores
const authStore = useAuthStore()
const tokenStore = useTokenStore()
const templateStore = useTemplateStore()

// Adobe Tracking
const { trackButtonClick, trackTokenUsage } = useAdobeTracking()

// Handle ESC key to close image modal
const handleEscapeKey = (event) => {
  if (event.key === 'Escape' && showImageModal.value) {
    showImageModal.value = false
  }
}

// Client-side auth check
onMounted(async () => {
  if (!authStore.isInitialized) {
    await authStore.init()
  }
  
  if (!authStore.isAuthenticated) {
    await navigateTo('/login')
    return
  }

  // Initialize token store after auth
  if (authStore.isAuthenticated && authStore.user && !tokenStore.isInitialized) {
    try {
      await tokenStore.init()
    } catch (error) {
      console.error('Document Processor: Error initializing token store:', error)
    }
  }
  
  // Initialize template store
  if (!templateStore.isInitialized) {
    await templateStore.init()
  }
  
  // Add keyboard event listener
  document.addEventListener('keydown', handleEscapeKey)
})

// Clean up on unmount
onBeforeUnmount(() => {
  // Clean up image preview URL
  if (imagePreviewUrl.value) {
    URL.revokeObjectURL(imagePreviewUrl.value)
  }
  
  // Remove keyboard event listener
  document.removeEventListener('keydown', handleEscapeKey)
})

// Watch for auth changes
watch(() => authStore.isAuthenticated, (isAuthenticated) => {
  if (!isAuthenticated) {
    navigateTo('/login')
  }
})

// Refs
const fileInput = ref(null)
const selectedFile = ref(null)
const extractionInstructions = ref('')
const loading = ref(false)
const error = ref('')
const extractedText = ref('')
const processingInfo = ref('')
const progress = ref(0)
const progressText = ref('')
const copyConfirmation = ref(false)
const generatingPDF = ref(false)
const imagePreviewUrl = ref('')
const showImageModal = ref(false)

// Template state
const showTemplateModal = ref(false)
const editingTemplate = ref(null)
const selectedTemplateId = ref(null)

// Removed old prompt templates - now using user-created templates from templateStore



// Token logic for Document Processor
const requiredTokens = computed(() => {
  return tokenStore.getTokenCost('document-processor')
})

const hasEnoughTokens = computed(() => {
  return tokenStore.tokens >= requiredTokens.value
})

// Dynamic placeholder for instructions
const instructionsPlaceholder = computed(() => {
  if (extractionInstructions.value === '') {
    return 'Example: Extract all contact information (names, emails, phone numbers) and format as a structured list with clear sections for each contact.'
  }
  return ''
})

// Removed old template handling methods - now using templateStore functions

const triggerFileInput = () => {
  if (!loading.value) {
    fileInput.value?.click()
  }
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    validateAndSetFile(file)
  }
}

const handleFileDrop = (event) => {
  const file = event.dataTransfer.files[0]
  if (file) {
    validateAndSetFile(file)
  }
}

const validateAndSetFile = (file) => {
  // Check file type
  const allowedTypes = ['application/pdf', 'image/png', 'image/jpeg', 'image/jpg']
  const allowedExtensions = ['.pdf', '.png', '.jpg', '.jpeg']
  
  const hasValidType = allowedTypes.includes(file.type)
  const hasValidExtension = allowedExtensions.some(ext => file.name.toLowerCase().endsWith(ext))
  
  if (!hasValidType && !hasValidExtension) {
    error.value = 'Please select a PDF, PNG, or JPG file.'
    return
  }

  // Check file size (25MB limit)
  if (file.size > 25 * 1024 * 1024) {
    error.value = 'File size must be less than 25MB.'
    return
  }

  selectedFile.value = file
  error.value = ''
  
  // Create image preview URL if it's an image
  if (isImageFile(file)) {
    imagePreviewUrl.value = URL.createObjectURL(file)
  } else {
    imagePreviewUrl.value = ''
  }
}

const isImageFile = (file) => {
  const imageTypes = ['image/png', 'image/jpeg', 'image/jpg']
  const imageExtensions = ['.png', '.jpg', '.jpeg']
  
  return imageTypes.includes(file.type) || 
         imageExtensions.some(ext => file.name.toLowerCase().endsWith(ext))
}

const removeFile = () => {
  // Clean up image preview URL if it exists
  if (imagePreviewUrl.value) {
    URL.revokeObjectURL(imagePreviewUrl.value)
    imagePreviewUrl.value = ''
  }
  
  selectedFile.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const processDocument = async () => {
  if (!selectedFile.value || loading.value) return

  // Check if user has enough tokens
  if (!hasEnoughTokens.value) {
    error.value = `You need ${requiredTokens.value} token(s) to process documents. You currently have ${tokenStore.tokens} tokens.`
    return
  }

  // Track processing start with file metadata
  trackButtonClick('Process Document Processor', {
    fileType: selectedFile.value.type,
    fileName: selectedFile.value.name.split('.').pop(), // file extension
    fileSizeMB: Math.round((selectedFile.value.size / 1024 / 1024) * 100) / 100,
    hasInstructions: extractionInstructions.value.length > 0,
    instructionsLength: extractionInstructions.value.length,
    tokensRequired: requiredTokens.value,
    tokensAvailable: tokenStore.tokens
  })

      loading.value = true
    error.value = ''
    extractedText.value = ''
    processingInfo.value = ''
    progress.value = 0

  try {
    // Start progress animation
    const progressInterval = setInterval(() => {
      if (progress.value < 90) {
        progress.value += Math.random() * 10
        updateProgressText()
      }
    }, 1000)

    // Create FormData
    const formData = new FormData()
    formData.append('document_file', selectedFile.value)
    if (extractionInstructions.value.trim()) {
      formData.append('instruction', extractionInstructions.value.trim())
    }

    // Make authenticated API call
    const { authenticatedEndpointRequest, apiEndpoints } = await import('~/config/api.config')

    
    const response = await authenticatedEndpointRequest(apiEndpoints.documentProcessor, {
      method: 'POST',
      body: formData
    })

    // Complete progress
    clearInterval(progressInterval)
    progress.value = 100
    progressText.value = 'Complete!'

    // Set the extracted text
    if (response) {
      let textContent = ''
      if (typeof response === 'string') {
        textContent = response
      } else if (response.extracted_text) {
        textContent = response.extracted_text
        // Also extract processing info if available
        if (response.processing_info) {
          processingInfo.value = response.processing_info
        }
      } else if (response.text) {
        textContent = response.text
      } else {
        throw new Error('Invalid response format - missing text content')
      }
      
      // Format the extracted text as HTML
      extractedText.value = formatExtractedText(textContent)
      
      // Deduct tokens and track usage
      try {
        await tokenStore.useTokens(requiredTokens.value)
        
        // Track token usage with Adobe Analytics
        trackTokenUsage(requiredTokens.value, 'document_processor', {
          fileType: selectedFile.value?.type || 'unknown',
          fileName: selectedFile.value?.name?.split('.').pop() || 'unknown',
          fileSizeMB: Math.round((selectedFile.value.size / 1024 / 1024) * 100) / 100,
          hasInstructions: extractionInstructions.value.length > 0,
          instructionsLength: extractionInstructions.value.length,
          textLength: textContent.length,
          success: true
        })
      } catch (tokenError) {
        console.error('Error deducting tokens:', tokenError)
      }
      
      // Show success notification
      const toast = useToast()
      toast.add({
        title: 'Text Extracted Successfully',
        description: `Your document has been processed successfully. ${requiredTokens.value} token(s) used.`,
        color: 'green'
      })
    } else {
      throw new Error('Invalid response format - empty response')
    }

  } catch (err) {
    console.error('Error processing document:', err)
    
    // Track API error with Adobe Analytics
    const { trackError } = useAdobeTracking()
    trackError('api_document_processor_failed', 'Document Processor API request failed', {
      errorMessage: err.message || err.toString(),
      errorCode: err.status || err.statusCode || 'unknown',
      errorType: err.name || 'APIError',
      endpoint: 'documentProcessor',
      requestData: {
        fileName: selectedFile.value?.name || 'unknown',
        fileType: selectedFile.value?.type || 'unknown',
        fileSizeMB: selectedFile.value ? Math.round((selectedFile.value.size / 1024 / 1024) * 100) / 100 : 0,
        hasInstructions: !!extractionInstructions.value.trim(),
        instructionsLength: extractionInstructions.value.length,
        tokensRequired: requiredTokens.value,
        tokensAvailable: tokenStore.tokens
      },
      userAgent: window.navigator?.userAgent || 'unknown',
      timestamp: new Date().toISOString()
    })
    
    error.value = err.message || 'Failed to process document. Please try again.'
  } finally {
    loading.value = false
    setTimeout(() => {
      progress.value = 0
      progressText.value = ''
    }, 2000)
  }
}

const updateProgressText = () => {
  const texts = [
    'Uploading document...',
    'Analyzing file format...',
    'Performing OCR...',
    'Extracting text content...',
    'Processing with AI...',
    'Applying instructions...',
    'Finalizing results...'
  ]
  const index = Math.floor((progress.value / 100) * (texts.length - 1))
  progressText.value = texts[index] || texts[0]
}



const isMarkdownContent = (text) => {
  // Check for common Markdown patterns
  const markdownPatterns = [
    /^#{1,6}\s+/m,           // Headers (# ## ###)
    /\*\*.*?\*\*/,           // Bold text
    /\*.*?\*/,               // Italic text
    /`.*?`/,                 // Inline code
    /```[\s\S]*?```/,        // Code blocks
    /^\s*[-*+]\s+/m,         // Unordered lists
    /^\s*\d+\.\s+/m,         // Ordered lists
    /\[.*?\]\(.*?\)/,        // Links
    /\|.*\|/,                // Tables
    /^>\s+/m,                // Blockquotes
    /^---+$/m,               // Horizontal rules
  ]
  
  return markdownPatterns.some(pattern => pattern.test(text))
}

const parseMarkdownToHTML = (text) => {
  let html = text
  
  // Headers (## Header -> <h2>Header</h2>)
  html = html.replace(/^#{6}\s+(.+)$/gm, '<h6>$1</h6>')
  html = html.replace(/^#{5}\s+(.+)$/gm, '<h5>$1</h5>')
  html = html.replace(/^#{4}\s+(.+)$/gm, '<h4>$1</h4>')
  html = html.replace(/^#{3}\s+(.+)$/gm, '<h3>$1</h3>')
  html = html.replace(/^#{2}\s+(.+)$/gm, '<h2>$1</h2>')
  html = html.replace(/^#{1}\s+(.+)$/gm, '<h1>$1</h1>')
  
  // Bold and Italic
  html = html.replace(/\*\*\*(.*?)\*\*\*/g, '<strong><em>$1</em></strong>')
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>')
  
  // Code blocks (```code```)
  html = html.replace(/```([\s\S]*?)```/g, '<pre class="bg-gray-100 p-4 rounded-lg overflow-x-auto"><code>$1</code></pre>')
  
  // Inline code (`code`)
  html = html.replace(/`([^`]+)`/g, '<code class="bg-gray-100 px-2 py-1 rounded text-sm">$1</code>')
  
  // Links [text](url)
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-blue-600 hover:text-blue-800 underline" target="_blank" rel="noopener noreferrer">$1</a>')
  
  // Unordered lists
  html = html.replace(/^\s*[-*+]\s+(.+)$/gm, '<li>$1</li>')
  html = html.replace(/(<li>.*<\/li>)/s, '<ul class="list-disc pl-6 space-y-1">$1</ul>')
  
  // Ordered lists
  html = html.replace(/^\s*(\d+)\.\s+(.+)$/gm, '<li>$2</li>')
  // This is a bit more complex for ordered lists, we'll handle it differently
  
  // Blockquotes
  html = html.replace(/^>\s+(.+)$/gm, '<blockquote class="border-l-4 border-gray-300 pl-4 italic text-gray-700">$1</blockquote>')
  
  // Horizontal rules
  html = html.replace(/^---+$/gm, '<hr class="border-gray-300 my-4">')
  
  // Basic table support (simple)
  html = html.replace(/\|(.+)\|/g, (match, content) => {
    const cells = content.split('|').map(cell => cell.trim())
    return '<tr>' + cells.map(cell => `<td class="border px-2 py-1">${cell}</td>`).join('') + '</tr>'
  })
  
  // Convert line breaks to paragraphs for non-list content
  const lines = html.split('\n')
  let result = []
  let currentParagraph = []
  
  for (let line of lines) {
    line = line.trim()
    if (line === '') {
      if (currentParagraph.length > 0) {
        const paragraphText = currentParagraph.join(' ')
        if (!paragraphText.match(/^<[h1-6|ul|ol|li|blockquote|hr|pre|table]/)) {
          result.push(`<p>${paragraphText}</p>`)
        } else {
          result.push(paragraphText)
        }
        currentParagraph = []
      }
    } else if (line.match(/^<[h1-6|ul|ol|blockquote|hr|pre|table]/)) {
      if (currentParagraph.length > 0) {
        result.push(`<p>${currentParagraph.join(' ')}</p>`)
        currentParagraph = []
      }
      result.push(line)
    } else {
      currentParagraph.push(line)
    }
  }
  
  // Handle remaining paragraph
  if (currentParagraph.length > 0) {
    const paragraphText = currentParagraph.join(' ')
    if (!paragraphText.match(/^<[h1-6|ul|ol|li|blockquote|hr|pre|table]/)) {
      result.push(`<p>${paragraphText}</p>`)
    } else {
      result.push(paragraphText)
    }
  }
  
  return result.join('\n')
}

const formatExtractedText = (text) => {
  // Check if the text contains Markdown syntax
  if (isMarkdownContent(text)) {
    return parseMarkdownToHTML(text)
  }
  
  // Fallback to original plain text formatting
  return text
    .split('\n\n')
    .map(paragraph => {
      if (paragraph.trim()) {
        // Check if it's a header (contains colon or is all caps and short)
        if (paragraph.includes(':') && paragraph.split(':')[0].length < 50) {
          const [title, ...content] = paragraph.split(':')
          return `<h3>${title.trim()}:</h3>${content.length ? `<p>${content.join(':').trim()}</p>` : ''}`
        }
        // Check if it's a list item
        else if (paragraph.trim().startsWith('•') || paragraph.trim().startsWith('-') || paragraph.trim().startsWith('*')) {
          const items = paragraph.split('\n').filter(line => line.trim())
          return `<ul>${items.map(item => `<li>${item.replace(/^[•\-\*]\s*/, '').trim()}</li>`).join('')}</ul>`
        }
        // Regular paragraph
        else {
          return `<p>${paragraph.trim()}</p>`
        }
      }
      return ''
    })
    .filter(Boolean)
    .join('')
}

const copyToClipboard = async () => {
  if (!extractedText.value) return

  try {
    // Track copy action
    trackButtonClick('Copy Document Processor', {
      fileType: selectedFile.value?.type || 'unknown',
      fileName: selectedFile.value?.name?.split('.').pop() || 'unknown',
      textLength: extractedText.value.length,
      copyMethod: 'clipboard'
    })

    // Convert HTML to plain text
    const tempDiv = document.createElement('div')
    tempDiv.innerHTML = extractedText.value
    const textContent = tempDiv.textContent || tempDiv.innerText || ''
    
    await navigator.clipboard.writeText(textContent)
    copyConfirmation.value = true
    // Hide the confirmation after 3 seconds
    setTimeout(() => {
      copyConfirmation.value = false
    }, 3000)
  } catch (err) {
    console.error('Failed to copy to clipboard:', err)
  }
}

const downloadPDF = async () => {
  if (!extractedText.value) return

  generatingPDF.value = true
  
  try {
    // Track PDF download action
    trackButtonClick('Download Document Processor PDF', {
      fileType: selectedFile.value?.type || 'unknown',
      fileName: selectedFile.value?.name?.split('.').pop() || 'unknown',
      textLength: extractedText.value.length,
      downloadFormat: 'pdf'
    })

    // Dynamic import of jspdf
    const { jsPDF } = await import('jspdf')

    // Create new PDF document
    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4'
    })

    // Page settings
    const pageWidth = pdf.internal.pageSize.getWidth()
    const pageHeight = pdf.internal.pageSize.getHeight()
    const margin = 20
    const maxWidth = pageWidth - (margin * 2)
    let currentY = margin

    // Add title
    pdf.setFontSize(20)
    pdf.setFont(undefined, 'bold')
    pdf.setTextColor(249, 115, 22) // Orange color
    pdf.text('Document Processor Results', pageWidth / 2, currentY, { align: 'center' })
    
    currentY += 10
    
    // Add subtitle
    pdf.setFontSize(10)
    pdf.setFont(undefined, 'normal')
    pdf.setTextColor(107, 114, 128) // Gray color
    const subtitle = `Extracted on ${new Date().toLocaleDateString()} • ${selectedFile.value?.name || 'Document'}`
    pdf.text(subtitle, pageWidth / 2, currentY, { align: 'center' })
    
    currentY += 15
    
    // Add line separator
    pdf.setDrawColor(249, 115, 22) // Orange color
    pdf.setLineWidth(0.5)
    pdf.line(margin, currentY, pageWidth - margin, currentY)
    
    currentY += 10

    // Convert HTML to plain text while preserving structure
    const tempDiv = document.createElement('div')
    tempDiv.innerHTML = extractedText.value
    
    // Process content by element type
    const processElement = (element, isNested = false) => {
      const tagName = element.tagName?.toLowerCase()
      let text = ''
      
      if (tagName === 'h1' || tagName === 'h2' || tagName === 'h3') {
        text = element.textContent?.trim() || ''
        if (text) {
          // Check if we need a new page
          if (currentY > pageHeight - 30) {
            pdf.addPage()
            currentY = margin
          }
          
          currentY += 5
          pdf.setFontSize(14)
          pdf.setFont(undefined, 'bold')
          pdf.setTextColor(31, 41, 55) // Dark gray
          
          const lines = pdf.splitTextToSize(text, maxWidth)
          pdf.text(lines, margin, currentY)
          currentY += lines.length * 6 + 5
        }
      } else if (tagName === 'p') {
        text = element.textContent?.trim() || ''
        if (text) {
          // Check if we need a new page
          if (currentY > pageHeight - 20) {
            pdf.addPage()
            currentY = margin
          }
          
          pdf.setFontSize(11)
          pdf.setFont(undefined, 'normal')
          pdf.setTextColor(55, 65, 81) // Gray
          
          const lines = pdf.splitTextToSize(text, maxWidth)
          pdf.text(lines, margin + (isNested ? 5 : 0), currentY)
          currentY += lines.length * 5 + 3
        }
      } else if (tagName === 'ul' || tagName === 'ol') {
        currentY += 2
        Array.from(element.children).forEach((li, index) => {
          const liText = li.textContent?.trim() || ''
          if (liText) {
            // Check if we need a new page
            if (currentY > pageHeight - 15) {
              pdf.addPage()
              currentY = margin
            }
            
            pdf.setFontSize(11)
            pdf.setFont(undefined, 'normal')
            pdf.setTextColor(55, 65, 81)
            
            const bullet = tagName === 'ul' ? '• ' : `${index + 1}. `
            const fullText = bullet + liText
            const lines = pdf.splitTextToSize(fullText, maxWidth - 5)
            pdf.text(lines, margin + 5, currentY)
            currentY += lines.length * 5 + 2
          }
        })
        currentY += 3
      } else if (tagName === 'strong' || tagName === 'b') {
        // Handle inline bold (will be processed by parent)
        return element.textContent?.trim() || ''
      } else {
        // Handle other elements or text nodes
        text = element.textContent?.trim() || ''
        if (text && element.nodeType === 1) {
          pdf.setFontSize(11)
          pdf.setFont(undefined, 'normal')
          pdf.setTextColor(55, 65, 81)
          
          const lines = pdf.splitTextToSize(text, maxWidth)
          pdf.text(lines, margin, currentY)
          currentY += lines.length * 5 + 3
        }
      }
    }

    // Process all child elements
    Array.from(tempDiv.children).forEach(element => {
      processElement(element)
    })

    // If no structured content, add as plain text
    if (tempDiv.children.length === 0) {
      const plainText = tempDiv.textContent?.trim() || extractedText.value.replace(/<[^>]*>/g, '')
      
      pdf.setFontSize(11)
      pdf.setFont(undefined, 'normal')
      pdf.setTextColor(55, 65, 81)
      
      const lines = pdf.splitTextToSize(plainText, maxWidth)
      lines.forEach(line => {
        if (currentY > pageHeight - 20) {
          pdf.addPage()
          currentY = margin
        }
        pdf.text(line, margin, currentY)
        currentY += 5
      })
    }

    // Save the PDF
    pdf.save(`document-processor-${Date.now()}.pdf`)

    // Show success notification
    const toast = useToast()
    toast.add({
      title: 'PDF Generated',
      description: 'Your extracted text has been downloaded as PDF with copyable text.',
      color: 'green'
    })

  } catch (error) {
    console.error('PDF generation failed:', error)
    
    // Show error notification
    const toast = useToast()
    toast.add({
      title: 'PDF Generation Failed',
      description: 'There was an error generating the PDF. Please try again.',
      color: 'red'
    })
  } finally {
    generatingPDF.value = false
  }
}

// Template functions
const selectTemplate = async (template) => {
  
  // Visual feedback - mark template as selected
  selectedTemplateId.value = template.id
  
  // Force reactivity update
  extractionInstructions.value = template.content
  
  // Use nextTick to ensure DOM is updated
  await nextTick()
  
  // Focus the textarea to show the change
  const textarea = document.querySelector('textarea[rows="8"]')
  if (textarea) {
    textarea.focus()
    // Scroll to the start of the textarea to show the new content
    textarea.scrollTop = 0
    textarea.blur() // Trigger any change events
  }
  
  // Clear selection after short delay
  setTimeout(() => {
    selectedTemplateId.value = null
  }, 1000)
  
  // Track template usage
  trackButtonClick('Use Processing Template', {
    templateId: template.id,
    templateTitle: template.title,
    templateLength: template.content.length
  })
  
}

const editTemplate = (template) => {
  editingTemplate.value = template
  showTemplateModal.value = true
}

const deleteTemplate = async (templateId) => {
  if (!confirm('Are you sure you want to delete this template? This action cannot be undone.')) {
    return
  }
  
  try {
    await templateStore.deleteTemplate(templateId)
    
    // Track template deletion
    trackButtonClick('Delete Processing Template', {
      templateId,
      remainingTemplates: templateStore.userTemplates.length
    })
    
  } catch (error) {
    console.error('Error deleting template:', error)
    trackError('template_delete_failed', 'Failed to delete processing template', {
      templateId,
      errorMessage: error.message || error.toString()
    })
  }
}

const closeTemplateModal = () => {
  showTemplateModal.value = false
  editingTemplate.value = null
}

const onTemplateCreated = (template) => {
  // Track template creation
  trackButtonClick('Create Processing Template', {
    templateId: template.id,
    templateTitle: template.title,
    templateLength: template.content.length,
    hasDescription: !!template.description
  })
}

const onTemplateUpdated = (template) => {
  // Track template update
  trackButtonClick('Update Processing Template', {
    templateId: template.id,
    templateTitle: template.title,
    templateLength: template.content.length,
    hasDescription: !!template.description
  })
}

const formatDate = (date) => {
  if (!date) return ''
  
  const now = new Date()
  const targetDate = date.toDate ? date.toDate() : new Date(date)
  const diffMs = now - targetDate
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) {
    return 'Today'
  } else if (diffDays === 1) {
    return 'Yesterday'
  } else if (diffDays < 7) {
    return `${diffDays} days ago`
  } else {
    return targetDate.toLocaleDateString()
  }
}

// SEO
useHead({
  title: 'Document Processor - DAISY',
  meta: [
    {
      name: 'description',
      content: 'Advanced document processing with OCR and AI. Upload PDFs, images, and documents to extract and process text content with custom instructions.'
    }
  ]
})
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.prose {
  color: #374151;
}

.prose h3 {
  color: #1f2937;
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

.prose ul {
  margin: 0.5rem 0;
  padding-left: 1.5rem;
}

.prose li {
  margin: 0.25rem 0;
}

.prose strong {
  color: #111827;
  font-weight: 600;
}

.prose p {
  margin: 0.75rem 0;
  line-height: 1.6;
}

/* Enhanced Document Digitalizer Styles */
:deep(.prose h3),
.prose h3 {
  font-size: 1.25rem !important;
  font-weight: 600 !important;
  color: #1f2937 !important;
  margin-top: 1.75rem !important;
  margin-bottom: 0.875rem !important;
  padding-bottom: 0.5rem !important;
  border-bottom: 1px solid #e5e7eb !important;
}

:deep(.prose p),
.prose p {
  margin: 12px 0 !important;
  line-height: 1.7 !important;
  font-size: 1rem !important;
}

:deep(.prose ul),
.prose ul {
  margin: 15px 0 !important;
  padding-left: 20px !important;
}

:deep(.prose li),
.prose li {
  margin: 6px 0 !important;
  line-height: 1.6 !important;
  font-size: 0.875rem !important;
}
</style> 