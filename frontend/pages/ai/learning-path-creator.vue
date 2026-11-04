<template>
  <!-- Loading State while auth is being determined -->
  <div v-if="!authStore.isInitialized" class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-25 to-purple-50 flex items-center justify-center">
    <div class="text-center">
      <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-500 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl animate-pulse">
        <UIcon name="i-heroicons-academic-cap" class="w-8 h-8 text-white" />
      </div>
      <h2 class="text-2xl font-bold bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent mb-2">
        DAISY
      </h2>
      <p class="text-gray-600 font-light">Loading Learning Path Creator...</p>
      <div class="mt-4 flex justify-center">
        <div class="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    </div>
  </div>

  <!-- Main Content - Only show if authenticated -->
  <div v-else-if="authStore.isAuthenticated" class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-25 to-purple-50">
    <!-- Unified Header -->
    <AIHeader />

    <!-- Hero Banner -->
    <div class="relative bg-gradient-to-r from-blue-800 via-indigo-600 to-purple-500 border-b border-blue-700 overflow-hidden">
      <!-- Learning Path Pattern -->
      <div class="absolute right-0 top-0 w-1/2 h-full opacity-8">
        <svg class="w-full h-full" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="learning-path-pattern" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
              <!-- Learning nodes -->
              <circle cx="10" cy="5" r="1.5" fill="white" opacity="0.4"/>
              <circle cx="5" cy="12" r="1.5" fill="white" opacity="0.5"/>
              <circle cx="15" cy="15" r="1.5" fill="white" opacity="0.3"/>
              <!-- Connection paths -->
              <path d="M10,5 Q7,8 5,12" stroke="white" stroke-width="0.3" fill="none" opacity="0.4"/>
              <path d="M5,12 Q10,13 15,15" stroke="white" stroke-width="0.3" fill="none" opacity="0.4"/>
            </pattern>
          </defs>
          <rect width="100" height="100" fill="url(#learning-path-pattern)"/>
        </svg>
      </div>
      
      <!-- Knowledge Network Background -->
      <div class="absolute right-0 top-0 w-2/3 h-full opacity-4">
        <div class="w-full h-full" style="background-image: radial-gradient(circle at 85% 25%, white 2px, transparent 2px), radial-gradient(circle at 75% 75%, white 1.5px, transparent 1.5px), radial-gradient(circle at 90% 55%, white 1px, transparent 1px); background-size: 48px 48px, 36px 36px, 64px 64px;"></div>
      </div>
      
      <UContainer class="relative z-10 py-16">
        <div class="max-w-4xl">
          <div class="flex items-center mb-6">
            <div class="w-16 h-16 bg-blue-500 rounded-2xl flex items-center justify-center mr-6 border border-blue-700">
              <UIcon name="i-heroicons-academic-cap" class="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 class="text-4xl font-bold text-white mb-2">Learning Path Creator</h1>
              <p class="text-xl text-blue-100">Personalized AI-Generated Learning Journeys</p>
            </div>
          </div>
        </div>
      </UContainer>
    </div>
    
    <UContainer class="py-8">

      <!-- Learning Path Form -->
      <div class="bg-white/90 backdrop-blur-sm rounded-3xl shadow-xl p-8 mb-8 border border-blue-100">
        <div class="flex items-center space-x-3 mb-6">
          <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-500 rounded-2xl flex items-center justify-center">
            <UIcon name="i-heroicons-clipboard-document-list" class="w-6 h-6 text-white" />
          </div>
          <h2 class="text-2xl font-bold text-gray-900">Create Your Learning Path</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <!-- Skill Field -->
          <div class="space-y-2">
            <label class="block text-sm font-semibold text-gray-700">
              Skill to Learn
              <span class="text-red-500 ml-1">*</span>
            </label>
            <input
              v-model="formData.skill"
              type="text"
              class="w-full px-4 py-3 text-gray-900 bg-white border border-blue-200 rounded-xl focus:border-blue-400 focus:ring-2 focus:ring-blue-100 focus:outline-none transition-all"
              placeholder="e.g., Project Management, Data Science, Python Programming"
              maxlength="100"
            />
            <p class="text-xs text-gray-500">Enter the skill or subject you want to learn</p>
          </div>

          <!-- Skill Level Field -->
          <div class="space-y-2">
            <label class="block text-sm font-semibold text-gray-700">
              Current Skill Level
              <span class="text-red-500 ml-1">*</span>
            </label>
            <select
              v-model="formData.skill_level"
              class="w-full px-4 py-3 text-gray-900 bg-white border border-blue-200 rounded-xl focus:border-blue-400 focus:ring-2 focus:ring-blue-100 focus:outline-none transition-all"
            >
              <option value="">Select your current level</option>
              <option value="Complete Beginner">Complete Beginner</option>
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advanced">Advanced</option>
            </select>
            <p class="text-xs text-gray-500">Choose your current knowledge level in this skill</p>
          </div>

          <!-- Target Time Field -->
          <div class="space-y-2">
            <label class="block text-sm font-semibold text-gray-700">
              Target Timeframe
              <span class="text-red-500 ml-1">*</span>
            </label>
            <select
              v-model="formData.target_time"
              class="w-full px-4 py-3 text-gray-900 bg-white border border-blue-200 rounded-xl focus:border-blue-400 focus:ring-2 focus:ring-blue-100 focus:outline-none transition-all"
            >
              <option value="">Select target timeframe</option>
              <option value="1 month">1 month</option>
              <option value="2 months">2 months</option>
              <option value="3 months">3 months</option>
              <option value="6 months">6 months</option>
              <option value="1 year">1 year</option>
            </select>
            <p class="text-xs text-gray-500">How long do you want to spend learning this skill?</p>
          </div>

          <!-- Study Commitment Field -->
          <div class="space-y-2">
            <label class="block text-sm font-semibold text-gray-700">
              Weekly Study Time
              <span class="text-red-500 ml-1">*</span>
            </label>
            <select
              v-model="formData.study_commitment"
              class="w-full px-4 py-3 text-gray-900 bg-white border border-blue-200 rounded-xl focus:border-blue-400 focus:ring-2 focus:ring-blue-100 focus:outline-none transition-all"
            >
              <option value="">Select weekly commitment</option>
              <option value="1-2 hours per week">1-2 hours per week</option>
              <option value="3-5 hours per week">3-5 hours per week</option>
              <option value="5-10 hours per week">5-10 hours per week</option>
              <option value="> 10 hours per week">> 10 hours per week</option>
            </select>
            <p class="text-xs text-gray-500">How many hours can you dedicate weekly to learning?</p>
          </div>
        </div>

        <!-- Template Section -->
        <div v-if="templateStore.getTemplatesForAssistant('learning-path-creator').length > 0" class="bg-gradient-to-br from-blue-50/50 to-purple-50/30 rounded-2xl p-6 border border-blue-200 mb-6">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-xl flex items-center justify-center">
                <UIcon name="i-heroicons-bookmark" class="w-5 h-5 text-white" />
              </div>
              <h3 class="text-lg font-semibold text-gray-900">Learning Templates</h3>
            </div>
            <button
              @click="showTemplateModal = true"
              class="inline-flex items-center space-x-1 px-3 py-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white text-sm rounded-lg hover:from-blue-600 hover:to-purple-600 transition-all shadow-sm hover:shadow-md cursor-pointer"
            >
              <UIcon name="i-heroicons-plus" class="w-4 h-4" />
              <span>Create Template</span>
            </button>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            <div
              v-for="template in templateStore.getTemplatesForAssistant('learning-path-creator')"
              :key="template.id"
              @click="selectTemplate(template)"
              :class="[
                'relative text-left p-4 rounded-lg transition-all cursor-pointer group border',
                selectedTemplateId === template.id 
                  ? 'bg-blue-100 border-blue-400 shadow-md'
                  : 'bg-white border-blue-200 hover:border-blue-300 hover:bg-blue-50'
              ]"
            >
              <!-- Edit/Delete buttons -->
              <div class="absolute top-2 right-2 flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity z-10">
                <button
                  @click.stop="editTemplate(template)"
                  class="p-1 text-gray-400 hover:text-blue-500 rounded-md hover:bg-blue-100 transition-colors"
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
                <h4 class="text-sm font-semibold text-gray-900 mb-1">{{ template.title }}</h4>
                <p v-if="template.description" class="text-xs text-gray-600 line-clamp-2">{{ template.description }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Create Learning Path Button -->
        <div class="flex flex-col items-center space-y-4">
          <button
            @click="createLearningPath"
            :disabled="!canCreatePath || loading"
            :class="[
              'flex items-center justify-center px-8 py-4 rounded-xl font-semibold shadow-lg transition-all duration-300',
              canCreatePath && !loading
                ? 'bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white hover:shadow-xl transform hover:scale-105 cursor-pointer'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            ]"
          >
            <span v-if="loading">Creating Learning Path...</span>
            <span v-else-if="!isFormValid">Complete all required fields</span>
            <span v-else-if="!hasEnoughTokens">Insufficient tokens ({{ tokenStore.tokens }}/{{ requiredTokens }})</span>
            <span v-else>Create Learning Path ({{ requiredTokens }} token{{ requiredTokens !== 1 ? 's' : '' }})</span>
          </button>
        </div>
      </div>

      <!-- Loading Animation -->
      <div v-if="loading" class="bg-white/90 backdrop-blur-sm rounded-3xl shadow-xl p-8 mb-8 border border-blue-100">
        <div class="text-center py-12">
          <div class="flex justify-center mb-6">
            <div class="relative">
              <div class="animate-spin rounded-full h-20 w-20 border-4 border-blue-200 border-t-blue-600"></div>
              <div class="absolute inset-0 flex items-center justify-center">
                <UIcon name="i-heroicons-academic-cap" class="text-2xl text-blue-600" />
              </div>
            </div>
          </div>
          
          <div class="flex items-center justify-center space-x-2 mb-2">
            <UIcon name="i-heroicons-sparkles" class="text-xl text-blue-600" />
            <h3 class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Creating Your Learning Path</h3>
          </div>
          <p class="text-gray-600 font-light mb-8">Generating personalized learning recommendations...</p>
          
          <!-- Progress Animation -->
          <div class="max-w-md mx-auto">
            <div class="bg-blue-100 rounded-full h-3 shadow-inner">
              <div 
                class="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full transition-all duration-500 shadow-lg" 
                :style="{ width: progress + '%' }"
              ></div>
            </div>
            <div class="flex items-center justify-center space-x-2 mt-4">
              <UIcon name="i-heroicons-cpu-chip" class="text-sm text-blue-500" />
              <p class="text-sm text-gray-600 font-medium">{{ progressText }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Learning Path Result -->
      <div v-if="learningPathResult" class="bg-white/90 backdrop-blur-sm rounded-3xl shadow-xl p-8 mb-8 border border-blue-100">
        <div class="flex items-center justify-between mb-8">
          <div class="flex items-center space-x-3">
            <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-500 rounded-2xl flex items-center justify-center">
              <UIcon name="i-heroicons-check-circle" class="w-6 h-6 text-white" />
            </div>
            <div>
              <h3 class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Learning Path Created</h3>
              <p class="text-sm text-gray-600 mt-1 flex items-center space-x-1">
                <UIcon name="i-heroicons-information-circle" class="w-4 h-4 text-blue-500" />
                <span>{{ formData.skill }} • {{ formData.target_time }} • {{ formData.study_commitment }}</span>
              </p>
            </div>
          </div>
          <div class="flex items-center space-x-3">
            <button
              @click="downloadPDF"
              :disabled="generatingPDF"
              class="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 disabled:from-gray-400 disabled:to-gray-500 text-white font-medium rounded-lg shadow-lg transition-all cursor-pointer disabled:cursor-not-allowed"
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
                <span>Learning path copied to clipboard!</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Learning Path Content -->
        <div class="bg-gradient-to-br from-blue-50/50 to-purple-50/30 rounded-2xl p-6 border border-blue-200">
          <div class="prose max-w-none" v-html="learningPathResult"></div>
        </div>

        <!-- Citations Section -->
        <div v-if="citations && (citations.search_queries?.length > 0 || citations.sources?.length > 0)" class="mt-6 bg-gray-50 rounded-xl p-4">
          <h4 class="text-sm font-semibold text-gray-700 mb-3 flex items-center space-x-2">
            <UIcon name="i-heroicons-document-text" class="w-4 h-4" />
            <span>Research Sources</span>
          </h4>
          
          <!-- Search Queries -->
          <div v-if="citations.search_queries?.length > 0" class="mb-3">
            <p class="text-xs text-gray-600 mb-2">Search queries used:</p>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="query in citations.search_queries" 
                :key="query"
                class="inline-flex items-center px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-md"
              >
                <UIcon name="i-heroicons-magnifying-glass" class="w-3 h-3 mr-1" />
                {{ query }}
              </span>
            </div>
          </div>
          
          <!-- Sources -->
          <div v-if="citations.sources?.length > 0" class="space-y-2">
            <p class="text-xs text-gray-600">Sources referenced:</p>
            <div class="space-y-1">
              <a 
                v-for="(source, index) in citations.sources" 
                :key="index"
                :href="source.url || source"
                target="_blank"
                rel="noopener noreferrer"
                class="block text-xs text-blue-600 hover:text-blue-800 underline"
              >
                {{ source.title || source.url || source }}
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-if="error" class="bg-gradient-to-br from-red-50/90 to-rose-50/80 backdrop-blur-sm border border-red-200 rounded-2xl shadow-xl p-6 mb-8">
        <div class="flex items-start justify-between">
          <div class="flex items-start space-x-3">
            <UIcon name="i-heroicons-exclamation-triangle" class="text-2xl text-red-600 mt-1" />
            <div>
              <h3 class="text-lg font-bold text-red-800 mb-2">Learning Path Creation Failed</h3>
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
      <div class="mt-8 border border-blue-200 rounded-2xl shadow-sm p-8" style="background-color: rgba(59, 130, 246, 0.25);">
        <div class="flex items-center space-x-2 mb-4">
          <UIcon name="i-heroicons-light-bulb" class="text-2xl text-blue-800" />
          <h3 class="text-xl font-bold text-blue-900">Tips for Better Learning Paths</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-3">
            <h4 class="font-semibold text-blue-800">Skill Selection</h4>
            <ul class="text-sm text-blue-700 space-y-1">
              <li>• Be specific about the skill you want to learn</li>
              <li>• Include relevant context or specialization</li>
              <li>• Consider your career goals and interests</li>
            </ul>
          </div>
          <div class="space-y-3">
            <h4 class="font-semibold text-blue-800">Time Management</h4>
            <ul class="text-sm text-blue-700 space-y-1">
              <li>• Be realistic about your available time</li>
              <li>• Consider your current commitments</li>
              <li>• Allow flexibility for unexpected challenges</li>
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
      :assistant-type="'learning-path-creator'"
      :color-scheme="'blue'"
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
const { trackButtonClick, trackTokenUsage, trackError } = useAdobeTracking()

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
      console.error('Learning Path Creator: Error initializing token store:', error)
    }
  }
  
  // Initialize template store
  if (!templateStore.isInitialized) {
    await templateStore.init()
  }
})

