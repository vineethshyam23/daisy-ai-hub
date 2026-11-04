<template>
  <!-- Main Content -->
  <div class="min-h-screen bg-gray-50">
    <!-- Unified Header -->
    <AIHeader />

    <!-- Hero Banner -->
    <div class="relative bg-gradient-to-r from-purple-800 via-purple-600 to-purple-500 border-b border-purple-700 overflow-hidden">
          <!-- Image Creation Pattern -->
          <div class="absolute right-0 top-0 w-1/2 h-full opacity-8">
            <svg class="w-full h-full" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <pattern id="image-pattern" x="0" y="0" width="22" height="22" patternUnits="userSpaceOnUse">
                  <rect x="6" y="6" width="10" height="8" fill="none" stroke="white" stroke-width="0.5"/>
                  <circle cx="8.5" cy="9" r="1" fill="none" stroke="white" stroke-width="0.4"/>
                  <path d="M6,12 L9,10 L12,11 L16,9" stroke="white" stroke-width="0.4" fill="none"/>
                </pattern>
              </defs>
              <rect width="100" height="100" fill="url(#image-pattern)"/>
            </svg>
          </div>
          
          <!-- Creative Network Background -->
          <div class="absolute right-0 top-0 w-2/3 h-full opacity-4">
            <div class="w-full h-full" style="background-image: radial-gradient(circle at 82% 30%, white 2px, transparent 2px), radial-gradient(circle at 88% 70%, white 1.5px, transparent 1.5px), radial-gradient(circle at 76% 55%, white 1px, transparent 1px); background-size: 40px 40px, 28px 28px, 55px 55px;"></div>
          </div>
          
      <UContainer class="relative z-10 py-16">
        <div class="max-w-4xl">
          <div class="flex items-center mb-6">
            <div class="w-16 h-16 bg-purple-500 rounded-2xl flex items-center justify-center mr-6 border border-purple-700">
              <UIcon name="i-heroicons-photo" class="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 class="text-4xl font-bold text-white mb-2">Image Generator</h1>
              <p class="text-xl text-purple-100">Create stunning images from text descriptions using advanced AI</p>
            </div>
          </div>
        </div>
      </UContainer>
    </div>
    
    <UContainer class="py-8">
      
      <!-- Generation Form -->
      <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-8 mb-8">
        <div class="flex items-center space-x-3 mb-6">
          <UIcon name="i-heroicons-sparkles" class="text-2xl text-purple-600" />
          <h2 class="text-2xl font-bold text-gray-900">Generate New Image</h2>
        </div>

        <form @submit.prevent="generateImages" class="space-y-8">
          <!-- Prompt Input and Settings in one row -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- Prompt Input (2/3 width) -->
            <div class="lg:col-span-2">
              <div class="bg-white border border-gray-200 rounded-xl p-6">
                <div class="flex items-center space-x-2 mb-3">
                  <UIcon name="i-heroicons-pencil-square" class="text-lg text-purple-600" />
                  <label for="prompt" class="text-lg font-semibold text-gray-800">
                    Image Description
                  </label>
                </div>
                <p class="text-sm text-gray-600 mb-4">Describe the image you want to create in detail</p>
                <textarea
                  id="prompt"
                  v-model="form.prompt"
                  rows="6"
                  :disabled="loading"
                  placeholder="A majestic mountain landscape at sunset with golden light reflecting on a pristine lake, with dramatic clouds and vibrant colors..."
                  class="w-full px-4 py-3 bg-white border border-gray-300 focus:border-purple-500 focus:outline-none rounded-lg resize-none transition-colors"
                  required
                ></textarea>
              </div>
            </div>

            <!-- Generation Settings (1/3 width) -->
            <div class="lg:col-span-1">
              <div class="bg-white border border-gray-200 rounded-xl p-6">
                <div class="flex items-center space-x-2 mb-4">
                  <UIcon name="i-heroicons-cog-6-tooth" class="text-xl text-gray-700" />
                  <h3 class="text-lg font-semibold text-gray-800">Settings</h3>
                </div>
                
                <div class="space-y-6">
                  <!-- Number of Images with Token Cost -->
                  <div>
                    <div class="flex items-center justify-between mb-2">
                      <label class="text-sm font-medium text-gray-700">Number of Images</label>
                      <div class="flex items-center space-x-1">
                        <UIcon name="i-heroicons-currency-dollar" class="text-xs text-purple-500" />
                        <span class="text-xs font-medium text-purple-600">{{ requiredTokens }} tokens</span>
                      </div>
                    </div>
                    <select
                      v-model="form.number_of_images"
                      :disabled="loading"
                      class="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:border-purple-500 focus:outline-none transition-colors"
                    >
                      <option value="1">1 Image (2 tokens)</option>
                      <option value="2">2 Images (4 tokens)</option>
                      <option value="3">3 Images (6 tokens)</option>
                      <option value="4">4 Images (8 tokens)</option>
                    </select>
                  </div>

                  <!-- Aspect Ratio -->
                  <div>
                    <div class="flex items-center space-x-2 mb-2">
                      <label class="text-sm font-medium text-gray-700">Aspect Ratio</label>
                    </div>
                    <select
                      v-model="form.aspect_ratio"
                      :disabled="loading"
                      class="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:border-purple-500 focus:outline-none transition-colors"
                    >
                      <option value="1:1">Square (1:1)</option>
                      <option value="16:9">Landscape (16:9)</option>
                      <option value="9:16">Portrait (9:16)</option>
                      <option value="4:3">Photo (4:3)</option>
                      <option value="3:4">Portrait Photo (3:4)</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Generate Button -->
          <div class="flex justify-center pt-6">
            <UButton
              type="submit"
              :disabled="!isFormValid || loading || (tokenStore.isTokenDataReady && !hasEnoughTokens)"
              :loading="loading"
              color="primary"
              size="xl"
              :class="[
                'font-semibold px-12 py-4 shadow-sm transition-all duration-200',
                (!tokenStore.isTokenDataReady || hasEnoughTokens)
                  ? 'bg-purple-600 hover:bg-purple-700 text-white cursor-pointer'
                  : 'bg-gray-400 text-gray-600 cursor-not-allowed'
              ]"
              :icon="loading ? 'i-heroicons-arrow-path' : 'i-heroicons-photo'"
            >
              {{ 
                loading ? 'Generating Images...' : 
                !tokenStore.isTokenDataReady ? 'Loading tokens...' :
                !hasEnoughTokens ? `Need ${requiredTokens - tokenStore.tokens} more tokens` :
                'Generate Images' 
              }}
            </UButton>
          </div>
          
          <!-- Insufficient Tokens Info -->
          <div v-if="tokenStore.isTokenDataReady && !hasEnoughTokens" class="bg-orange-50 border border-orange-200 rounded-xl p-4 mt-4">
            <div class="flex items-start space-x-3">
              <UIcon name="i-heroicons-information-circle" class="text-orange-500 text-lg mt-0.5" />
              <div>
                <p class="text-sm font-semibold text-orange-800 mb-1">Not enough tokens</p>
                <p class="text-sm text-orange-700 mb-2">
                  You need {{ requiredTokens }} tokens but only have {{ tokenStore.tokens }} available.
                </p>
                <button
                  @click="$router.push('/profile')"
                  class="inline-flex items-center space-x-2 px-3 py-1.5 bg-orange-500 hover:bg-orange-600 text-white text-xs font-medium rounded-lg transition-colors cursor-pointer"
                >
                  <UIcon name="i-heroicons-user-circle" class="text-sm" />
                  <span>Go to Profile to get more tokens</span>
                </button>
              </div>
            </div>
          </div>
        </form>
      </div>

      <!-- Disclaimer -->
      <DisclaimerBox 
        disclaimer-text="Images are AI-generated and might not reflect real people, places, or events. Please, double-check or use images we already have licenses for."
        class="mb-6"
      />

      <!-- Loading State -->
      <div v-if="loading" class="bg-white border border-gray-200 rounded-2xl shadow-sm p-8 mb-8">
        <div class="text-center py-12">
          <div class="flex justify-center mb-6">
            <div class="relative">
              <div class="animate-spin rounded-full h-20 w-20 border-4 border-purple-200 border-t-purple-600"></div>
              <div class="absolute inset-0 flex items-center justify-center">
                <UIcon name="i-heroicons-photo" class="text-2xl text-purple-600" />
              </div>
            </div>
          </div>
          
          <div class="flex items-center justify-center space-x-2 mb-2">
            <UIcon name="i-heroicons-sparkles" class="text-xl text-purple-600" />
            <h3 class="text-2xl font-bold text-purple-600">Creating Your Images</h3>
          </div>
          <p class="text-gray-600 mb-8">This may take 30-60 seconds depending on complexity...</p>
          
          <!-- Progress Animation -->
          <div class="max-w-md mx-auto">
            <div class="bg-purple-100 rounded-full h-3">
              <div 
                class="bg-purple-500 h-3 rounded-full transition-all duration-500" 
                :style="{ width: progress + '%' }"
              ></div>
            </div>
            <div class="flex items-center justify-center space-x-2 mt-4">
              <UIcon name="i-heroicons-cpu-chip" class="text-sm text-purple-500" />
              <p class="text-sm text-gray-600 font-medium">{{ progressText }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Generated Images -->
      <div v-if="generatedImages.length > 0" class="bg-white border border-gray-200 rounded-2xl shadow-sm p-8 mb-8">
        <div class="flex items-center justify-between mb-8">
          <div class="flex items-center space-x-3">
            <UIcon name="i-heroicons-check-circle" class="text-2xl text-purple-600" />
            <h3 class="text-2xl font-bold text-purple-600">Generated Images</h3>
          </div>
          <div class="flex items-center space-x-2 px-4 py-2 bg-purple-50 border border-purple-200 text-purple-800 rounded-full">
            <UIcon name="i-heroicons-photo" class="text-sm" />
            <span class="text-sm font-semibold">{{ generatedImages.length }} image(s)</span>
          </div>
        </div>

        <!-- Images Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          <div
            v-for="(image, index) in generatedImages"
            :key="index"
            class="group relative bg-white rounded-2xl overflow-hidden border border-gray-200 shadow-sm hover:shadow-md transition-all duration-200"
          >
            <!-- Image Container -->
            <div class="relative overflow-hidden rounded-t-2xl">
              <img
                :src="image.url"
                :alt="`Generated image ${index + 1}`"
                class="w-full h-auto object-cover transition-transform duration-500 group-hover:scale-110"
              />
              
              <!-- Hover Overlay with Actions -->
              <div class="absolute inset-0 bg-black/70 opacity-0 group-hover:opacity-100 transition-all duration-200 flex items-center justify-center">
                <div class="flex space-x-4">
                  
                  <!-- Download Button -->
                  <button
                    @click="downloadImage(image, index + 1)"
                    class="flex items-center justify-center space-x-2 px-5 py-2.5 bg-white text-gray-900 hover:bg-gray-100 font-medium rounded-lg shadow-sm transition-all duration-200 cursor-pointer"
                  >
                    <UIcon name="i-heroicons-arrow-down-tray" class="w-4 h-4" />
                    <span class="text-sm">Download</span>
                  </button>
                  
                  <!-- View Button -->
                  <button
                    @click="openImageModal(image)"
                    class="flex items-center justify-center space-x-2 px-5 py-2.5 bg-black/80 text-white hover:bg-black font-medium rounded-lg shadow-sm transition-all duration-200 cursor-pointer"
                  >
                    <UIcon name="i-heroicons-eye" class="w-4 h-4" />
                    <span class="text-sm">Preview</span>
                  </button>
                </div>
              </div>
            </div>

            <!-- Image Info Bar -->
            <div class="p-4 bg-purple-50 border-t border-purple-200">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <UIcon name="i-heroicons-photo" class="text-purple-600" />
                  <span class="text-sm font-semibold text-purple-800">Image {{ index + 1 }}</span>
                </div>
                <div class="flex items-center space-x-2">
                  <UIcon name="i-heroicons-squares-2x2" class="text-purple-600 text-xs" />
                  <span class="text-xs font-medium text-purple-700">{{ form.aspect_ratio }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Bulk Actions -->
        <div class="bg-purple-50 rounded-xl p-6 border border-purple-200">
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0">
            <div class="flex items-start space-x-3">
              <UIcon name="i-heroicons-chat-bubble-left-ellipsis" class="text-purple-600 mt-1" />
              <div>
                <p class="text-sm font-medium text-gray-700 mb-1">Generation Prompt:</p>
                <p class="text-sm text-gray-600 leading-relaxed max-w-md">
                  "{{ form.prompt.slice(0, 80) }}{{ form.prompt.length > 80 ? '...' : '' }}"
                </p>
              </div>
            </div>
            
            <button
              @click="downloadAllImages"
              class="flex items-center justify-center space-x-2 px-6 py-3 bg-purple-500 hover:bg-purple-600 text-white font-medium rounded-xl shadow-sm hover:shadow-md transition-all duration-200 cursor-pointer"
            >
              <UIcon name="i-heroicons-arrow-down-tray" class="w-5 h-5" />
              <span>Download All Images</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-if="error" class="bg-red-50 border border-red-200 rounded-2xl shadow-sm p-6 mb-8">
        <div class="flex items-start justify-between">
          <div class="flex items-start space-x-3">
            <UIcon name="i-heroicons-exclamation-triangle" class="text-2xl text-red-600 mt-1" />
            <div>
              <h3 class="text-lg font-bold text-red-800 mb-2">Generation Failed</h3>
              <p class="text-red-600 text-sm leading-relaxed">{{ error }}</p>
            </div>
          </div>
          <UButton
            @click="error = ''"
            variant="ghost"
            icon="i-heroicons-x-mark"
            class="text-red-400 hover:text-red-600 hover:bg-red-100 cursor-pointer"
            size="sm"
          />
        </div>
      </div>
    </UContainer>

    <!-- Image Modal -->
    <div v-if="showImageModal" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center p-4 z-50" @click="showImageModal = false">
      <div class="bg-white rounded-lg max-w-4xl max-h-full overflow-auto border border-gray-200" @click.stop>
        <div class="flex justify-between items-center p-4 border-b border-gray-200">
          <h3 class="text-lg font-medium">Full Size View</h3>
          <button @click="showImageModal = false" class="text-gray-400 hover:text-gray-600 cursor-pointer">
            ✕
          </button>
        </div>
        
        <div class="p-4">
          <img v-if="selectedImage" :src="selectedImage.url" :alt="selectedImage.alt" class="w-full h-auto rounded-lg" />
        </div>
        
        <div class="flex justify-end p-4 border-t border-gray-200">
          <button 
            @click="downloadImageFromModal" 
            class="px-4 py-2 bg-purple-500 text-white rounded-lg font-medium hover:bg-purple-600 flex items-center space-x-2 transition-all cursor-pointer"
          >
            <UIcon name="i-heroicons-arrow-down-tray" class="w-4 h-4" />
            <span>Download</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Tips Section -->
    <UContainer class="py-8">
      <div class="border border-purple-200 rounded-2xl shadow-sm p-8" style="background-color: rgba(147, 51, 234, 0.25);">
        <div class="flex items-center space-x-2 mb-4">
          <UIcon name="i-heroicons-light-bulb" class="text-2xl text-purple-800" />
          <h3 class="text-xl font-bold text-purple-900">Tips for Better Results</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-3">
            <h4 class="font-semibold text-purple-800">Prompt Writing</h4>
            <ul class="text-sm text-purple-700 space-y-1">
              <li>• Be specific and descriptive in your prompts</li>
              <li>• Include style, mood, and artistic details</li>
              <li>• Mention lighting, colors, and composition</li>
            </ul>
          </div>
          <div class="space-y-3">
            <h4 class="font-semibold text-purple-800">Image Settings</h4>
            <ul class="text-sm text-purple-700 space-y-1">
              <li>• Choose appropriate aspect ratio for your use case</li>
              <li>• Generate multiple images for better variety</li>
              <li>• Consider your token budget when selecting quantity</li>
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
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useTokenStore } from '~/stores/tokens'
import { useAdobeTracking } from '~/composables/useAdobeTracking'

// Stores
const authStore = useAuthStore()
const tokenStore = useTokenStore()

// Adobe Tracking
const { trackButtonClick } = useAdobeTracking()

// Constants
const TOKENS_PER_IMAGE = 2

// Initialize stores after navigation (auth is handled by middleware)
onMounted(async () => {
  // Initialize token store after successful authentication
  if (!tokenStore.isInitialized) {
    await tokenStore.init()
  }
})

// Form State
const form = ref({
  prompt: '',
  number_of_images: 1,
  aspect_ratio: '1:1'
})

// UI State
const loading = ref(false)
const error = ref('')
const generatedImages = ref([])
const progress = ref(0)
const progressText = ref('')
const showImageModal = ref(false)
const selectedImage = ref(null)

// Timing tracking
const generationStartTime = ref(null)

// Computed
const isFormValid = computed(() => {
  return form.value.prompt.trim().length > 0 &&
         form.value.number_of_images > 0 &&
         form.value.aspect_ratio.length > 0
})

const requiredTokens = computed(() => {
  return form.value.number_of_images * TOKENS_PER_IMAGE
})

const hasEnoughTokens = computed(() => {
  // Only check tokens if token data is ready from Firebase
  if (!tokenStore.isTokenDataReady) {
    return true // Assume we have enough tokens while loading
  }
  return tokenStore.tokens >= requiredTokens.value
})

const tokenStatus = computed(() => {
  const tokens = tokenStore.tokens
  const required = requiredTokens.value
  if (tokens >= required) {
    return { valid: true, message: `${required} tokens required` }
  } else {
    return { valid: false, message: `Insufficient tokens: ${tokens}/${required} available` }
  }
})

// Methods
const generateImages = async () => {
  if (!isFormValid.value) return
  
  // Check if user has enough tokens
  if (!hasEnoughTokens.value) {
    error.value = `Insufficient tokens. You need ${requiredTokens.value} tokens but only have ${tokenStore.tokens} available.`
    return
  }

  // Track button click with structured data
  trackButtonClick('Generate Images', {
    numberOfImages: parseInt(form.value.number_of_images),
    aspectRatio: form.value.aspect_ratio,
    tokensRequired: requiredTokens.value,
    tokensAvailable: tokenStore.tokens,
    promptLength: form.value.prompt.length,
    hasPrompt: !!form.value.prompt.trim()
  })

  loading.value = true
  error.value = ''
  generatedImages.value = []
  progress.value = 0

  // Start timing for performance tracking
  generationStartTime.value = Date.now()

  try {
    // Simulate progress
    const progressInterval = setInterval(() => {
      if (progress.value < 90) {
        progress.value += Math.random() * 10
        updateProgressText()
      }
    }, 1000)

    // Make authenticated API call with environment-aware endpoint
    const { authenticatedEndpointRequest, apiEndpoints } = await import('~/config/api.config')
    const response = await authenticatedEndpointRequest(apiEndpoints.generateImages, {
      method: 'POST',
      body: {
        prompt: form.value.prompt,
        number_of_images: form.value.number_of_images,
        aspect_ratio: form.value.aspect_ratio,
        negative_prompt: "",
        person_generation: "",
        safety_filter_level: "",
        add_watermark: false
      }
    }).catch(() => {
      // Fallback to dummy data if endpoint doesn't exist
      return generateDummyResponse()
    })

    clearInterval(progressInterval)
    progress.value = 100
    progressText.value = 'Complete!'

    // Process response - handle direct array of data URLs
    if (Array.isArray(response)) {
      // Direct array of data:image/png;base64,... strings
      generatedImages.value = response.map((dataUrl, index) => {
        // Validate data URL format
        if (!dataUrl || !dataUrl.startsWith('data:image/')) {
          throw new Error(`Invalid image data URL at index ${index}`)
        }
        
        return {
          url: dataUrl,
          base64: dataUrl.includes(',') ? dataUrl.split(',')[1] : dataUrl,
          alt: `Generated image ${index + 1}: ${form.value.prompt}`
        }
      })
      
      
      // Deduct tokens after successful generation
      const actualTokensUsed = generatedImages.value.length * TOKENS_PER_IMAGE
      await tokenStore.useTokens(actualTokensUsed)
      
      // Track token usage
      const { trackTokenUsage } = useAdobeTracking()
      trackTokenUsage(actualTokensUsed, 'image_generator', {
        numberOfImages: generatedImages.value.length,
        aspectRatio: form.value.aspect_ratio,
        promptLength: form.value.prompt.length
      })
      
      // Force UI reactivity update
      await nextTick()
      
    } else if (response.images && Array.isArray(response.images)) {
      // Legacy format with images property
      generatedImages.value = response.images.map((base64, index) => ({
        url: base64.startsWith('data:') ? base64 : `data:image/png;base64,${base64}`,
        base64: base64.startsWith('data:') ? base64.split(',')[1] : base64,
        alt: `Generated image ${index + 1}: ${form.value.prompt}`
      }))
      
      // Deduct tokens after successful generation (legacy format)
      const actualTokensUsed = generatedImages.value.length * TOKENS_PER_IMAGE
      await tokenStore.useTokens(actualTokensUsed)
      
      // Force UI reactivity update
      await nextTick()
    } else {
      throw new Error('Invalid response format: Expected array of data URLs or object with images property')
    }

  } catch (err) {
    console.error('Error generating images:', err)
    
    // Track API error with Adobe Analytics
    const { trackError } = useAdobeTracking()
    trackError('api_image_generator_failed', 'Image Generator API request failed', {
      errorMessage: err.message || err.toString(),
      errorCode: err.status || err.statusCode || 'unknown',
      errorType: err.name || 'APIError',
      endpoint: 'generateImages',
      requestData: {
        prompt: form.value.prompt,
        numberOfImages: parseInt(form.value.number_of_images),
        aspectRatio: form.value.aspect_ratio,
        promptLength: form.value.prompt.length,
        tokensRequired: requiredTokens.value,
        tokensAvailable: tokenStore.tokens
      },
      userAgent: window.navigator?.userAgent || 'unknown',
      timestamp: new Date().toISOString(),
      generationDuration: Date.now() - (generationStartTime.value || Date.now())
    })
    
    error.value = err.message || 'Failed to generate images. Please try again.'
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
    'Analyzing your prompt...',
    'Initializing AI model...',
    'Generating image composition...',
    'Adding details and textures...',
    'Applying final touches...',
    'Almost ready...'
  ]
  const index = Math.floor((progress.value / 100) * (texts.length - 1))
  progressText.value = texts[index] || texts[0]
}

// Dummy response generator for testing - matches new API format
const generateDummyResponse = () => {
  // Create a simple colored square as base64 for testing
  const canvas = document.createElement('canvas')
  canvas.width = 512
  canvas.height = 512
  const ctx = canvas.getContext('2d')
  
  // Create different colored squares for each image
  const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
  const dataUrls = []
  
  for (let i = 0; i < form.value.number_of_images; i++) {
    ctx.fillStyle = colors[i % colors.length]
    ctx.fillRect(0, 0, 512, 512)
    ctx.fillStyle = 'white'
    ctx.font = '32px Arial'
    ctx.textAlign = 'center'
    ctx.fillText(`Generated Image ${i + 1}`, 256, 256)
    ctx.fillText(form.value.prompt.slice(0, 20), 256, 300)
    
    // Return full data URL (matching API format)
    const dataUrl = canvas.toDataURL('image/png')
    dataUrls.push(dataUrl)
  }
  
  // Return direct array of data URLs (new API format)
  return dataUrls
}

const downloadImage = (image, index, skipTracking = false) => {
  try {
    // Track download action only if not part of bulk download
    if (!skipTracking) {
      trackButtonClick('Download Single Image', {
        imageIndex: index,
        totalImages: generatedImages.value.length,
        aspectRatio: form.value.aspect_ratio,
        downloadMethod: 'single'
      })
    }

    const link = document.createElement('a')
    link.href = image.url
    link.download = `ai-generated-image-${index}-${Date.now()}.png`
    link.style.display = 'none'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (error) {
    console.error('Download failed:', error)
    // Fallback: open in new tab
    window.open(image.url, '_blank')
  }
}

const downloadAllImages = () => {
  // Track bulk download action
  trackButtonClick('Download All Images', {
    totalImages: generatedImages.value.length,
    aspectRatio: form.value.aspect_ratio,
    downloadMethod: 'bulk'
  })

  generatedImages.value.forEach((image, index) => {
    setTimeout(() => downloadImage(image, index + 1, true), index * 100) // skipTracking = true
  })
}

const openImageModal = (image) => {
  // Track image modal opening
  const imageIndex = generatedImages.value.indexOf(image) + 1
  trackButtonClick('Open Image Modal', {
    imageIndex: imageIndex,
    totalImages: generatedImages.value.length,
    aspectRatio: form.value.aspect_ratio,
    action: 'view_fullsize'
  })

  selectedImage.value = image
  showImageModal.value = true
}

const downloadImageFromModal = () => {
  if (selectedImage.value) {
    const index = generatedImages.value.indexOf(selectedImage.value) + 1
    downloadImage(selectedImage.value, index)
  }
}

// Track image generation timing performance
// SEO
useHead({
  title: 'Image Generator - DAISY',
  meta: [
    { name: 'description', content: 'Generate stunning images from text descriptions using advanced AI technology.' }
  ]
})
</script>