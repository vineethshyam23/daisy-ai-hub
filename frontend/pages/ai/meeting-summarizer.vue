<template>
  <!-- Loading State while auth is being determined -->
  <div v-if="!authStore.isInitialized" class="min-h-screen bg-gradient-to-br from-teal-50 via-teal-25 to-emerald-50 flex items-center justify-center">
    <div class="text-center">
      <div class="w-16 h-16 bg-gradient-to-br from-teal-500 to-emerald-500 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl animate-pulse">
        <UIcon name="i-heroicons-cpu-chip" class="w-8 h-8 text-white" />
      </div>
      <h2 class="text-2xl font-bold bg-gradient-to-r from-teal-500 to-emerald-500 bg-clip-text text-transparent mb-2">
        DAISY
      </h2>
      <p class="text-gray-600 font-light">Loading Meeting Summarizer...</p>
      <div class="mt-4 flex justify-center">
        <div class="w-8 h-8 border-4 border-teal-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    </div>
  </div>

  <!-- Main Content - Only show if authenticated -->
  <div v-else-if="authStore.isAuthenticated" class="min-h-screen bg-gradient-to-br from-teal-50 via-teal-25 to-emerald-50">
    <!-- Unified Header -->
    <AIHeader />

    <!-- Hero Banner -->
    <div class="relative bg-gradient-to-r from-teal-800 via-teal-600 to-teal-500 border-b border-teal-700 overflow-hidden">
          <!-- Meeting Pattern -->
          <div class="absolute right-0 top-0 w-1/2 h-full opacity-8">
            <svg class="w-full h-full" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <pattern id="meeting-pattern" x="0" y="0" width="28" height="28" patternUnits="userSpaceOnUse">
                  <circle cx="8" cy="8" r="2" fill="none" stroke="white" stroke-width="0.5"/>
                  <circle cx="20" cy="8" r="2" fill="none" stroke="white" stroke-width="0.5"/>
                  <circle cx="14" cy="16" r="2" fill="none" stroke="white" stroke-width="0.5"/>
                  <path d="M8,10 L14,14 M20,10 L14,14" stroke="white" stroke-width="0.4"/>
                  <rect x="6" y="20" width="16" height="1" fill="white" opacity="0.4"/>
                </pattern>
              </defs>
              <rect width="100" height="100" fill="url(#meeting-pattern)"/>
            </svg>
          </div>
          
          <!-- Collaboration Network Background -->
          <div class="absolute right-0 top-0 w-2/3 h-full opacity-4">
            <div class="w-full h-full" style="background-image: radial-gradient(circle at 83% 32%, white 2px, transparent 2px), radial-gradient(circle at 77% 68%, white 1.5px, transparent 1.5px), radial-gradient(circle at 91% 48%, white 1px, transparent 1px); background-size: 44px 44px, 32px 32px, 60px 60px;"></div>
          </div>
          
      <UContainer class="relative z-10 py-16">
        <div class="max-w-4xl">
          <div class="flex items-center mb-6">
            <div class="w-16 h-16 bg-teal-500 rounded-2xl flex items-center justify-center mr-6 border border-teal-700">
              <UIcon name="i-heroicons-document-text" class="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 class="text-4xl font-bold text-white mb-2">Meeting Summarizer</h1>
              <p class="text-xl text-teal-100">Transform meeting transcripts into structured summaries with key decisions and action items</p>
            </div>
          </div>
        </div>
      </UContainer>
    </div>
    
    <UContainer class="py-8">
      
      <!-- Upload Form -->
      <div class="bg-white/90 backdrop-blur-sm rounded-3xl shadow-xl p-8 mb-8 border border-teal-100">
        <div class="flex items-center space-x-3 mb-6">
          <div class="w-12 h-12 bg-gradient-to-br from-teal-500 to-emerald-500 rounded-2xl flex items-center justify-center">
            <UIcon name="i-heroicons-document-arrow-up" class="w-6 h-6 text-white" />
          </div>
          <h2 class="text-2xl font-bold text-gray-900">Upload Meeting Transcript</h2>
        </div>

        <!-- File Upload Area -->
        <div class="bg-gradient-to-br from-teal-50/50 to-emerald-50/30 rounded-2xl p-8 border-2 border-dashed border-teal-300 hover:border-teal-400 transition-colors mb-6">
          <div 
            @click="triggerFileInput"
            @drop.prevent="handleFileDrop"
            @dragover.prevent
            @dragenter.prevent
            class="text-center cursor-pointer"
          >
            <div class="w-16 h-16 bg-gradient-to-br from-teal-500 to-emerald-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <UIcon name="i-heroicons-cloud-arrow-up" class="w-8 h-8 text-white" />
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">
              Drop your meeting transcript here
            </h3>
            <p class="text-gray-600 mb-4">
              Or click to browse and select a file
            </p>
            <div class="flex items-center justify-center space-x-4 text-sm text-gray-500">
              <div class="flex items-center space-x-1">
                <UIcon name="i-heroicons-document-text" class="w-4 h-4" />
                <span>.txt</span>
              </div>
              <div class="flex items-center space-x-1">
                <UIcon name="i-heroicons-document" class="w-4 h-4" />
                <span>.docx</span>
              </div>
              <span>•</span>
              <span>Max 10MB</span>
            </div>
          </div>
        </div>

        <!-- Selected File Display -->
        <div v-if="selectedFile" class="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-4 border border-green-200 mb-6">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-gradient-to-br from-green-500 to-emerald-500 rounded-lg flex items-center justify-center">
                <UIcon name="i-heroicons-document-check" class="w-5 h-5 text-white" />
              </div>
              <div>
                <p class="font-semibold text-green-800">{{ selectedFile.name }}</p>
                <p class="text-sm text-green-600">{{ formatFileSize(selectedFile.size) }} • Ready to process</p>
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

        <!-- Template Selection -->
        <div v-if="selectedFile" class="bg-gradient-to-br from-teal-50/50 to-emerald-50/30 rounded-2xl p-6 border border-teal-200 mb-6">
          <div class="flex items-center space-x-3 mb-4">
            <div class="w-10 h-10 bg-gradient-to-br from-teal-500 to-emerald-500 rounded-xl flex items-center justify-center">
              <UIcon name="i-heroicons-adjustments-horizontal" class="w-5 h-5 text-white" />
            </div>
            <h3 class="text-lg font-semibold text-gray-900">Summary Template</h3>
          </div>
          
          <p class="text-sm text-gray-600 mb-4">Choose the best template for your meeting type:</p>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div
              v-for="template in templates"
              :key="template.value"
              @click="selectedTemplate = template.value"
              :class="[
                'relative cursor-pointer rounded-xl border-2 p-4 transition-all duration-200',
                selectedTemplate === template.value
                  ? 'border-teal-500 bg-teal-50 shadow-md'
                  : 'border-gray-200 hover:border-teal-300 hover:bg-teal-25'
              ]"
            >
              <div class="flex items-start space-x-3">
                <div :class="[
                  'flex-shrink-0 w-4 h-4 rounded-full border-2 mt-1 transition-colors',
                  selectedTemplate === template.value
                    ? 'border-teal-500 bg-teal-500'
                    : 'border-gray-300'
                ]">
                  <div v-if="selectedTemplate === template.value" class="w-full h-full rounded-full bg-white scale-50"></div>
                </div>
                <div class="flex-1 min-w-0">
                  <h4 class="text-sm font-semibold text-gray-900 capitalize mb-1">
                    {{ template.label }}
                  </h4>
                  <p class="text-xs text-gray-600 leading-relaxed">
                    {{ template.description }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Process Button -->
        <div class="flex flex-col items-center space-y-4">
          <button
            @click="processMeeting"
            :disabled="!selectedFile || loading || (tokenStore.isTokenDataReady && !hasEnoughTokens)"
            :class="[
              'flex items-center space-x-3 px-8 py-4 rounded-xl font-semibold shadow-lg transition-all duration-300',
              selectedFile && !loading && (!tokenStore.isTokenDataReady || hasEnoughTokens)
                ? 'bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 text-white hover:shadow-xl transform hover:scale-105 cursor-pointer'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            ]"
          >
            <UIcon :name="loading ? 'i-heroicons-arrow-path' : 'i-heroicons-sparkles'" class="w-5 h-5" :class="{ 'animate-spin': loading }" />
            <span v-if="loading">Processing Meeting...</span>
            <span v-else-if="!selectedFile">Select a file first</span>
            <span v-else-if="!tokenStore.isTokenDataReady">Loading tokens...</span>
            <span v-else-if="!hasEnoughTokens">Insufficient Tokens ({{ requiredTokens }} required)</span>
            <span v-else>Generate Summary ({{ requiredTokens }} token{{ requiredTokens > 1 ? 's' : '' }})</span>
          </button>



          <!-- Insufficient Tokens Warning -->
          <div v-if="selectedFile && tokenStore.isTokenDataReady && !hasEnoughTokens" class="bg-gradient-to-r from-red-50 to-rose-50 border border-red-200 rounded-xl p-4 max-w-md">
            <div class="flex items-start space-x-3">
              <UIcon name="i-heroicons-exclamation-triangle" class="text-red-500 text-lg mt-0.5" />
              <div>
                <p class="text-sm font-semibold text-red-800 mb-1">Not enough tokens</p>
                <p class="text-sm text-red-700 mb-2">
                  You need {{ requiredTokens }} token{{ requiredTokens > 1 ? 's' : '' }} but only have {{ tokenStore.tokens }} available.
                </p>
                <p class="text-xs text-red-600">
                  Your tokens will reset in {{ tokenStore.getHoursUntilReset() }} hours.
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Hidden File Input -->
        <input
          ref="fileInput"
          type="file"
          accept=".txt,.docx"
          @change="handleFileSelect"
          class="hidden"
        />
      </div>

      <!-- Disclaimer -->
      <DisclaimerBox 
        disclaimer-text="This meeting summary is generated by AI and may not capture all nuances or context. Please review and adjust if needed."
        class="mb-6"
      />

      <!-- Loading Animation -->
      <div v-if="loading" class="bg-white/90 backdrop-blur-sm rounded-3xl shadow-xl p-8 mb-8 border border-teal-100">
        <div class="text-center py-12">
          <div class="flex justify-center mb-6">
            <div class="relative">
              <div class="animate-spin rounded-full h-20 w-20 border-4 border-teal-200 border-t-teal-600"></div>
              <div class="absolute inset-0 flex items-center justify-center">
                <UIcon name="i-heroicons-document-text" class="text-2xl text-teal-600" />
              </div>
            </div>
          </div>
          
          <div class="flex items-center justify-center space-x-2 mb-2">
            <UIcon name="i-heroicons-sparkles" class="text-xl text-teal-600" />
            <h3 class="text-2xl font-bold bg-gradient-to-r from-teal-600 to-emerald-600 bg-clip-text text-transparent">Processing Meeting Transcript</h3>
          </div>
          <p class="text-gray-600 font-light mb-8">Analyzing content and extracting key information...</p>
          
          <!-- Progress Animation -->
          <div class="max-w-md mx-auto">
            <div class="bg-teal-100 rounded-full h-3 shadow-inner">
              <div 
                class="bg-gradient-to-r from-teal-500 to-emerald-500 h-3 rounded-full transition-all duration-500 shadow-lg" 
                :style="{ width: progress + '%' }"
              ></div>
            </div>
            <div class="flex items-center justify-center space-x-2 mt-4">
              <UIcon name="i-heroicons-cpu-chip" class="text-sm text-teal-500" />
              <p class="text-sm text-gray-600 font-medium">{{ progressText }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Meeting Summarizer Results -->
      <div v-if="meetingSummary" class="bg-white/90 backdrop-blur-sm rounded-3xl shadow-xl p-8 mb-8 border border-teal-100">
        <div class="flex items-center justify-between mb-8">
          <div class="flex items-center space-x-3">
            <div class="w-12 h-12 bg-gradient-to-br from-teal-500 to-emerald-500 rounded-2xl flex items-center justify-center">
              <UIcon name="i-heroicons-check-circle" class="w-6 h-6 text-white" />
            </div>
            <h3 class="text-2xl font-bold bg-gradient-to-r from-teal-600 to-emerald-600 bg-clip-text text-transparent">Meeting Summary Generated</h3>
          </div>
          <div class="flex items-center space-x-3">
            <button
              @click="downloadPDF"
              :disabled="generatingPDF"
              class="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 disabled:from-gray-400 disabled:to-gray-500 text-white font-medium rounded-lg shadow-lg transition-all cursor-pointer disabled:cursor-not-allowed"
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
                <span>Summary copied to clipboard!</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Summary Content -->
        <div class="bg-gradient-to-br from-teal-50/50 to-emerald-50/30 rounded-2xl p-6 border border-teal-200">
          <div class="prose max-w-none" v-html="meetingSummary"></div>
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

      <!-- Tips Section -->
      <div class="mt-8 border border-teal-200 rounded-2xl shadow-sm p-8" style="background-color: rgba(20, 184, 166, 0.25);">
        <div class="flex items-center space-x-2 mb-4">
          <UIcon name="i-heroicons-light-bulb" class="text-2xl text-teal-800" />
          <h3 class="text-xl font-bold text-teal-900">Tips for Better Results</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-3">
            <h4 class="font-semibold text-teal-800">Transcript Quality</h4>
            <ul class="text-sm text-teal-700 space-y-1">
              <li>• Use clear, well-structured meeting transcripts</li>
              <li>• Include speaker names and timestamps if available</li>
              <li>• Ensure complete conversations without missing parts</li>
            </ul>
          </div>
          <div class="space-y-3">
            <h4 class="font-semibold text-teal-800">File Format</h4>
            <ul class="text-sm text-teal-700 space-y-1">
              <li>• Upload .txt or .docx files up to 10MB</li>
              <li>• Organize content with clear sections if possible</li>
              <li>• Include meeting context and participant information</li>
            </ul>
          </div>
        </div>
      </div>
    </UContainer>
    
    <!-- Global Footer -->
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

// Initialize stores after navigation (auth is handled by middleware)
onMounted(async () => {
  // Initialize token store after successful authentication
  if (!tokenStore.isInitialized) {
    try {
      await tokenStore.init()
    } catch (error) {
      console.error('Meeting Summarizer: Error initializing token store:', error)
    }
  }
})

// Refs
const fileInput = ref(null)
const selectedFile = ref(null)
const selectedTemplate = ref('discussion') // Default template
const loading = ref(false)
const error = ref('')
const meetingSummary = ref('')
const progress = ref(0)
const progressText = ref('')
const copyConfirmation = ref(false)
const generatingPDF = ref(false)

// Template options
const templates = ref([
  {
    value: 'discussion',
    label: 'Discussion',
    description: 'Perfect for regular project meetings, planning sessions, and decision-making discussions. Organizes content into key decisions, action items with owners and deadlines, and open questions for follow-up.'
  },
  {
    value: 'daily-weekly',
    label: 'Daily/Weekly',
    description: 'Ideal for daily standups, weekly team meetings, and recurring status updates. Creates a structured table showing what each participant accomplished, current work, blockers, and next steps.'
  },
  {
    value: 'presentation',
    label: 'Presentation',
    description: 'Best for presentations, demos, training sessions, and knowledge sharing meetings. Captures key topics, insights, recommendations, supporting data, and Q&A highlights in a comprehensive format.'
  }
])

// Token calculation based on file size
const calculateTokenCost = (fileSize) => {
  const fileSizeMB = fileSize / (1024 * 1024)
  if (fileSizeMB < 5) {
    return 1 // Files under 5MB cost 1 token
  } else if (fileSizeMB <= 10) {
    return 2 // Files between 5-10MB cost 2 tokens
  }
  return 2 // Fallback (shouldn't happen as we limit to 10MB)
}

// Computed properties for token management
const requiredTokens = computed(() => {
  return selectedFile.value ? calculateTokenCost(selectedFile.value.size) : 0
})

const hasEnoughTokens = computed(() => {
  // Only check tokens if token data is ready from Firebase
  if (!tokenStore.isTokenDataReady) {
    return true // Assume we have enough tokens while loading
  }
  return tokenStore.tokens >= requiredTokens.value
})

// Methods
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
  const allowedTypes = ['text/plain', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
  const allowedExtensions = ['.txt', '.docx']
  
  const hasValidType = allowedTypes.includes(file.type)
  const hasValidExtension = allowedExtensions.some(ext => file.name.toLowerCase().endsWith(ext))
  
  if (!hasValidType && !hasValidExtension) {
    error.value = 'Please select a .txt or .docx file.'
    return
  }

  // Check file size (10MB limit)
  if (file.size > 10 * 1024 * 1024) {
    error.value = 'File size must be less than 10MB.'
    return
  }

  selectedFile.value = file
  error.value = ''
}

const removeFile = () => {
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

const processMeeting = async () => {
  if (!selectedFile.value || loading.value) return

  // Check if user has sufficient tokens
  if (!hasEnoughTokens.value) {
    const toast = useToast()
    toast.add({
      title: 'Insufficient Tokens',
      description: `You need ${requiredTokens.value} token(s) to process this file. Your tokens will reset in ${tokenStore.getHoursUntilReset()} hours.`,
      color: 'red',
      timeout: 8000
    })
    return
  }

  // Track processing start with file metadata
  trackButtonClick('Process Meeting Transcript', {
    fileType: selectedFile.value.type,
    fileName: selectedFile.value.name.split('.').pop(), // file extension
    fileSizeMB: Math.round((selectedFile.value.size / 1024 / 1024) * 100) / 100,
    tokenCost: requiredTokens.value,
    tokensAvailable: tokenStore.tokens,
    template: selectedTemplate.value
  })

  loading.value = true
  error.value = ''
  meetingSummary.value = ''
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
    formData.append('transcript_file', selectedFile.value)
    formData.append('template', selectedTemplate.value)

    // Make authenticated API call
    const { authenticatedEndpointRequest, apiEndpoints } = await import('~/config/api.config')
    const response = await authenticatedEndpointRequest(apiEndpoints.meetingMinutes, {
      method: 'POST',
      body: formData
    }).catch((err) => {
      // Fallback to dummy response for testing
      return generateDummyResponse()
    })

    // Complete progress
    clearInterval(progressInterval)
    progress.value = 100
    progressText.value = 'Complete!'

    // Set the meeting summary - API now returns JSON with meeting_summary field
    if (response) {
      // Extract the HTML content from the response object
      let htmlContent = ''
      if (typeof response === 'string') {
        htmlContent = response
      } else if (response.meeting_summary) {
        // Remove markdown code block wrapper if present
        htmlContent = response.meeting_summary
        if (htmlContent.startsWith('```html\n')) {
          htmlContent = htmlContent.replace(/^```html\n/, '').replace(/\n```$/, '')
        }
      } else {
        throw new Error('Invalid response format - missing meeting_summary field')
      }
      
      meetingSummary.value = htmlContent
      
      // Consume tokens after successful processing
      const tokensUsed = requiredTokens.value
      const tokenConsumed = await tokenStore.useTokens(tokensUsed)
      
      if (tokenConsumed) {
        // Track token usage
        const { trackTokenUsage } = useAdobeTracking()
        trackTokenUsage(tokensUsed, 'meeting_summarizer', {
          fileSize: selectedFile.value?.size || 0,
          fileName: selectedFile.value?.name || 'unknown',
          fileType: selectedFile.value?.type || 'unknown',
          template: selectedTemplate.value
        })
      } else {
        console.warn('Failed to consume tokens, but processing was successful')
      }
      
      // Show success notification with token info
      const toast = useToast()
      toast.add({
        title: 'Meeting Summary Generated',
        description: `Your meeting summary has been generated successfully. ${tokenStore.tokens} tokens remaining today.`,
        color: 'green'
      })
    } else {
      throw new Error('Invalid response format - empty response')
    }

  } catch (err) {
    console.error('Error processing meeting transcript:', err)
    
    // Track API error with Adobe Analytics
    const { trackError } = useAdobeTracking()
    trackError('api_meeting_summarizer_failed', 'Meeting Summarizer API request failed', {
      errorMessage: err.message || err.toString(),
      errorCode: err.status || err.statusCode || 'unknown',
      errorType: err.name || 'APIError',
      endpoint: 'meetingSummarizer',
      requestData: {
        fileName: selectedFile.value?.name || 'unknown',
        fileType: selectedFile.value?.type || 'unknown',
        fileSizeMB: selectedFile.value ? Math.round((selectedFile.value.size / 1024 / 1024) * 100) / 100 : 0,
        template: selectedTemplate.value,
        tokensRequired: requiredTokens.value,
        tokensAvailable: tokenStore.tokens
      },
      userAgent: window.navigator?.userAgent || 'unknown',
      timestamp: new Date().toISOString()
    })
    
    error.value = err.message || 'Failed to process meeting transcript. Please try again.'
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
    'Uploading transcript...',
    'Analyzing meeting content...',
    'Extracting key decisions...',
    'Identifying action items...',
    'Generating summary structure...',
    'Finalizing report...'
  ]
  const index = Math.floor((progress.value / 100) * (texts.length - 1))
  progressText.value = texts[index] || texts[0]
}

// Dummy response for testing
const generateDummyResponse = () => {
  return {
    meeting_summary: `<h3>Meeting Context:</h3>
<ul>
<li><strong>Project/Topic:</strong> ${selectedFile.value?.name?.replace(/\.(txt|docx)$/, '') || 'Project Planning'}</li>
<li><strong>Meeting Date:</strong> ${new Date().toLocaleDateString()}</li>
<li><strong>Attendees:</strong> Team Members</li>
</ul>

<h3>1. Executive Summary:</h3>
<p>This is a demo summary generated from your uploaded transcript. The actual API will provide detailed analysis of your meeting content.</p>

<h3>2. Key Decisions Made:</h3>
<ul>
<li>Demo decision 1 extracted from transcript</li>
<li>Demo decision 2 based on meeting discussion</li>
<li>Demo decision 3 regarding next steps</li>
</ul>

<h3>3. Action Items:</h3>
<ul>
<li>Complete task A: <strong>Owner(s):</strong> Team Member 1 - <strong>Deadline:</strong> Next Week</li>
<li>Review proposal B: <strong>Owner(s):</strong> Team Member 2 - <strong>Deadline:</strong> End of Month</li>
<li>Follow up on topic C: <strong>Owner(s):</strong> Team Lead - <strong>Deadline:</strong> ASAP</li>
</ul>

<h3>4. Open Questions / For Next Meeting:</h3>
<ul>
<li>Question about budget allocation</li>
<li>Timeline confirmation needed</li>
<li>Resource availability discussion</li>
</ul>`
  }
}

// Note: formatMeetingSummary function removed - API now returns ready-to-use HTML

const copyToClipboard = async () => {
  if (!meetingSummary.value) return

  try {
    // Track copy action
    trackButtonClick('Copy Meeting Summarizer', {
      fileType: selectedFile.value?.type || 'unknown',
      fileName: selectedFile.value?.name?.split('.').pop() || 'unknown',
      summaryLength: meetingSummary.value.length,
      copyMethod: 'clipboard'
    })

    // Convert HTML to plain text
    const tempDiv = document.createElement('div')
    tempDiv.innerHTML = meetingSummary.value
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
  if (!meetingSummary.value) return

  generatingPDF.value = true
  
  try {
    // Track PDF download action
    trackButtonClick('Download Meeting Summarizer PDF', {
      fileType: selectedFile.value?.type || 'unknown',
      fileName: selectedFile.value?.name?.split('.').pop() || 'unknown',
      summaryLength: meetingSummary.value.length,
      downloadFormat: 'pdf'
    })

    // Dynamic import of html2pdf
    const html2pdf = (await import('html2pdf.js')).default

    // Create a styled container for PDF
    const pdfContainer = document.createElement('div')
    pdfContainer.style.cssText = `
      font-family: system-ui, -apple-system, sans-serif;
      line-height: 1.6;
      color: #374151;
      max-width: 800px;
      margin: 0 auto;
      padding: 40px 20px;
      background: white;
    `

    // Add title
    const title = document.createElement('div')
    title.style.cssText = `
      text-align: center;
      margin-bottom: 40px;
      border-bottom: 3px solid #14b8a6;
      padding-bottom: 20px;
    `
    title.innerHTML = `
      <h1 style="
        font-size: 28px;
        font-weight: 700;
        color: #111827;
        margin: 0 0 10px 0;
        background: linear-gradient(to right, #14b8a6, #10b981);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
      ">Meeting Summary</h1>
      <p style="
        font-size: 14px;
        color: #6b7280;
        margin: 0;
      ">Generated on ${new Date().toLocaleDateString()} • ${selectedFile.value?.name || 'Meeting Transcript'}</p>
    `

    // Add meeting content with enhanced styles
    const content = document.createElement('div')
    content.innerHTML = meetingSummary.value
    
    // Apply inline styles for PDF
    const h2Elements = content.querySelectorAll('h2')
    h2Elements.forEach(h2 => {
      h2.style.cssText = `
        font-size: 24px;
        font-weight: 700;
        color: #111827;
        margin: 30px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #14b8a6;
        background: linear-gradient(to right, #14b8a6, #10b981);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
      `
    })

    const h3Elements = content.querySelectorAll('h3')
    h3Elements.forEach(h3 => {
      h3.style.cssText = `
        font-size: 20px;
        font-weight: 600;
        color: #1f2937;
        margin: 25px 0 12px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid #e5e7eb;
      `
    })

    const pElements = content.querySelectorAll('p')
    pElements.forEach(p => {
      p.style.cssText = `
        margin: 12px 0;
        line-height: 1.7;
        font-size: 14px;
      `
    })

    const ulElements = content.querySelectorAll('ul')
    ulElements.forEach(ul => {
      ul.style.cssText = `
        margin: 15px 0;
        padding-left: 20px;
      `
    })

    const liElements = content.querySelectorAll('li')
    liElements.forEach(li => {
      li.style.cssText = `
        margin: 6px 0;
        line-height: 1.6;
        font-size: 14px;
      `
    })

    // Style tables for PDF
    const tables = content.querySelectorAll('table')
    tables.forEach(table => {
      table.style.cssText = `
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      `
      
      const theadElements = table.querySelectorAll('thead th')
      theadElements.forEach(th => {
        th.style.cssText = `
          background: #14b8a6;
          color: white;
          padding: 12px 8px;
          text-align: left;
          font-weight: 600;
          font-size: 11px;
          text-transform: uppercase;
          letter-spacing: 0.5px;
          border: 1px solid #0d9488;
        `
      })

      const tbodyElements = table.querySelectorAll('tbody td')
      tbodyElements.forEach((td, index) => {
        const isFirstColumn = index % theadElements.length === 0
        td.style.cssText = `
          padding: 10px 8px;
          border: 1px solid #e5e7eb;
          vertical-align: top;
          line-height: 1.4;
          ${isFirstColumn ? 'background-color: #f9fafb; font-weight: 600; color: #111827;' : ''}
        `
      })
    })

    pdfContainer.appendChild(title)
    pdfContainer.appendChild(content)

    // PDF generation options
    const options = {
      margin: [15, 15, 15, 15],
      filename: `meeting-summary-${Date.now()}.pdf`,
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { 
        scale: 2,
        useCORS: true,
        allowTaint: true,
        letterRendering: true
      },
      jsPDF: { 
        unit: 'mm', 
        format: 'a4', 
        orientation: 'portrait'
      },
      pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
    }

    // Generate and download PDF
    await html2pdf().set(options).from(pdfContainer).save()

    // Show success notification
    const toast = useToast()
    toast.add({
      title: 'PDF Generated',
      description: 'Your meeting summary has been downloaded as PDF.',
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

// SEO
useHead({
  title: 'Meeting Summarizer - Transform Transcripts into Structured Summaries | AI Hub',
  meta: [
    {
      name: 'description',
      content: 'Transform meeting transcripts into structured summaries with key decisions, action items, and next steps using AI-powered analysis.'
    }
  ]
})
</script>

<style scoped>
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

/* Enhanced Heading Styles for Meeting Summaries */
:deep(.prose h2),
.prose h2 {
  font-size: 1.5rem !important;
  font-weight: 700 !important;
  color: #111827 !important;
  margin-top: 2rem !important;
  margin-bottom: 1rem !important;
  padding-bottom: 0.75rem !important;
  border-bottom: 2px solid #14b8a6 !important;
  background: linear-gradient(to right, #14b8a6, #10b981) !important;
  background-clip: text !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  text-fill-color: transparent !important;
}

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

/* Add more spacing after paragraphs that follow headings */
:deep(.prose h2 + p),
:deep(.prose h3 + p),
.prose h2 + p,
.prose h3 + p {
  margin-top: 1.25rem !important;
  margin-bottom: 1.5rem !important;
  font-size: 1rem !important;
  line-height: 1.7 !important;
}

/* First paragraph after h2 gets special treatment */
:deep(.prose h2 + p),
.prose h2 + p {
  font-size: 1.05rem !important;
  color: #4b5563 !important;
  font-weight: 400 !important;
}

/* Enhanced Meeting Summarizer Styles - WORKING VERSION */
.meeting-summarizer h3 {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111827;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 0.5rem;
}

.meeting-summarizer h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}

.meeting-summarizer ul {
  list-style-type: disc;
  list-style-position: inside;
  margin-left: 1rem;
  margin-bottom: 1rem;
}

.meeting-summarizer li {
  margin-bottom: 0.25rem;
  line-height: 1.625;
}

/* Table Styling for Meeting Summaries - Global styles to work with v-html */
:deep(.prose table),
.prose table {
  width: 100% !important;
  border-collapse: collapse !important;
  margin: 1.5rem 0 !important;
  background: white !important;
  border-radius: 0.75rem !important;
  overflow: hidden !important;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
  border: 1px solid #e5e7eb !important;
}

:deep(.prose thead),
.prose thead {
  background: linear-gradient(to right, #14b8a6, #10b981) !important;
}

:deep(.prose thead th),
.prose thead th {
  padding: 1rem 0.75rem !important;
  text-align: left !important;
  font-weight: 600 !important;
  font-size: 0.875rem !important;
  color: white !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
  border-bottom: 2px solid #0d9488 !important;
  border-right: 1px solid rgba(255, 255, 255, 0.2) !important;
}

:deep(.prose thead th:last-child),
.prose thead th:last-child {
  border-right: none !important;
}

:deep(.prose tbody tr),
.prose tbody tr {
  border-bottom: 1px solid #f3f4f6 !important;
  transition: background-color 0.2s ease !important;
}

:deep(.prose tbody tr:hover),
.prose tbody tr:hover {
  background-color: #f8fafc !important;
}

:deep(.prose tbody tr:last-child),
.prose tbody tr:last-child {
  border-bottom: none !important;
}

:deep(.prose tbody td),
.prose tbody td {
  padding: 0.875rem 0.75rem !important;
  font-size: 0.875rem !important;
  line-height: 1.5 !important;
  color: #374151 !important;
  vertical-align: top !important;
  border-right: 1px solid #f3f4f6 !important;
}

:deep(.prose tbody td:last-child),
.prose tbody td:last-child {
  border-right: none !important;
}

:deep(.prose tbody td:first-child),
.prose tbody td:first-child {
  font-weight: 600 !important;
  color: #111827 !important;
  background-color: #f9fafb !important;
}

/* Responsive table styling */
@media (max-width: 768px) {
  :deep(.prose table),
  .prose table {
    font-size: 0.75rem !important;
  }
  
  :deep(.prose thead th),
  :deep(.prose tbody td),
  .prose thead th,
  .prose tbody td {
    padding: 0.5rem 0.375rem !important;
  }
  
  :deep(.prose thead th),
  .prose thead th {
    font-size: 0.75rem !important;
  }
}
</style> 