// Watch for auth changes
watch(() => authStore.isAuthenticated, (isAuthenticated) => {
  if (!isAuthenticated) {
    navigateTo('/login')
  }
})

// Form data
const formData = ref({
  skill: '',
  skill_level: '',
  target_time: '',
  study_commitment: ''
})

// State
const loading = ref(false)
const error = ref('')
const learningPathResult = ref('')
const citations = ref(null)
const progress = ref(0)
const progressText = ref('')
const copyConfirmation = ref(false)
const generatingPDF = ref(false)

// Template state
const showTemplateModal = ref(false)
const editingTemplate = ref(null)
const selectedTemplateId = ref(null)

// Token logic
const requiredTokens = computed(() => {
  return tokenStore.getTokenCost('learning-path-creator')
})

const hasEnoughTokens = computed(() => {
  return tokenStore.tokens >= requiredTokens.value
})

// Form validation
const isFormValid = computed(() => {
  return formData.value.skill.trim() &&
         formData.value.skill_level &&
         formData.value.target_time &&
         formData.value.study_commitment
})

const canCreatePath = computed(() => {
  return isFormValid.value && hasEnoughTokens.value
})

const createLearningPath = async () => {
  if (!canCreatePath.value || loading.value) return

  // Track learning path creation start
  trackButtonClick('Create Learning Path', {
    skill: formData.value.skill,
    skillLevel: formData.value.skill_level,
    targetTime: formData.value.target_time,
    studyCommitment: formData.value.study_commitment,
    tokensRequired: requiredTokens.value,
    tokensAvailable: tokenStore.tokens
  })

  loading.value = true
  error.value = ''
  learningPathResult.value = ''
  citations.value = null
  progress.value = 0

  try {
    // Start progress animation
    const progressInterval = setInterval(() => {
      if (progress.value < 90) {
        progress.value += Math.random() * 10
        updateProgressText()
      }
    }, 1000)

    // Make authenticated API call
    const { authenticatedEndpointRequest, apiEndpoints } = await import('~/config/api.config')
    
    const response = await authenticatedEndpointRequest(apiEndpoints.learningPathCreator, {
      method: 'POST',
      body: {
        skill: formData.value.skill.trim(),
        skill_level: formData.value.skill_level,
        target_time: formData.value.target_time,
        study_commitment: formData.value.study_commitment
      }
    })

    // Complete progress
    clearInterval(progressInterval)
    progress.value = 100
    progressText.value = 'Complete!'

    // Process the response
    if (response && response.content) {
      // Parse HTML content from the response
      let htmlContent = response.content
      
      // Remove markdown code block wrapper if present
      if (htmlContent.startsWith('```html\n') && htmlContent.endsWith('\n```')) {
        htmlContent = htmlContent.slice(8, -4)
      }
      
      learningPathResult.value = htmlContent
      
      // Store citations if available
      if (response.citations) {
        citations.value = response.citations
      }
      
      // Ensure all links open in new window after DOM update
      await nextTick()
      updateLinksToOpenInNewWindow()
      
      // Deduct tokens and track usage
      try {
        await tokenStore.useTokens(requiredTokens.value)
        
        // Track token usage with Adobe Analytics
        trackTokenUsage(requiredTokens.value, 'learning_path_creator', {
          skill: formData.value.skill,
          skillLevel: formData.value.skill_level,
          targetTime: formData.value.target_time,
          studyCommitment: formData.value.study_commitment,
          responseLength: htmlContent.length,
          hasCitations: !!response.citations,
          citationCount: response.citations?.sources?.length || 0,
          success: true
        })
      } catch (tokenError) {
        console.error('Error deducting tokens:', tokenError)
      }
      
      // Show success notification
      const toast = useToast()
      toast.add({
        title: 'Learning Path Created',
        description: `Your personalized learning path has been generated successfully. ${requiredTokens.value} token(s) used.`,
        color: 'green'
      })
    } else {
      throw new Error('Invalid response format - missing content')
    }

  } catch (err) {
    console.error('Error creating learning path:', err)
    
    // Track API error with Adobe Analytics [[memory:5842320]]
    trackError('api_learning_path_creator_failed', 'Learning Path Creator API request failed', {
      errorMessage: err.message || err.toString(),
      errorCode: err.status || err.statusCode || 'unknown',
      errorType: err.name || 'APIError',
      endpoint: 'learningPathCreator',
      requestData: {
        skill: formData.value.skill,
        skillLevel: formData.value.skill_level,
        targetTime: formData.value.target_time,
        studyCommitment: formData.value.study_commitment,
        tokensRequired: requiredTokens.value,
        tokensAvailable: tokenStore.tokens
      },
      userAgent: window.navigator?.userAgent || 'unknown',
      timestamp: new Date().toISOString()
    })
    
    error.value = err.message || 'Failed to create learning path. Please try again.'
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
    'Analyzing your learning goals...',
    'Researching best learning resources...',
    'Creating personalized curriculum...',
    'Structuring learning milestones...',
    'Generating detailed study plan...',
    'Optimizing for your schedule...',
    'Finalizing your learning path...'
  ]
  const index = Math.floor((progress.value / 100) * (texts.length - 1))
  progressText.value = texts[index] || texts[0]
}

