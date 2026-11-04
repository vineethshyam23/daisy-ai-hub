<template>
  <!-- Loading State -->
  <div v-if="!authStore.isInitialized" class="min-h-screen bg-gradient-to-br from-green-50 via-green-25 to-emerald-50 flex items-center justify-center">
    <div class="text-center">
      <div class="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl animate-pulse">
        <UIcon name="i-heroicons-cpu-chip" class="w-8 h-8 text-white" />
      </div>
      <h2 class="text-2xl font-bold bg-gradient-to-r from-green-500 to-emerald-500 bg-clip-text text-transparent mb-2">
        DAISY
      </h2>
      <p class="text-gray-600 font-light">Loading Invoice Validator...</p>
      <div class="mt-4 flex justify-center">
        <div class="w-8 h-8 border-4 border-green-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    </div>
  </div>

  <!-- Main Content -->
  <div v-else-if="authStore.isAuthenticated" class="min-h-screen bg-gradient-to-br from-green-50 via-green-25 to-emerald-50">
    <AIHeader />
    
    <!-- Hero Banner -->
    <div class="relative bg-gradient-to-r from-green-800 via-green-600 to-green-500 border-b border-green-700 overflow-hidden">
      <!-- Background Pattern -->
      <div class="absolute right-0 top-0 w-1/2 h-full opacity-8">
        <svg class="w-full h-full" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="invoice-pattern" x="0" y="0" width="28" height="28" patternUnits="userSpaceOnUse">
              <rect x="6" y="6" width="16" height="12" fill="none" stroke="white" stroke-width="0.5"/>
              <line x1="8" y1="9" x2="20" y2="9" stroke="white" stroke-width="0.3"/>
              <line x1="8" y1="12" x2="18" y2="12" stroke="white" stroke-width="0.3"/>
              <line x1="8" y1="15" x2="16" y2="15" stroke="white" stroke-width="0.3"/>
              <circle cx="18" cy="20" r="2" fill="none" stroke="white" stroke-width="0.4"/>
              <path d="M16,20 L20,20 M18,18 L18,22" stroke="white" stroke-width="0.3"/>
            </pattern>
          </defs>
          <rect width="100" height="100" fill="url(#invoice-pattern)"/>
        </svg>
      </div>
      
      <UContainer class="relative z-10 py-16">
        <div class="max-w-4xl">
          <div class="flex items-center mb-6">
            <div class="w-16 h-16 bg-green-500 rounded-2xl flex items-center justify-center mr-6 border border-green-700">
              <UIcon name="i-heroicons-calculator" class="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 class="text-4xl font-bold text-white mb-2">Invoice Validator - SCO</h1>
              <p class="text-xl text-green-100">Supply-Chain Operations: Validate and Compare MLG Invoice & Jira Files</p>
            </div>
          </div>
        </div>
      </UContainer>
    </div>

    <UContainer class="py-8">
      <!-- Upload Form -->
      <div class="bg-white/90 backdrop-blur-sm rounded-3xl shadow-xl p-8 mb-8 border border-green-100">
        <div class="flex items-center space-x-3 mb-6">
          <div class="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center">
            <UIcon name="i-heroicons-document-arrow-up" class="w-6 h-6 text-white" />
          </div>
          <h2 class="text-2xl font-bold text-gray-900">Upload Files</h2>
        </div>

        <!-- File Upload Areas -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <!-- Invoice File Upload -->
          <div class="bg-gradient-to-br from-green-50/50 to-emerald-50/30 rounded-2xl p-6 border-2 border-dashed border-green-300 hover:border-green-400 transition-colors">
            <div 
              @click="triggerFileInput('invoice')"
              @drop.prevent="handleFileDrop($event, 'invoice')"
              @dragover.prevent
              @dragenter.prevent
              class="text-center cursor-pointer"
            >
              <div class="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl flex items-center justify-center mx-auto mb-3">
                <UIcon name="i-heroicons-document-text" class="w-6 h-6 text-white" />
              </div>
              <h3 class="text-lg font-semibold text-gray-900 mb-2">MLG Invoice File</h3>
              <p class="text-gray-600 mb-3">Drop your invoice Excel file here</p>
              <div class="flex items-center justify-center space-x-2 text-sm text-gray-500">
                <UIcon name="i-heroicons-table-cells" class="w-4 h-4" />
                <span>.xlsx, .xls</span>
              </div>
            </div>
            
            <!-- Selected Invoice File -->
            <div v-if="invoiceFile" class="mt-4 bg-green-100 rounded-lg p-3 border border-green-200">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <UIcon name="i-heroicons-document-check" class="w-5 h-5 text-green-600" />
                  <div>
                    <p class="font-semibold text-green-800 text-sm">{{ invoiceFile.name }}</p>
                    <p class="text-xs text-green-600">{{ formatFileSize(invoiceFile.size) }}</p>
                  </div>
                </div>
                <button @click="removeFile('invoice')" class="text-green-600 hover:text-red-600 transition-colors">
                  <UIcon name="i-heroicons-x-mark" class="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>

          <!-- Jira File Upload -->
          <div class="bg-gradient-to-br from-green-50/50 to-emerald-50/30 rounded-2xl p-6 border-2 border-dashed border-green-300 hover:border-green-400 transition-colors">
            <div 
              @click="triggerFileInput('jira')"
              @drop.prevent="handleFileDrop($event, 'jira')"
              @dragover.prevent
              @dragenter.prevent
              class="text-center cursor-pointer"
            >
              <div class="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl flex items-center justify-center mx-auto mb-3">
                <UIcon name="i-heroicons-bug-ant" class="w-6 h-6 text-white" />
              </div>
              <h3 class="text-lg font-semibold text-gray-900 mb-2">Jira File</h3>
              <p class="text-gray-600 mb-3">Drop your Jira Excel file here</p>
              <div class="flex items-center justify-center space-x-2 text-sm text-gray-500">
                <UIcon name="i-heroicons-table-cells" class="w-4 h-4" />
                <span>.xlsx, .xls</span>
              </div>
            </div>
            
            <!-- Selected Jira File -->
            <div v-if="jiraFile" class="mt-4 bg-green-100 rounded-lg p-3 border border-green-200">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <UIcon name="i-heroicons-document-check" class="w-5 h-5 text-green-600" />
                  <div>
                    <p class="font-semibold text-green-800 text-sm">{{ jiraFile.name }}</p>
                    <p class="text-xs text-green-600">{{ formatFileSize(jiraFile.size) }}</p>
                  </div>
                </div>
                <button @click="removeFile('jira')" class="text-green-600 hover:text-red-600 transition-colors">
                  <UIcon name="i-heroicons-x-mark" class="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Sheet Name Input -->
        <div class="bg-gradient-to-br from-green-50/50 to-emerald-50/30 rounded-2xl p-6 border border-green-200 mb-6">
          <div class="flex items-center space-x-3 mb-4">
            <div class="w-10 h-10 bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl flex items-center justify-center">
              <UIcon name="i-heroicons-adjustments-horizontal" class="w-5 h-5 text-white" />
            </div>
            <h3 class="text-lg font-semibold text-gray-900">Sheet Configuration</h3>
          </div>
          
          <label class="block text-sm font-medium text-gray-700 mb-2">Sheet Name</label>
          <input
            v-model="sheetName"
            type="text"
            class="w-full px-4 py-3 text-gray-900 bg-white border border-green-200 rounded-xl focus:border-green-400 focus:ring-2 focus:ring-green-100 focus:outline-none transition-all"
            placeholder="Default: Deckblatt"
          />
          <p class="text-sm text-gray-600 mt-2">Specify which sheet in the Excel files should be processed for validation.</p>
        </div>

        <!-- Process Button -->
        <div class="flex flex-col items-center space-y-4">
          <button
            @click="processValidation"
            :disabled="!invoiceFile || !jiraFile || !sheetName || loading"
            :class="[
              'flex items-center space-x-3 px-8 py-4 rounded-xl font-semibold shadow-lg transition-all duration-300',
              invoiceFile && jiraFile && sheetName && !loading
                ? 'bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white hover:shadow-xl transform hover:scale-105 cursor-pointer'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            ]"
          >
            <UIcon :name="loading ? 'i-heroicons-arrow-path' : 'i-heroicons-calculator'" class="w-5 h-5" :class="{ 'animate-spin': loading }" />
            <span v-if="loading">Processing Validation...</span>
            <span v-else-if="!invoiceFile || !jiraFile">Upload both files first</span>
            <span v-else-if="!sheetName">Enter sheet name</span>
            <span v-else>Start Validation</span>
          </button>
        </div>

        <!-- Hidden File Inputs -->
        <input ref="invoiceFileInput" type="file" accept=".xlsx,.xls" @change="handleFileSelect($event, 'invoice')" class="hidden" />
        <input ref="jiraFileInput" type="file" accept=".xlsx,.xls" @change="handleFileSelect($event, 'jira')" class="hidden" />
      </div>

      <!-- Loading Animation -->
      <div v-if="loading" class="bg-white/90 backdrop-blur-sm rounded-3xl shadow-xl p-8 mb-8 border border-green-100">
        <div class="text-center py-12">
          <div class="flex justify-center mb-6">
            <div class="relative">
              <div class="animate-spin rounded-full h-20 w-20 border-4 border-green-200 border-t-green-600"></div>
              <div class="absolute inset-0 flex items-center justify-center">
                <UIcon name="i-heroicons-calculator" class="text-2xl text-green-600" />
              </div>
            </div>
          </div>
          
          <div class="flex items-center justify-center space-x-2 mb-2">
            <UIcon name="i-heroicons-sparkles" class="text-xl text-green-600" />
            <h3 class="text-2xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">Validating Files</h3>
          </div>
          <p class="text-gray-600 font-light mb-8">Comparing invoice and Jira data...</p>
          
          <!-- Progress Animation -->
          <div class="max-w-md mx-auto">
            <div class="bg-green-100 rounded-full h-3 shadow-inner">
              <div 
                class="bg-gradient-to-r from-green-500 to-emerald-500 h-3 rounded-full transition-all duration-500 shadow-lg" 
                :style="{ width: progress + '%' }"
              ></div>
            </div>
            <div class="flex items-center justify-center space-x-2 mt-4">
              <UIcon name="i-heroicons-cpu-chip" class="text-sm text-green-500" />
              <p class="text-sm text-gray-600 font-medium">{{ progressText }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Results Section -->
      <div v-if="downloadUrl" class="bg-white/90 backdrop-blur-sm rounded-3xl shadow-xl p-8 mb-8 border border-green-100">
        <div class="flex items-center justify-between mb-8">
          <div class="flex items-center space-x-3">
            <div class="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center">
              <UIcon name="i-heroicons-check-circle" class="w-6 h-6 text-white" />
            </div>
            <div>
              <h3 class="text-2xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">Validation Complete</h3>
              <p class="text-sm text-gray-600 mt-1">Your comparison results are ready for download</p>
            </div>
          </div>
          <div class="flex items-center space-x-3">
            <button
              @click="downloadResult"
              class="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white font-medium rounded-lg shadow-lg transition-all cursor-pointer"
            >
              <UIcon name="i-heroicons-arrow-down-tray" class="w-5 h-5" />
              <span>Download Excel Result</span>
            </button>
          </div>
        </div>

        <!-- Summary Info -->
        <div class="bg-gradient-to-br from-green-50/50 to-emerald-50/30 rounded-2xl p-6 border border-green-200">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
            <div>
              <div class="text-2xl font-bold text-green-700">{{ invoiceFile?.name }}</div>
              <div class="text-sm text-gray-600">Invoice File</div>
            </div>
            <div class="flex items-center justify-center">
              <UIcon name="i-heroicons-arrow-right" class="w-8 h-8 text-green-500" />
            </div>
            <div>
              <div class="text-2xl font-bold text-green-700">{{ jiraFile?.name }}</div>
              <div class="text-sm text-gray-600">Jira File</div>
            </div>
          </div>
          <div class="text-center mt-4 pt-4 border-t border-green-200">
            <p class="text-sm text-gray-600">Sheet: <span class="font-semibold text-green-700">{{ sheetName }}</span></p>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-if="error" class="bg-gradient-to-br from-red-50/90 to-rose-50/80 backdrop-blur-sm border border-red-200 rounded-2xl shadow-xl p-6 mb-8">
        <div class="flex items-start justify-between">
          <div class="flex items-start space-x-3">
            <UIcon name="i-heroicons-exclamation-triangle" class="text-2xl text-red-600 mt-1" />
            <div>
              <h3 class="text-lg font-bold text-red-800 mb-2">Validation Failed</h3>
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

      <!-- Tips Section -->
      <div class="mt-8 border border-green-200 rounded-2xl shadow-sm p-8" style="background-color: rgba(34, 197, 94, 0.25);">
        <div class="flex items-center space-x-2 mb-4">
          <UIcon name="i-heroicons-light-bulb" class="text-2xl text-green-800" />
          <h3 class="text-xl font-bold text-green-900">Tips for Better Results</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-3">
            <h4 class="font-semibold text-green-800">File Requirements</h4>
            <ul class="text-sm text-green-700 space-y-1">
              <li>• Use Excel files (.xlsx or .xls format)</li>
              <li>• Ensure MLG Invoice file has the correct sheet name reference</li>
              <li>• Files should contain structured data with headers</li>
            </ul>
          </div>
          <div class="space-y-3">
            <h4 class="font-semibold text-green-800">Sheet Configuration</h4>
            <ul class="text-sm text-green-700 space-y-1">
              <li>• Enter the exact sheet name (case-sensitive)</li>
              <li>• Sheet must exist in the MLG Invoice file</li>
              <li>• Use default sheet name if unsure</li>
            </ul>
          </div>
        </div>
      </div>
    </UContainer>
    
    <GlobalFooter />
  </div>
</template>

<script setup>
import { useAuthStore } from '~/stores/auth'
import { useTokenStore } from '~/stores/tokens'
import { useAdobeTracking } from '~/composables/useAdobeTracking'

// Stores
const authStore = useAuthStore()
const tokenStore = useTokenStore()

// Adobe Tracking
const { trackButtonClick, trackTokenUsage } = useAdobeTracking()

// Refs
const invoiceFileInput = ref(null)
const jiraFileInput = ref(null)
const invoiceFile = ref(null)
const jiraFile = ref(null)
const sheetName = ref('Deckblatt')
const loading = ref(false)
const error = ref('')
const downloadUrl = ref('')
const progress = ref(0)
const progressText = ref('')
const isObjectUrl = ref(false) // Track if downloadUrl is an object URL

// Token Logic - Invoice Validator SCO is free but we track usage
const requiredTokens = 0

// Auth Check
onMounted(async () => {
  if (!authStore.isInitialized) await authStore.init()
  if (!authStore.isAuthenticated) await navigateTo('/login')
  if (!tokenStore.isInitialized) await tokenStore.init()
})

// File handling
const triggerFileInput = (type) => {
  if (!loading.value) {
    if (type === 'invoice') {
      invoiceFileInput.value?.click()
    } else if (type === 'jira') {
      jiraFileInput.value?.click()
    }
  }
}

const handleFileSelect = (event, type) => {
  const file = event.target.files[0]
  if (file) {
    validateAndSetFile(file, type)
  }
}

const handleFileDrop = (event, type) => {
  const file = event.dataTransfer.files[0]
  if (file) {
    validateAndSetFile(file, type)
  }
}

const validateAndSetFile = (file, type) => {
  // Check file type
  const allowedTypes = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']
  const allowedExtensions = ['.xlsx', '.xls']
  
  const hasValidType = allowedTypes.includes(file.type)
  const hasValidExtension = allowedExtensions.some(ext => file.name.toLowerCase().endsWith(ext))
  
  if (!hasValidType && !hasValidExtension) {
    error.value = 'Please select an Excel file (.xlsx or .xls).'
    return
  }

  // Check file size (50MB limit)
  if (file.size > 50 * 1024 * 1024) {
    error.value = 'File size must be less than 50MB.'
    return
  }

  if (type === 'invoice') {
    invoiceFile.value = file
  } else if (type === 'jira') {
    jiraFile.value = file
  }
  
  error.value = ''
}

const removeFile = (type) => {
  if (type === 'invoice') {
    invoiceFile.value = null
    if (invoiceFileInput.value) {
      invoiceFileInput.value.value = ''
    }
  } else if (type === 'jira') {
    jiraFile.value = null
    if (jiraFileInput.value) {
      jiraFileInput.value.value = ''
    }
  }
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// Reset form function
const resetForm = () => {
  // Clean up file inputs
  invoiceFile.value = null
  jiraFile.value = null
  sheetName.value = 'Deckblatt'
  error.value = ''
  
  // Clean up download URL if it's an object URL
  if (isObjectUrl.value && downloadUrl.value) {
    URL.revokeObjectURL(downloadUrl.value)
  }
  downloadUrl.value = ''
  isObjectUrl.value = false
  
  // Reset file input elements
  if (invoiceFileInput.value) {
    invoiceFileInput.value.value = ''
  }
  if (jiraFileInput.value) {
    jiraFileInput.value.value = ''
  }
}

// Main processing function
const processValidation = async () => {
  if (!invoiceFile.value || !jiraFile.value || !sheetName.value || loading.value) return

  // Track processing start
  trackButtonClick('Process Invoice Validator SCO', {
    invoiceFileName: invoiceFile.value.name.split('.').pop(),
    jiraFileName: jiraFile.value.name.split('.').pop(),
    invoiceFileSizeMB: Math.round((invoiceFile.value.size / 1024 / 1024) * 100) / 100,
    jiraFileSizeMB: Math.round((jiraFile.value.size / 1024 / 1024) * 100) / 100,
    sheetName: sheetName.value
  })

  loading.value = true
  error.value = ''
  downloadUrl.value = ''
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
    formData.append('invoice_file', invoiceFile.value)
    formData.append('jira_file', jiraFile.value)
    formData.append('sheet_name', sheetName.value)

    // Make authenticated API call
    const { authenticatedEndpointRequest, apiEndpoints } = await import('~/config/api.config')
    

    
    const response = await authenticatedEndpointRequest(apiEndpoints.invoiceValidatorSco, {
      method: 'POST',
      body: formData
    })


    // Complete progress
    clearInterval(progressInterval)
    progress.value = 100
    progressText.value = 'Complete!'

    // Handle response - check if it's a blob or has download_url
    if (response instanceof Blob) {
      // Clean up previous object URL if it exists
      if (isObjectUrl.value && downloadUrl.value) {
        URL.revokeObjectURL(downloadUrl.value)
      }
      
      // Create object URL from blob for download
      downloadUrl.value = URL.createObjectURL(response)
      isObjectUrl.value = true
    } else if (response && response.download_url) {
      // Clean up previous object URL if it exists
      if (isObjectUrl.value && downloadUrl.value) {
        URL.revokeObjectURL(downloadUrl.value)
      }
      
      downloadUrl.value = response.download_url
      isObjectUrl.value = false
    } else {
      throw new Error('Invalid response format - expected Blob or download URL')
    }
    
    // Track usage (free service - 0 tokens)
    trackTokenUsage(0, 'invoice_validator_sco', {
      invoiceFileName: invoiceFile.value.name.split('.').pop(),
      jiraFileName: jiraFile.value.name.split('.').pop(),
      invoiceFileSizeMB: Math.round((invoiceFile.value.size / 1024 / 1024) * 100) / 100,
      jiraFileSizeMB: Math.round((jiraFile.value.size / 1024 / 1024) * 100) / 100,
      sheetName: sheetName.value,
      success: true
    })
    
    // Show success notification
    const toast = useToast()
    toast.add({
      title: 'Validation Complete',
      description: 'Invoice validation completed successfully.',
      color: 'green'
    })

  } catch (err) {
    console.error('Error processing invoice validation:', err)
    
    // Track API error with Adobe Analytics
    const { trackError } = useAdobeTracking()
    trackError('api_invoice_validator_sco_failed', 'Invoice Validator SCO API request failed', {
      errorMessage: err.message || err.toString(),
      errorCode: err.status || err.statusCode || 'unknown',
      errorType: err.name || 'APIError',
      endpoint: 'invoiceValidatorSco',
      requestData: {
        invoiceFileName: invoiceFile.value?.name || 'unknown',
        jiraFileName: jiraFile.value?.name || 'unknown',
        invoiceFileType: invoiceFile.value?.type || 'unknown',
        jiraFileType: jiraFile.value?.type || 'unknown',
        invoiceFileSizeMB: invoiceFile.value ? Math.round((invoiceFile.value.size / 1024 / 1024) * 100) / 100 : 0,
        jiraFileSizeMB: jiraFile.value ? Math.round((jiraFile.value.size / 1024 / 1024) * 100) / 100 : 0,
        sheetName: sheetName.value
      },
      userAgent: window.navigator?.userAgent || 'unknown',
      timestamp: new Date().toISOString()
    })
    
    error.value = err.message || 'Validation failed. Please try again.'
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
    'Uploading files...',
    'Reading Excel data...',
    'Processing invoice data...',
    'Analyzing Jira data...',
    'Comparing datasets...',
    'Computing differences...',
    'Generating Excel report...'
  ]
  const index = Math.floor((progress.value / 100) * (texts.length - 1))
  progressText.value = texts[index] || texts[0]
}

const downloadResult = () => {
  if (downloadUrl.value) {
    // Track download action
    trackButtonClick('Download Invoice Validator Result', {
      invoiceFileName: invoiceFile.value?.name || 'unknown',
      jiraFileName: jiraFile.value?.name || 'unknown',
      sheetName: sheetName.value,
      downloadFormat: 'excel'
    })

    // Create download link
    const link = document.createElement('a')
    link.href = downloadUrl.value
    link.download = `invoice-validation-result-${Date.now()}.xlsx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    // Clean up object URL after download if it's a blob URL
    if (isObjectUrl.value) {
      // Clean up with a small delay to ensure download starts
      setTimeout(() => {
        URL.revokeObjectURL(downloadUrl.value)
        downloadUrl.value = ''
        isObjectUrl.value = false
      }, 1000)
    }
    
    // Show download notification
    const toast = useToast()
    toast.add({
      title: 'Download Started',
      description: 'Your validation result Excel file is being downloaded.',
      color: 'green'
    })
    
    // Reset form after 2 seconds
    setTimeout(() => {
      resetForm()
      
      // Show reset notification
      const resetToast = useToast()
      resetToast.add({
        title: 'Form Reset',
        description: 'Ready for new validation. Form has been cleared.',
        color: 'blue'
      })
    }, 2000)
  }
}

// Cleanup for object URLs
onUnmounted(() => {
  if (isObjectUrl.value && downloadUrl.value) {
    URL.revokeObjectURL(downloadUrl.value)
  }
})

// SEO
useHead({
  title: 'Invoice Validator - SCO - DAISY',
  meta: [
    {
      name: 'description',
      content: 'Supply-Chain Operations tool: Upload invoice and Jira Excel files to validate and compare them. Returns a downloadable Excel file with computed differences.'
    }
  ]
})
</script>

<style scoped>
/* Add any specific styles if needed */
</style> 