const updateLinksToOpenInNewWindow = () => {
  // Find all links in the learning path result and ensure they open in new window
  const resultContainer = document.querySelector('.prose')
  if (resultContainer) {
    const links = resultContainer.querySelectorAll('a')
    links.forEach(link => {
      // Only modify external links (not internal navigation)
      if (link.href && (link.href.startsWith('http://') || link.href.startsWith('https://'))) {
        link.setAttribute('target', '_blank')
        link.setAttribute('rel', 'noopener noreferrer')
      }
    })
  }
}

const copyToClipboard = async () => {
  if (!learningPathResult.value) return

  try {
    // Track copy action
    trackButtonClick('Copy Learning Path', {
      skill: formData.value.skill,
      pathLength: learningPathResult.value.length,
      copyMethod: 'clipboard'
    })

    // Convert HTML to plain text
    const tempDiv = document.createElement('div')
    tempDiv.innerHTML = learningPathResult.value
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
  if (!learningPathResult.value) return

  generatingPDF.value = true
  
  try {
    // Track PDF download action
    trackButtonClick('Download Learning Path PDF', {
      skill: formData.value.skill,
      pathLength: learningPathResult.value.length,
      downloadFormat: 'pdf'
    })

    // Dynamic import of jspdf
    const { jsPDF } = await import('jspdf')

    // Create new PDF document with more space
    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4'
    })

    // Page settings
    const pageWidth = pdf.internal.pageSize.getWidth()
    const pageHeight = pdf.internal.pageSize.getHeight()
    const margin = 15
    const maxWidth = pageWidth - (margin * 2)
    let currentY = margin

    // Helper function to check if we need a new page
    const checkNewPage = (requiredSpace = 15) => {
      if (currentY + requiredSpace > pageHeight - margin) {
        pdf.addPage()
        currentY = margin
        return true
      }
      return false
    }

    // Add title section
    pdf.setFontSize(24)
    pdf.setFont(undefined, 'bold')
    pdf.setTextColor(59, 130, 246) // Blue color
    pdf.text(`Learning Path: ${formData.value.skill}`, pageWidth / 2, currentY, { align: 'center' })
    currentY += 12
    
    // Add subtitle with parameters
    pdf.setFontSize(12)
    pdf.setFont(undefined, 'normal')
    pdf.setTextColor(107, 114, 128) // Gray color
    const subtitle = `${formData.value.skill_level} • ${formData.value.target_time} • ${formData.value.study_commitment}`
    pdf.text(subtitle, pageWidth / 2, currentY, { align: 'center' })
    currentY += 8
    
    // Add creation date
    pdf.setFontSize(10)
    pdf.setTextColor(156, 163, 175) // Light gray
    const creationDate = `Created on ${new Date().toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    })}`
    pdf.text(creationDate, pageWidth / 2, currentY, { align: 'center' })
    currentY += 10
    
    // Add decorative line
    pdf.setDrawColor(59, 130, 246)
    pdf.setLineWidth(1)
    pdf.line(margin, currentY, pageWidth - margin, currentY)
    currentY += 15

    // Parse HTML content more intelligently
    const tempDiv = document.createElement('div')
    tempDiv.innerHTML = learningPathResult.value
    
    // Helper function to process mixed content (text + links) recursively
    const processMixedContent = (element, xPos, yPos, maxWidth, fontSize = 11, fontWeight = 'normal') => {
      pdf.setFontSize(fontSize)
      let currentX = xPos
      let currentLineY = yPos
      const startY = yPos
      
      // Recursive function to handle all nested elements
      const processNode = (node, inheritedWeight = fontWeight) => {
        if (node.nodeType === 3) { // Text node
          const text = node.textContent
          if (text) {
            pdf.setFont(undefined, inheritedWeight)
            pdf.setTextColor(75, 85, 99)
            
            // Split by spaces but preserve spaces
            const parts = text.split(/(\s+)/)
            parts.forEach(part => {
              if (part.trim()) { // Non-whitespace part
                const partWidth = pdf.getTextWidth(part)
                
                // Check if part fits on current line
                if (currentX + partWidth > maxWidth && currentX > xPos) {
                  currentLineY += fontSize * 0.5 + 2
                  currentX = xPos
                }
                
                pdf.text(part, currentX, currentLineY)
                currentX += partWidth
              } else { // Whitespace
                const spaceWidth = pdf.getTextWidth(' ')
                if (currentX + spaceWidth <= maxWidth) {
                  pdf.text(' ', currentX, currentLineY)
                  currentX += spaceWidth
                }
              }
            })
          }
        } else if (node.nodeType === 1) { // Element node
          const tagName = node.tagName?.toLowerCase()
          const text = node.textContent?.trim()
          
          if (!text) return
          
          switch (tagName) {
            case 'a':
              const linkUrl = node.href || node.getAttribute('href')
              pdf.setFont(undefined, inheritedWeight)
              pdf.setTextColor(59, 130, 246) // Blue for links
              
              const linkWidth = pdf.getTextWidth(text)
              
              // Check if link fits on current line
              if (currentX + linkWidth > maxWidth && currentX > xPos) {
                currentLineY += fontSize * 0.5 + 2
                currentX = xPos
              }
              
              pdf.text(text, currentX, currentLineY)
              
              // Add clickable area if valid URL
              if (linkUrl && (linkUrl.startsWith('http://') || linkUrl.startsWith('https://'))) {
                pdf.link(currentX, currentLineY - 3, linkWidth, fontSize * 0.5 + 1, { url: linkUrl })
              }
              
              currentX += linkWidth
              break
              
            case 'strong':
            case 'b':
              // Process children with bold weight
              Array.from(node.childNodes).forEach(child => {
                processNode(child, 'bold')
              })
              break
              
            case 'em':
            case 'i':
              // Process children with italic
              Array.from(node.childNodes).forEach(child => {
                processNode(child, 'italic')
              })
              break
              
            default:
              // Process children with inherited weight
              Array.from(node.childNodes).forEach(child => {
                processNode(child, inheritedWeight)
              })
              break
          }
        }
      }
      
      // Process all child nodes
      Array.from(element.childNodes).forEach(node => {
        processNode(node)
      })
      
      return Math.max(currentLineY - startY + fontSize * 0.5 + 3, fontSize + 5) // Return height used
    }
    
    // Enhanced function to process any element and extract/render all links
    const processElementWithLinks = (element, xPos, yPos, maxWidth, fontSize = 11, fontWeight = 'normal') => {
      // Check if element contains any links
      const hasLinks = element.querySelector('a') || element.innerHTML.includes('<a')
      
      if (hasLinks) {
        // Use advanced mixed content processing
        return processMixedContent(element, xPos, yPos, maxWidth, fontSize, fontWeight)
      } else {
        // Simple text processing
        const text = element.textContent?.trim() || ''
        if (text) {
          pdf.setFontSize(fontSize)
          pdf.setFont(undefined, fontWeight)
          pdf.setTextColor(75, 85, 99)
          const lines = pdf.splitTextToSize(text, maxWidth)
          pdf.text(lines, xPos, yPos)
          return lines.length * (fontSize * 0.5 + 2) + 3
        }
        return 0
      }
    }

    // Enhanced content processing
    const processContent = (element, level = 0) => {
      if (!element) return
      
      const tagName = element.tagName?.toLowerCase()
      const text = element.textContent?.trim() || ''
      
      if (!text && !['div', 'section', 'article'].includes(tagName)) return
      
      switch (tagName) {
        case 'h1':
          checkNewPage(20)
          currentY += level > 0 ? 8 : 0
          pdf.setFontSize(18)
          pdf.setFont(undefined, 'bold')
          pdf.setTextColor(31, 41, 55)
          const h1Lines = pdf.splitTextToSize(text, maxWidth)
          pdf.text(h1Lines, margin, currentY)
          currentY += h1Lines.length * 7 + 8
          
          // Add underline for h1
          pdf.setDrawColor(59, 130, 246)
          pdf.setLineWidth(0.5)
          pdf.line(margin, currentY - 5, margin + 60, currentY - 5)
          break
          
        case 'h2':
          checkNewPage(18)
          currentY += level > 0 ? 6 : 0
          pdf.setFontSize(16)
          pdf.setFont(undefined, 'bold')
          pdf.setTextColor(55, 65, 81)
          const h2Lines = pdf.splitTextToSize(text, maxWidth)
          pdf.text(h2Lines, margin + (level * 5), currentY)
          currentY += h2Lines.length * 6 + 6
          break
          
        case 'h3':
          checkNewPage(16)
          currentY += level > 0 ? 4 : 0
          pdf.setFontSize(14)
          pdf.setFont(undefined, 'bold')
          pdf.setTextColor(75, 85, 99)
          const h3Lines = pdf.splitTextToSize(text, maxWidth - (level * 5))
          pdf.text(h3Lines, margin + (level * 5), currentY)
          currentY += h3Lines.length * 5 + 5
          break
          
        case 'h4':
        case 'h5':
        case 'h6':
          checkNewPage(14)
          currentY += level > 0 ? 3 : 0
          pdf.setFontSize(12)
          pdf.setFont(undefined, 'bold')
          pdf.setTextColor(107, 114, 128)
          const hLines = pdf.splitTextToSize(text, maxWidth - (level * 5))
          pdf.text(hLines, margin + (level * 5), currentY)
          currentY += hLines.length * 4 + 4
          break
          
        case 'p':
          if (text) {
            checkNewPage(12)
            const heightUsed = processElementWithLinks(element, margin + (level * 5), currentY, maxWidth - (level * 5), 11)
            currentY += heightUsed
          }
          break
          
        case 'ul':
        case 'ol':
          currentY += 2
          Array.from(element.children).forEach((li, index) => {
            const liText = li.textContent?.trim()
            if (liText) {
              checkNewPage(10)
              pdf.setFontSize(11)
              pdf.setFont(undefined, 'normal')
              pdf.setTextColor(75, 85, 99)
              
              const bullet = tagName === 'ul' ? '•' : `${index + 1}.`
              const indentLevel = level * 5 + 5
              
              // Add bullet/number
              pdf.text(bullet, margin + indentLevel, currentY)
              
              // Add list item text with proper wrapping
              const listLines = pdf.splitTextToSize(liText, maxWidth - indentLevel - 8)
              pdf.text(listLines, margin + indentLevel + 8, currentY)
              currentY += listLines.length * 4 + 2
            }
          })
          currentY += 3
          break
          
        case 'table':
          processTable(element)
          break
          
        case 'blockquote':
          checkNewPage(12)
          pdf.setFontSize(11)
          pdf.setFont(undefined, 'italic')
          pdf.setTextColor(107, 114, 128)
          
          // Add quote styling
          pdf.setDrawColor(59, 130, 246)
          pdf.setLineWidth(2)
          pdf.line(margin + (level * 5), currentY - 2, margin + (level * 5), currentY + 8)
          
          const quoteLines = pdf.splitTextToSize(text, maxWidth - (level * 5) - 10)
          pdf.text(quoteLines, margin + (level * 5) + 10, currentY)
          currentY += quoteLines.length * 4 + 6
          break
          
        case 'strong':
        case 'b':
          // Handle inline bold - will be processed by parent
          break
          
        case 'div':
        case 'section':
        case 'article':
          // Process children for container elements
          Array.from(element.children).forEach(child => {
            processContent(child, level)
          })
          break
          
        case 'a':
          // Handle standalone links in main content
          const linkUrl = element.href || element.getAttribute('href')
          if (text) {
            checkNewPage(8)
            pdf.setFontSize(11)
            pdf.setFont(undefined, 'normal')
            pdf.setTextColor(59, 130, 246) // Blue for links
            const linkLines = pdf.splitTextToSize(text, maxWidth - (level * 5))
            
            if (linkUrl && (linkUrl.startsWith('http://') || linkUrl.startsWith('https://'))) {
              linkLines.forEach((line, lineIndex) => {
                const lineY = currentY + (lineIndex * 4)
                pdf.text(line, margin + (level * 5), lineY)
                
                // Add clickable link area
                const textWidth = pdf.getTextWidth(line)
                pdf.link(margin + (level * 5), lineY - 3, textWidth, 4, { url: linkUrl })
              })
            } else {
              pdf.text(linkLines, margin + (level * 5), currentY)
            }
            
            currentY += linkLines.length * 4 + 3
          }
          break
          
        default:
          // Handle any other elements with text content
          if (text && element.nodeType === 1) {
            checkNewPage(8)
            const heightUsed = processElementWithLinks(element, margin + (level * 5), currentY, maxWidth - (level * 5), 11)
            currentY += heightUsed
          }
          break
      }
    }
    
    // Enhanced table processing - convert to structured phases
    const processTable = (table) => {
      const rows = Array.from(table.querySelectorAll('tr'))
      if (rows.length === 0) return
      
      // Extract table headers
      const headerRow = rows[0]
      const headers = Array.from(headerRow.children).map(cell => cell.textContent?.trim() || '')
      
      // Process each data row as a phase
      const dataRows = rows.slice(1) // Skip header row
      
      dataRows.forEach((row, phaseIndex) => {
        const cells = Array.from(row.children)
        
        // Start new page for each phase (except first)
        if (phaseIndex > 0) {
          pdf.addPage()
          currentY = margin
        } else {
          checkNewPage(40)
          currentY += 10
        }
        
        // Phase title
        pdf.setFontSize(16)
        pdf.setFont(undefined, 'bold')
        pdf.setTextColor(59, 130, 246)
        
        const phaseTitle = `Phase ${phaseIndex + 1}`
        pdf.text(phaseTitle, margin, currentY)
        currentY += 10
        
        // Add decorative line under phase title
        pdf.setDrawColor(59, 130, 246)
        pdf.setLineWidth(0.8)
        pdf.line(margin, currentY, margin + 80, currentY)
        currentY += 12
        
        // Process each cell as a section
        cells.forEach((cell, cellIndex) => {
          if (cellIndex >= headers.length) return
          
          const header = headers[cellIndex]
          const content = cell.textContent?.trim() || ''
          
          if (!content || !header) return
          
          checkNewPage(20)
          
          // Section header
          pdf.setFontSize(13)
          pdf.setFont(undefined, 'bold')
          pdf.setTextColor(75, 85, 99)
          pdf.text(header, margin, currentY)
          currentY += 8
          
          // Section content - process HTML within the cell
          const cellDiv = document.createElement('div')
          cellDiv.innerHTML = cell.innerHTML
          
          // Process nested content within the cell
          const processNestedContent = (element, indent = 5) => {
            Array.from(element.children).forEach(child => {
              const tagName = child.tagName?.toLowerCase()
              const text = child.textContent?.trim() || ''
              
              if (!text) return
              
              checkNewPage(8)
              
              switch (tagName) {
                case 'h4':
                case 'h5':
                case 'h6':
                case 'strong':
                  pdf.setFontSize(11)
                  pdf.setFont(undefined, 'bold')
                  pdf.setTextColor(55, 65, 81)
                  const strongLines = pdf.splitTextToSize(text, maxWidth - margin - indent)
                  pdf.text(strongLines, margin + indent, currentY)
                  currentY += strongLines.length * 4 + 3
                  break
                  
                case 'ul':
                case 'ol':
                  Array.from(child.children).forEach((li, liIndex) => {
                    const liText = li.textContent?.trim()
                    if (liText) {
                      checkNewPage(6)
                      pdf.setFontSize(10)
                      
                      const bullet = tagName === 'ul' ? '•' : `${liIndex + 1}.`
                      pdf.setFont(undefined, 'normal')
                      pdf.setTextColor(75, 85, 99)
                      pdf.text(bullet, margin + indent, currentY)
                      
                      // Process list item with potential links
                      const heightUsed = processElementWithLinks(li, margin + indent + 10, currentY, maxWidth - margin - indent - 10, 10)
                      currentY += heightUsed
                    }
                  })
                  currentY += 3
                  break
                  
                case 'a':
                  const linkUrl = child.href || child.getAttribute('href')
                  pdf.setFontSize(10)
                  pdf.setFont(undefined, 'normal')
                  pdf.setTextColor(59, 130, 246) // Blue for links
                  const linkLines = pdf.splitTextToSize(text, maxWidth - margin - indent)
                  
                  // Add clickable link if URL exists
                  if (linkUrl && (linkUrl.startsWith('http://') || linkUrl.startsWith('https://'))) {
                    linkLines.forEach((line, lineIndex) => {
                      const lineY = currentY + (lineIndex * 4)
                      pdf.text(line, margin + indent, lineY)
                      
                      // Add clickable link area for this line
                      const textWidth = pdf.getTextWidth(line)
                      pdf.link(margin + indent, lineY - 3, textWidth, 4, { url: linkUrl })
                    })
                  } else {
                    // Fallback for links without valid URLs
                    pdf.text(linkLines, margin + indent, currentY)
                  }
                  
                  currentY += linkLines.length * 4 + 2
                  break
                  
                case 'p':
                default:
                  const heightUsed = processElementWithLinks(child, margin + indent, currentY, maxWidth - margin - indent, 10)
                  currentY += heightUsed
                  break
              }
            })
          }
          
          if (cellDiv.children.length > 0) {
            processNestedContent(cellDiv)
          } else {
            // Process cell content with potential links
            const heightUsed = processElementWithLinks(cell, margin + 5, currentY, maxWidth - margin - 5, 10)
            currentY += heightUsed
          }
          
          currentY += 8 // Space between sections
        })
        
        currentY += 15 // Extra space between phases
      })
    }

    // Process all content
    if (tempDiv.children.length > 0) {
      Array.from(tempDiv.children).forEach(child => {
        processContent(child, 0)
      })
    } else {
      // Fallback for plain text content
      const plainText = tempDiv.textContent?.trim() || learningPathResult.value.replace(/<[^>]*>/g, '')
      if (plainText) {
        pdf.setFontSize(11)
        pdf.setFont(undefined, 'normal')
        pdf.setTextColor(75, 85, 99)
        
        const lines = pdf.splitTextToSize(plainText, maxWidth)
        lines.forEach(line => {
          checkNewPage(5)
          pdf.text(line, margin, currentY)
          currentY += 5
        })
      }
    }

    // Add footer to all pages
    const totalPages = pdf.internal.getNumberOfPages()
    for (let i = 1; i <= totalPages; i++) {
      pdf.setPage(i)
      pdf.setFontSize(8)
      pdf.setFont(undefined, 'normal')
      pdf.setTextColor(156, 163, 175)
      
      // Page number
      pdf.text(`Page ${i} of ${totalPages}`, pageWidth - margin, pageHeight - 10, { align: 'right' })
      
      // Footer text
      pdf.text('Generated by DAISY Learning Path Creator', margin, pageHeight - 10)
    }

    // Save the PDF with a more descriptive filename
    const skillSlug = formData.value.skill.toLowerCase().replace(/[^a-z0-9]/g, '-').substring(0, 30)
    const fileName = `learning-path-${skillSlug}-${formData.value.skill_level.toLowerCase().replace(/\s+/g, '-')}-${Date.now()}.pdf`
    pdf.save(fileName)

    // Show success notification
    const toast = useToast()
    toast.add({
      title: 'PDF Generated Successfully',
      description: `Your ${formData.value.skill} learning path has been downloaded as a beautifully formatted PDF.`,
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
  
  // Parse template content as JSON to populate form fields
  try {
    const templateData = JSON.parse(template.content)
    
    // Populate form fields from template
    if (templateData.skill) formData.value.skill = templateData.skill
    if (templateData.skill_level) formData.value.skill_level = templateData.skill_level
    if (templateData.target_time) formData.value.target_time = templateData.target_time
    if (templateData.study_commitment) formData.value.study_commitment = templateData.study_commitment
    
  } catch (e) {
    // If template content is not JSON, treat as skill name
    formData.value.skill = template.content
  }
  
  // Clear selection after short delay
  setTimeout(() => {
    selectedTemplateId.value = null
  }, 1000)
  
  // Track template usage
  trackButtonClick('Use Learning Path Template', {
    templateId: template.id,
    templateTitle: template.title,
    templateContent: template.content
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
    trackButtonClick('Delete Learning Path Template', {
      templateId,
      remainingTemplates: templateStore.userTemplates.length
    })
    
  } catch (error) {
    console.error('Error deleting template:', error)
    trackError('template_delete_failed', 'Failed to delete learning path template', {
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
  trackButtonClick('Create Learning Path Template', {
    templateId: template.id,
    templateTitle: template.title,
    templateContent: template.content,
    hasDescription: !!template.description
  })
}

const onTemplateUpdated = (template) => {
  // Track template update
  trackButtonClick('Update Learning Path Template', {
    templateId: template.id,
    templateTitle: template.title,
    templateContent: template.content,
    hasDescription: !!template.description
  })
}

// SEO
useHead({
  title: 'Learning Path Creator - DAISY',
  meta: [
    {
      name: 'description',
      content: 'Create personalized AI-generated learning paths tailored to your skill level, time commitment, and goals. Get structured study plans with curated resources and milestones.'
    }
  ]
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.prose {
  color: #374151;
}

.prose h1,
.prose h2,
.prose h3 {
  color: #1f2937;
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

.prose h1 {
  font-size: 1.5rem;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 0.5rem;
}

.prose h2 {
  font-size: 1.25rem;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 0.25rem;
}

.prose h3 {
  font-size: 1.125rem;
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

.prose a {
  color: #2563eb;
  text-decoration: underline;
}

.prose a:hover {
  color: #1d4ed8;
}

/* Enhanced Learning Path Styles */
:deep(.prose h1),
.prose h1 {
  font-size: 1.5rem !important;
  font-weight: 600 !important;
  color: #1f2937 !important;
  margin-top: 1.75rem !important;
  margin-bottom: 0.875rem !important;
  padding-bottom: 0.5rem !important;
  border-bottom: 2px solid #e5e7eb !important;
}

:deep(.prose h2),
.prose h2 {
  font-size: 1.25rem !important;
  font-weight: 600 !important;
  color: #1f2937 !important;
  margin-top: 1.5rem !important;
  margin-bottom: 0.75rem !important;
  padding-bottom: 0.25rem !important;
  border-bottom: 1px solid #e5e7eb !important;
}

:deep(.prose h3),
.prose h3 {
  font-size: 1.125rem !important;
  font-weight: 600 !important;
  color: #1f2937 !important;
  margin-top: 1.25rem !important;
  margin-bottom: 0.625rem !important;
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

:deep(.prose a),
.prose a {
  color: #2563eb !important;
  text-decoration: underline !important;
}

:deep(.prose a:hover),
.prose a:hover {
  color: #1d4ed8 !important;
}

/* Enhanced Table Styles */
:deep(.prose table),
.prose table {
  width: 100% !important;
  border-collapse: collapse !important;
  margin: 1.5rem 0 !important;
  background-color: white !important;
  border-radius: 8px !important;
  overflow: hidden !important;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
}

:deep(.prose thead),
.prose thead {
  background-color: #f8fafc !important;
  border-bottom: 2px solid #e2e8f0 !important;
}

:deep(.prose th),
.prose th {
  padding: 12px 16px !important;
  text-align: left !important;
  vertical-align: top !important;
  font-weight: 600 !important;
  font-size: 0.875rem !important;
  color: #374151 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
  border-right: 1px solid #e2e8f0 !important;
  background-color: #f1f5f9 !important;
}

:deep(.prose th:last-child),
.prose th:last-child {
  border-right: none !important;
}

:deep(.prose td),
.prose td {
  padding: 12px 16px !important;
  text-align: left !important;
  vertical-align: top !important;
  border-bottom: 1px solid #e2e8f0 !important;
  border-right: 1px solid #f1f5f9 !important;
  font-size: 0.875rem !important;
  line-height: 1.5 !important;
  color: #4b5563 !important;
}

:deep(.prose td:last-child),
.prose td:last-child {
  border-right: none !important;
}

:deep(.prose tbody tr:nth-child(even)),
.prose tbody tr:nth-child(even) {
  background-color: #f9fafb !important;
}

:deep(.prose tbody tr:hover),
.prose tbody tr:hover {
  background-color: #f0f9ff !important;
}

:deep(.prose tbody tr:last-child td),
.prose tbody tr:last-child td {
  border-bottom: none !important;
}

/* Ensure all links in results open in new window */
:deep(.prose a),
.prose a {
  color: #2563eb !important;
  text-decoration: underline !important;
  font-weight: 500 !important;
}

:deep(.prose a:hover),
.prose a:hover {
  color: #1d4ed8 !important;
  text-decoration: none !important;
}
</style>
